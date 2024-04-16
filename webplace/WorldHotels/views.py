import os
from itertools import groupby

import requests
from django.core.paginator import Paginator
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.dateparse import parse_datetime

from .forms import SearchForm
from .models import Hotel, DummyWeatherData, TourismData, CountryDescriptionData


def index(request):
    hotel_list = Hotel.objects.order_by("hotel_id")
    paginator = Paginator(hotel_list, 30)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, "WorldHotels/index.html", context)


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
    # print(grouped_weather)
    return grouped_weather


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)

    photo_urls = [hotel.photo1, hotel.photo2, hotel.photo3, hotel.photo4, hotel.photo5]

    photo_urls = [url for url in photo_urls if url]

    weather_forecast = get_weather_forecast(hotel.latitude, hotel.longitude)

    context = {'hotel': hotel,
               'photo_urls': photo_urls,
               'google_maps_api': os.getenv('GOOGLE_MAPS_API_KEY'),
               'weather_forecast': weather_forecast,
               'weather_api_key': os.getenv('WEATHER_API_KEY')}

    return render(request, 'WorldHotels/detail.html', context)


def search_hotels(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            country = form.cleaned_data['country']

            average_weather = DummyWeatherData.objects.filter(country=country, month=month)
            hotels = Hotel.objects.filter(country=country)

            max_year = TourismData.objects.filter(country=country, month=month) \
                .aggregate(max_year=Max('year'))['max_year']

            tourists = TourismData.objects.filter(country=country, month=month, year=max_year)

            country_description = CountryDescriptionData.objects.filter(country_name=country)

            context = {'hotels': hotels, 'country': country,
                       'month': month, 'average_weather': average_weather[0],
                       'tourists': tourists[0],
                       'country_description': country_description[0]}

            return render(request, 'WorldHotels/result.html', context)
    else:
        form = SearchForm()

    return render(request, 'WorldHotels/search.html', {'form': form})
