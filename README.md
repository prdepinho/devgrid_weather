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
