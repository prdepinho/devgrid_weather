from django.test import TestCase
from django.db import IntegrityError
from .models import User
from uuid import UUID, uuid4
import json
import threading
import time
from django.utils import timezone
from .views import get_weather, get_progress, get_weather_background

# Create your tests here.

class WeatherTestCase(TestCase):

    def test_user(self):
        now = timezone.now()
        data = {
                'user_id': '193b6acc-2b78-4ddc-9ef8-632cde33ef74',
                'cities': [3439525, 3439781, 3440645, 3442098, 3442778, 3443341, 3442233, 3440781,
                           3441572, 3441575, 3443207, 3442546, 3441287, 3441242, 3441686, 3440639,
                           3441354, 3442057, 3442585, 3442727, 3439705, 3441890, 3443411, 3440054,
                           3441684, 3440711, 3440714, 3440696, 3441894, 3443173, 3441702, 3442007,
                           3441665, 3440963, 3443413, 3440033, 3440034, 3440571, 3443025, 3441243,
                           3440789, 3442568, 3443737, 3440771, 3440777, 3442597, 3442587, 3439749,
                           3441358, 3442980, 3442750, 3443352, 3442051, 3441442, 3442398, 3442163,
                           3443533, 3440942, 3442720, 3441273, 3442071, 3442105, 3442683, 3443030,
                           3441011, 3440925, 3440021, 3441292, 3480823, 3440379, 3442106, 3439696,
                           3440063, 3442231, 3442926, 3442050, 3440698, 3480819, 3442450, 3442584,
                           3443632, 3441122, 3441475, 3440791, 3480818, 3439780, 3443861, 3440780,
                           3442805, 7838849, 3440581, 3440830, 3443756, 3443758, 3443013, 3439590,
                           3439598, 3439619, 3439622, 3439652, 3439659, 3439661, 3439725, 3439748,
                           3439787, 3439831, 3439838, 3439902, 3440055, 3440076, 3440394, 3440400,
                           3440541, 3440554, 3440577, 3440580, 3440596, 3440653, 3440654, 3440684,
                           3440705, 3440747, 3440762, 3440879, 3440939, 3440985, 3441074, 3441114,
                           3441377, 3441476, 3441481, 3441483, 3441577, 3441659, 3441674, 3441803,
                           3441954, 3441988, 3442058, 3442138, 3442206, 3442221, 3442236, 3442238,
                           3442299, 3442716, 3442766, 3442803, 3442939, 3443061, 3443183, 3443256,
                           3443280, 3443289, 3443342, 3443356, 3443588, 3443631, 3443644, 3443697,
                           3443909, 3443928, 3443952, 3480812, 3480820, 3480822, 3480825
                           ]
               }
        json_foo = {
                "id": data['user_id'],
                "list": [
                    {"foo": 1, "bar": 2},
                    {"foo": 2, "bar": 3},
                    ]
                }


        user = User.objects.create(id=UUID(data['user_id']), date=now)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, UUID(data['user_id']))

        user = User.objects.get(id=UUID(data['user_id']))
        self.assertIsNotNone(user)

        user.progress = 50.0
        user.json = json.dumps(json_foo)
        user.save()

        self.assertTrue(len(User.objects.filter(id=data['user_id'])) > 0)

        user = User.objects.get(id=UUID(data['user_id']))
        self.assertIsNotNone(user)
        self.assertEqual(user.id, UUID(data['user_id']))
        self.assertEqual(user.progress, 50.0)
        self.assertEqual(user.date, now)
        self.assertEqual(json.loads(user.json), json_foo)

        json_obj = {"foo": 3, "bar": 4}
        json_data = json.loads(user.json)
        json_data['list'].append(json_obj)
        json_foo['list'].append(json_obj)
        user.json = json.dumps(json_data)
        user.save()

        user = User.objects.get(id=UUID(data['user_id']))
        self.assertEqual(json.loads(user.json), json_foo)

        user = User.objects.get(id=UUID(data['user_id']))
        self.assertIsNotNone(user)
        user.delete()

        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(id=UUID(data['user_id']))
    

    def test_get_weather(self):
        data = {
                'user_id': str(uuid4()),
                'cities': [3439525, 3439781, 3440645, 3442098, 3442778, 3443341, 3442233, 3440781,
                           3441572, 3441575, 3443207, 3442546, 3441287, 3441242, 3441686, 3440639,
                           3441354, 3442057, 3442585, 3442727, 3439705, 3441890, 3443411, 3440054,
                           3441684, 3440711, 3440714, 3440696, 3441894, 3443173, 3441702, 3442007,
                           3441665, 3440963, 3443413, 3440033, 3440034, 3440571, 3443025, 3441243,
                           3440789, 3442568, 3443737, 3440771, 3440777, 3442597, 3442587, 3439749,
                           3441358, 3442980, 3442750, 3443352, 3442051, 3441442, 3442398, 3442163,
                           3443533, 3440942, 3442720, 3441273, 3442071, 3442105, 3442683, 3443030,
                           3441011, 3440925, 3440021, 3441292, 3480823, 3440379, 3442106, 3439696,
                           3440063, 3442231, 3442926, 3442050, 3440698, 3480819, 3442450, 3442584,
                           3443632, 3441122, 3441475, 3440791, 3480818, 3439780, 3443861, 3440780,
                           3442805, 7838849, 3440581, 3440830, 3443756, 3443758, 3443013, 3439590,
                           3439598, 3439619, 3439622, 3439652, 3439659, 3439661, 3439725, 3439748,
                           3439787, 3439831, 3439838, 3439902, 3440055, 3440076, 3440394, 3440400,
                           3440541, 3440554, 3440577, 3440580, 3440596, 3440653, 3440654, 3440684,
                           3440705, 3440747, 3440762, 3440879, 3440939, 3440985, 3441074, 3441114,
                           3441377, 3441476, 3441481, 3441483, 3441577, 3441659, 3441674, 3441803,
                           3441954, 3441988, 3442058, 3442138, 3442206, 3442221, 3442236, 3442238,
                           3442299, 3442716, 3442766, 3442803, 3442939, 3443061, 3443183, 3443256,
                           3443280, 3443289, 3443342, 3443356, 3443588, 3443631, 3443644, 3443697,
                           3443909, 3443928, 3443952, 3480812, 3480820, 3480822, 3480825
                           ]
               }

        user = User.objects.create(id=data['user_id'], date=timezone.now())
        user.json = '{"status": 200, "cities": []}'
        user.save()
        get_weather_background(data['user_id'], data['cities'])

        rval = get_progress(data['user_id'])
        self.assertEqual(rval.status_code, 200)
        answer = json.loads(rval.content)

        self.assertTrue('progress' in answer)
        self.assertEqual(answer['progress'], 100.0)
        self.assertTrue('cities' in answer)
        self.assertEqual(len(data['cities']), len(answer['cities']))
        for city in answer['cities']:
            self.assertTrue('id' in city)
            self.assertTrue('name' in city)
            self.assertTrue('country' in city)
            self.assertTrue('temperature' in city)
            self.assertTrue('humidity' in city)


