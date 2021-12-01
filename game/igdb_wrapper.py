import os
import requests
from game.igdb_data_format import format_data


class IGDBWrapper:
    db_requests_url = 'https://api.igdb.com/v4'
    access_token_url = 'https://id.twitch.tv/oauth2/token'

    def __init__(self) -> None:
        self.client_id = self.get_client_id()
        self.client_secret = self.get_client_secret()
        self.grant_type = self.get_grant_type()

    @staticmethod
    def get_client_secret() -> str:
        """Gets client secret from the project environment"""

        return os.getenv('IGDB_CLIENT_SECRET')

    @staticmethod
    def get_client_id() -> str:
        """Gets client id from the project environment"""

        return os.getenv('IGDB_CLIENT_ID')

    @staticmethod
    def get_grant_type() -> str:
        """Returns grant_type needed"""

        return "client_credentials"

    def get_access_token(self) -> str:
        """Gets access token using client_id, client_secret and grant_type"""

        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': self.grant_type,
        }
        response = requests.post(IGDBWrapper.access_token_url, data=params)
        return response.json().get('access_token')

    def get_headers(self) -> dict:
        """Generates required headers for requests"""

        return {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.get_access_token()}',
        }

    @staticmethod
    def generate_url_by_endpoint(endpoint: str) -> str:
        """Generates url for requests using endpoint"""

        return f'{IGDBWrapper.db_requests_url}/{endpoint}'

    def get_json_data_by_query(self, query: str, endpoint: str) -> list:
        """Makes api request to IGDB and returns list of required values using query input.
           Format data function transforms a return to a required format"""

        headers = self.get_headers()
        url = self.generate_url_by_endpoint(endpoint)
        response = requests.post(url, headers=headers, data=query)
        return format_data(response.json())


class IGDBRequestsHandler(IGDBWrapper):

    def get_genres(self) -> list:
        """Gets all genres names and ids of a database"""

        return self.get_json_data_by_query("fields name;", "genres")

    def get_platforms(self) -> list:
        """Gets all platforms names and ids of a database"""

        return self.get_json_data_by_query("fields name;", "platforms")

    def get_game_main_page_info(self, limit: int, filters=None) -> list:
        """Gets main page data from IGDB"""

        query = f"fields name, genres.name, cover.image_id; limit {limit}; "
        if filters:
            query += f"where total_rating >= {filters['lower_rating_bound']} & " \
                     f"total_rating <= {filters['upper_rating_bound']}"
            if filters.get('genres'):
                query += f" & genres = ({', '.join(filters['genres'])})"
            if filters.get('platforms'):
                query += f" & platforms = ({', '.join(filters['platforms'])})"
            query += ";"
        return self.get_json_data_by_query(query, "games")

    def get_game_detail_page_info(self, game_id: int) -> list:
        """Gets detail page data from IGDB"""

        return self.get_json_data_by_query(
            f"fields name, genres.name, platforms.abbreviation, summary, first_release_date, screenshots.image_id,"
            f"rating, rating_count, aggregated_rating, aggregated_rating_count; where id = {game_id};",
            "games"
        )[0]

    def get_game_search_info(self, search_input: str, limit: int) -> list:
        """Gets results of the search"""

        return self.get_json_data_by_query(
            f'fields name, genres.name, cover.image_id; search "{search_input}";limit {limit};', "games")
