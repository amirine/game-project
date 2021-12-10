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
