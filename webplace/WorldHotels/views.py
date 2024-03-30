from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Hotel


def index(request):
    hotel_list = Hotel.objects.order_by("hotel_id")
    paginator = Paginator(hotel_list, 30)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, "WorldHotels/index.html", context)


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    photo_urls = [hotel.photo1, hotel.photo2, hotel.photo3, hotel.photo4, hotel.photo5]

    photo_urls = [url for url in photo_urls if url]

    context = {'hotel': hotel, 'photo_urls': photo_urls}
    return render(request, 'WorldHotels/detail.html', context)
