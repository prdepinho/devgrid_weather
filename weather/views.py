from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from uuid import UUID
from .models import User
import json
import requests
import os
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def api(request):
    if request.method == "GET":
        try:
            id = request.GET.get('user_id')
            user_id = UUID(id)
        except (ValueError, TypeError):
            return JsonResponse({}, status=400)

        return get_progress(user_id)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = UUID(data['user_id'])
            cities = data['cities']
        except (ValueError, TypeError, KeyError):
            return JsonResponse({}, status=400)

        return get_weather(user_id, cities)

    else:
        return JsonResponse({}, status=405)


def get_progress(user_id):
    try:

        user = User.objects.select_for_update().get(id=user_id)
        return JsonResponse({'progress': user.progress}, status=200)

    except User.DoesNotExist:
        return JsonResponse({}, status=404)


def get_weather(user_id, cities):
    api_key = os.environ.get("API_KEY")

    if len(User.objects.filter(id=user_id)) > 0:
        return JsonResponse({'message': 'User already exists'}, status=409)

    user = User.objects.create(id=user_id, cities=cities)

    i = 0
    step = 20

    rval = { "cities": [] }

    while i < len(cities):
        step = min(step, len(cities) - i)

        url = f"https://api.openweathermap.org/data/2.5/group"
        params = {
                "id": ','.join(str(id) for id in cities[i:i+step]),
                "appid": api_key,
                "units": "metric"
                }
        i += step

        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            user.delete()
            return JsonResponse(resp.json(), status=resp.status_code)

        data = resp.json()

        length = data['cnt']
        records = data['list']

        for record in records:
            city = {
                    'id': record['id'],
                    'name': record['name'],
                    'country': record['sys']['country'],
                    'temperature': record['main']['temp'],
                    'humidity': record['main']['humidity']
                    }
            rval['cities'].append(city)

        with transaction.atomic():
            user = User.objects.select_for_update().get(id=user_id)
            user.progress = i / len(cities) * 100
            user.save()

    return JsonResponse(rval, status=200)
