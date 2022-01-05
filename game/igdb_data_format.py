from datetime import datetime


def image_transform(image_id: str, size='720p') -> str:
    """Transforms image_id from IGDB to link format"""

    return f"https://images.igdb.com/igdb/image/upload/t_{size}/{image_id}.jpg"


def date_transform(date: int) -> str:
    """Transforms int date to <year>-<month>-<day> format"""

    return datetime.fromtimestamp(date).strftime("%Y-%m-%d")


def format_data(data_to_format: list) -> list:
    """Transforms needed data to a required format for the pages"""

    for data in data_to_format:

        if data.get('cover'):
            data['cover']['image_id'] = image_transform(data['cover']['image_id'])

        if data.get('screenshots'):
            for screenshot in data['screenshots']:
                screenshot['image_id'] = image_transform(screenshot['image_id'])

        if data.get('first_release_date'):
            data['first_release_date'] = date_transform(data['first_release_date'])

    return data_to_format
