import os

from django.core.paginator import Paginator
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .common_methods_views.common import get_weather_forecast, get_flicker_photo, get_youtube_videos, rss_feed_view
from .forms import SearchForm
from .models import Hotel, DummyWeatherData, TourismData, CountryDescriptionData


def index(request):
    hotel_list = Hotel.objects.order_by("hotel_id")
    paginator = Paginator(hotel_list, 30)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    articles = rss_feed_view()
    context = {'page_obj': page_obj, 'articles': articles}
    return render(request, "WorldHotels/index.html", context)


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)

    # photo_urls = [hotel.photo1, hotel.photo2, hotel.photo3, hotel.photo4, hotel.photo5]
    # photo_urls = [url for url in photo_urls if url]

    weather_forecast = get_weather_forecast(hotel.latitude, hotel.longitude)

    photos = get_flicker_photo(hotel.latitude, hotel.longitude)

    context = {'hotel': hotel,
               'photo_urls': photos,
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
            if not tourists:  # Check if the list is empty
                tourists = 'No information'
            else:
                tourists = int(tourists[0].total)

            country_description = CountryDescriptionData.objects.filter(country_name=country)

            youtube_videos = get_youtube_videos(country)

            context = {'hotels': hotels, 'country': country,
                       'month': month, 'average_weather': average_weather[0],
                       'tourists': tourists,
                       'country_description': country_description[0],
                       'videos': youtube_videos}

            return render(request, 'WorldHotels/result.html', context)
    else:
        form = SearchForm()

    return render(request, 'WorldHotels/search.html', {'form': form})
