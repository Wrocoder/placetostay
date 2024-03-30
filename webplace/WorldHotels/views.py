from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import Http404
from .models import Hotel


def index(request):
    hotel_list = Hotel.objects.order_by("hotel_id")[:10]
    template = loader.get_template("WorldHotels/index.html")
    context = {
        "hotel_list": hotel_list,
    }
    return HttpResponse(template.render(context, request))


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    photo_urls = [hotel.photo1, hotel.photo2, hotel.photo3, hotel.photo4, hotel.photo5]

    photo_urls = [url for url in photo_urls if url]

    context = {'hotel': hotel, 'photo_urls': photo_urls}
    return render(request, 'WorldHotels/detail.html', context)
