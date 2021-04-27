## This is a technical test for Coin-Mena.

### List of technologies used:

- Django 3 (BackEnd)
- Celery 4.4.1 (Backend)
- Redis 3.4.1 (Backend)
- Docker and Docker-compose (DevOps)


### To build the project using docker and docker-compose:

```
docker-compose build
```

### To run the server:

```
docker-compose up -d
```

### To Run database migrations inside docker container:

```
docker exec -it backend-coinMena python manage.py makemigrations
docker exec -it backend-coinMena python manage.py migrate
```

### To create a super user for Django admin access:

```
docker exec -it backend-coinMena python manage.py createsuperuser
```
