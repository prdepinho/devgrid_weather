# devgrid_weather
A Django Rest Server that provides weather information.


# How to test and run the server:

This service uses Docker to run. You can install it in the link: https://docs.docker.com/desktop/install/windows-install/.

Run tests: 
```
docker-compose run --rm web python manage.py runserver
```

Run server:
```
docker-compose up --build
```

You need to have a .env file with API_KEY set to the key
to the OpenWeatherMap API.

You can use client.py to interact with the server.


# The Service

## POST:
```
http://localhost:8000/weather/api/
```
Post requires the followings parameters: the user id, which is a UUID string,
and a list of the city ids to query OpenWeatherMap.
```
'user_id': '293b6acc-2b78-4ddc-9ef8-632cde33ef80',
'cities': [3439525, 3439781, 3440645, 3442098, ... ]
```
This method will return 409 if the user already exists. 
Otherwise, it will return 202 immediately, and will start working
on the queries. The service will ensure that no more than 60 cities will
be queried per minute.

To keep track of the queries, use the GET method that follows.

## GET:
```
http://localhost:8000/weather/api/?user_id=293b6acc-2b78-4ddc-9ef8-632cde33ef80
```
Get receives a user_id as parameter, in the form of a UUID string.
If the user doesn't exist, the method will return 404. Otherwise,
it will return 200 and in the body there will be the following data:
```
    "status": 200,
    "body": "optional",
    "progress": 0.0,
    "cities": [ 
        {
            "id": 0,
            "name": "",
            "country": "",
            "temperature": 0.0,
            "humidity": 0.0
        }
    ]
```
The parameter `status` is the status of the last query given by OpenWeatherMap.
If it is 200, the query has been completed successfully. It will always be 200
if the GET method returned 200, and `body` will not be present.

`progress` is where the progress of the query is,
in percentage. When it comes to 100, then the query is finished.

`cities` is the list of information for each city queried. It gives the city
`id`, `name`, `country`, `temperature` in degrees celcius, and `humidity` in percentage.

If the query to OpenWeatherMap failed somehow, then the GET method will return
status 409, `status` will contain the status of the last OpenWeatherMap query 
and `body` will contain the error message of that call.
