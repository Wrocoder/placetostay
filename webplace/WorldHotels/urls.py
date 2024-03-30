from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("WorldHotels/<int:hotel_id>/", views.hotel_detail, name="detail"),

]