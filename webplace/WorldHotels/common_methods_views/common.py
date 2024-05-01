import os
from collections import Counter
from itertools import groupby

import feedparser
import flickrapi
import requests
from django.utils.dateparse import parse_datetime
from googleapiclient.discovery import build


def get_youtube_videos(country_name):
    youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
    request = youtube.search().list(
        q=country_name,
        part='snippet',
        maxResults=5,
        type='video'
    )
    response = request.execute()

    videos = []
    for item in response.get('items', []):
        videos.append({
            'title': item['snippet']['title'],
            'video_url': f'{item["id"]["videoId"]}'
        })

    return videos


def rss_feed_view():
    # RSS links
    # feed_url = 'https://againstthecompass.com/en/travel-blog/feed'
    # feed_url = 'https://travel.economictimes.indiatimes.com/rss/events/international'
    # feed_url = 'https://againstthecompass.com/en/travel-blog/feed'
    # feed_url = 'https://borednomad.com/feed/'
    feed_url = 'https://www.aluxurytravelblog.com/feed/'
    feed = feedparser.parse(feed_url)
    articles = [{
        'title': entry.title,
        'summary': entry.summary,
        'link': entry.link,
        'published': entry.published,
        'authors': entry.author,
        # 'value': entry.content,
    } for entry in feed.entries]
    return articles


def get_flicker_photo(lat, lon):
    flickr = flickrapi.FlickrAPI(os.getenv('FLICKER_API_KEY'), os.getenv('FLICKER_SECRET_KEY'), format='parsed-json')
    params = {
        'content_type': 1,  # only photos
        'media': 'photos',
        'tags': 'travel, hotel, ',
        'min_upload_date': 1577836800,
        'has_geo': '1',
        'lat': lat,
        'lon': lon,
        'radius': '10',
        'per_page': '10',
        'page': '1',
        'privacy_filter': 1,
        'sort': 'interestingness-desc'

    }

    photos = flickr.photos.search(**params)
    result_photo = []
    for photo in photos['photos']['photo']:
        url = f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}_w.jpg"
        result_photo.append(url)

    return result_photo


def process_weather_data(weather_data):
    result = {}
    for date, entries in weather_data.items():
        average_temp = sum((entry['main']['temp'] - 273.15) for entry in entries) / len(entries)

        all_descriptions = [item['description'] for entry in entries for item in entry['weather']]
        all_mains = [item['main'] for entry in entries for item in entry['weather']]

        most_common_description = Counter(all_descriptions).most_common(1)[0][0]
        most_common_main = Counter(all_mains).most_common(1)[0][0]

        result[date.strftime("%A, %d %B %Y")] = {
            'average_temp': round(average_temp, 2),
            'most_common_description': most_common_description,
            'most_common_main': most_common_main
        }

    return result


def get_weather_forecast(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={os.getenv('WEATHER_API_KEY')}"

    response = requests.get(url)
    weather_data = response.json()
    weather_list = weather_data['list']
    for item in weather_list:
        item['dt'] = parse_datetime(item['dt_txt'])
    grouped_weather = {
        k: list(g) for k, g in groupby(weather_list, key=lambda x: parse_datetime(x['dt_txt']).date())
    }

    return process_weather_data(grouped_weather)
