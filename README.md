# game-project

Getting Started
-------------------------

This application uses data from the video games database [IGDB API](https://api.igdb.com/)
and [Twitter API](https://dev.twitter.com/rest/public) for retrieving tweets by game name hashtag. Therefore, pay
attention some environment variables are needed for these APIs access.

IGDB API access variables:

```sh
IGDB_CLIENT_ID=
IGDB_CLIENT_SECRET=
```

Twitter API access variables:

```sh
TWITTER_BEARER_TOKEN=
```

The application supports sending confirmation emails to users when signing up (django-allauth package), that's why some
additional variables are also required:

```sh
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_HOST=
EMAIL_PORT=
```

To change the application settings so that the PostgreSQL database is used, the following environment variables needed:

```sh
DB_NAME=
DB_USERNAME=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

Please copy .env.example content into .env file and fill the required credentials.

How to update games database
-------------------------
For downloading games data from [IGDB API](https://api.igdb.com/) to your project database (or to update existing
entries) use <code>update_db</code> django management command. Specified custom command can be called using:

```sh
python3 manage.py update_db
```

To refresh games data on regular basis celery tasks are also created. Start celery worker and beat by running

```sh
celery -A game_project worker -l info --logfile=celery.log --detach
celery -A game_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Now you can check the logs in <code>celery.log</code> file and newly created celery tasks in Django admin interface *Periodic Tasks*
section.

How to use API
-------------------------

Most of the requests to the API are available only for authorized users. So in order to use it, please create an
account, or a superuser with all the available permissions - testing project's REST API would be much easier and wider.

To create admin user for the project, just run

```sh
python3 manage.py createsuperuser
```

and fill the required fields info. Creating any type of user will enable you to add and delete games from musts.

Generally project's REST API functionality includes:

1. Getting games list with pagination (available for authorized and unauthorized users).
2. Getting information for a specific game (available for authorized and unauthorized users).
3. Adding new game to database (available for admin user).
4. Updating a particular game (available for admin user).
5. Deleting a game (available for admin user).
6. Getting list of favourite games of an authorized user with pagination (available for authorized users).
7. Adding games to favourites for an authorized user (available for authorized users).
8. Deleting games from favourites for an authorized user (available for authorized users).

Points 1-4 are similarly implemented for genres, platforms, screenshots and covers. Points 6-8 are meant to be performed
within every individual user: users has access to their own musts only.

To retrieve games stored in database make <code>GET</code> request to <code> http://127.0.0.1:8000/api/games/ </code>:

```sh
curl "http://127.0.0.1:8000/api/games/"
```

or

```sh
curl "http://127.0.0.1:8000/api/games/ -u "login:password"
```

This operation doesn't require any user authorization, so both the requests will return the same data. Games are
displayed with pagination. Login and password set according user credentials.

To get all information from a specific game run:

```sh
curl http://127.0.0.1:8000/api/games/1/
```

POST, PUT and DELETE methods are prohibited for unauthorized users. To perform the request you should pass some extra
info about the user: login and password (make sure to set Basic Auth to Postman for such requests in case of using this
service).

POST method (new entry creation):

```sh
curl -X POST http://127.0.0.1:8000/api/games/ -H "Content-Type: application/json" -u "login:password" -d '{"id": 1, "name": "Test Game"}'
```

DELETE method (entry removal):

```sh
curl -X DELETE http://127.0.0.1:8000/api/games/1/ -u "login:password"
```

PUT method (entry update):

```sh
curl -X PUT http://127.0.0.1:8000/api/games/1/ -u "login:password" -H "Content-Type: application/json" -d '{"id": 1, "name": "Test Game New"}'
```

Analogically genres, platforms, screenshots and covers, appropriate urls:

```sh
curl "http://127.0.0.1:8000/api/genres/"
curl "http://127.0.0.1:8000/api/platforms/"
curl "http://127.0.0.1:8000/api/screenshots/"
curl "http://127.0.0.1:8000/api/covers/"
```

Requests to favourite user games have a little another structure. Get method for favourite games represents list of
favourite games for a particular user. Available only for auth users, pagination implemented

```sh
curl "http://127.0.0.1:8000/api/favourites/" -u "ira:admin"
```

