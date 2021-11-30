import requests
import os


class TwitterWrapper:
    twitter_requests_url = "https://api.twitter.com/2/tweets/search/recent"

    def get_bearer_token(self) -> str:
        """Gets Twitter API bearer token from project environment"""

        return os.getenv('TWITTER_BEARER_TOKEN')

    def get_headers(self) -> dict:
        """Gets headers for Twitter API request"""

        return {
            'Authorization': f'Bearer {self.get_bearer_token()}'
        }

    def generate_url(self, hashtag_name: str) -> dict:
        """Generates url for the search request by a hashtag and gets raw data from Twitter API"""

        params = {
            'query': f'#{hashtag_name}',
            'max_results': 10,
            'expansions': 'author_id',
            'tweet.fields': 'created_at,text',
            'user.fields': 'id,name,username',
        }

        headers = self.get_headers()
        response = requests.get(TwitterWrapper.twitter_requests_url, headers=headers, params=params)
        print(response.json())
        return response.json()

    def request_return_handle(self, search_name: str, limit: int) -> list:
        """Handles request return: compares tweets texts and users"""

        hashtag_name = search_name.replace(' ', '')
        print(hashtag_name)
        response_data = self.generate_url(hashtag_name)
        return [
            {
                'created_at': data['created_at'][:10],
                'text': data['text'],
                'author': f"@{includes['username']}",
            }
            for data, includes in zip(response_data['data'][:limit],
                                      response_data['includes']['users'][:limit])] \
            if response_data.get('data') else {}
