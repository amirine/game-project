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

Now you can check the logs in <code>celery.log</code> file and newly created celery tasks in Django admin
interface <code>Periodic Tasks</code>
section.

How to use API
-------------------------

Most of API requests are available only for authorized users. In order to use project's API properly, please create a user
account or run <code>python3 manage.py createsuperuser</code> to specify an admin user with expanded permissions.

Generally project's REST API functionality includes:

1. Getting games list with pagination (available for authorized and unauthorized users).
2. Getting information for a specific game (available for authorized and unauthorized users).
3. Adding new game to database (available for admin user).
4. Updating a particular game (available for admin user).
5. Deleting a game (available for admin user).
6. Getting list of favourite games (available for authorized users).
7. Adding games to favourites (available for authorized users).
8. Deleting games from favourites (available for authorized users).

Points 1-4 are similarly implemented for genres, platforms, screenshots and covers. Points 6-8 are meant to be performed
within every individual user: users have access to their own musts only.

To retrieve games stored in database make <code>GET</code> request to http://127.0.0.1:8000/api/games/:

```sh
curl "http://127.0.0.1:8000/api/games/"
curl "http://127.0.0.1:8000/api/games/ -u "login:password"
```

This operation doesn't require any user authorization, so both the requests will return the same data. Games are displayed
with pagination, login and password are set according user credentials.

To get information from a specific game run:

```sh
curl http://127.0.0.1:8000/api/games/1/
```

<code>POST</code>, <code>PUT</code> and <code>DELETE</code> methods are prohibited for unauthorized users. To perform
the request pass some extra info about the user: login and password (make sure to set Basic Auth to Postman for such
requests in case of using this service).

To create new entry run:

```sh
curl -X POST http://127.0.0.1:8000/api/games/ -H "Content-Type: application/json" -u "login:password" -d '{"id": 1, "name": "Test Game"}'
```

To delete a particular game run:

```sh
curl -X DELETE http://127.0.0.1:8000/api/games/1/ -u "login:password"
```

To update the game run:

```sh
curl -X PUT http://127.0.0.1:8000/api/games/1/ -u "login:password" -H "Content-Type: application/json" -d '{"id": 1, "name": "Test Game New"}'
```

Genres, platforms, screenshots and covers analogically, appropriate urls:

```sh
curl "http://127.0.0.1:8000/api/genres/"
curl "http://127.0.0.1:8000/api/platforms/"
curl "http://127.0.0.1:8000/api/screenshots/"
curl "http://127.0.0.1:8000/api/covers/"
```

Requests to favourite user games have a slightly different structure. <code>GET</code> method for favourite games
represents list of favourite games for a particular user:

```sh
curl "http://127.0.0.1:8000/api/favourites/" -u "login:password"
```

Method available only for authorized users, pagination implemented. <code>POST</code> method performs 2 basic tasks: add
and delete.
<code>POST</code> request body has the following format:

```sh
{
    "action": <action to perform in string format> (available actions: "add", "delete")
    "game_ids": <list of game ids>
}
```

To make a <code>POST</code> request run:

```sh
curl -X POST http://127.0.0.1:8000/api/favourites/ -H "Content-Type: application/json" -u "login:password" -d '{"action": "add", "game_ids": [1,2]}'
curl -X POST http://127.0.0.1:8000/api/favourites/ -H "Content-Type: application/json" -u "login:password" -d '{"action": "delete", "game_ids": [1,2]}'
```
