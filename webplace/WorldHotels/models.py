from django.db import models


class Hotel(models.Model):
    hotel_id = models.BigIntegerField(primary_key=True)
    chain_id = models.IntegerField(null=True, blank=True)
    chain_name = models.CharField(max_length=255, null=True, blank=True)
    brand_id = models.IntegerField(null=True, blank=True)
    brand_name = models.CharField(max_length=255, null=True, blank=True)
    hotel_name = models.CharField(max_length=255, null=True, blank=True)
    hotel_formerly_name = models.CharField(max_length=255, null=True, blank=True)
    hotel_translated_name = models.CharField(max_length=255, null=True, blank=True)
    addressline1 = models.CharField(max_length=600, null=True, blank=True)
    addressline2 = models.CharField(max_length=600, null=True, blank=True)
    zipcode = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100)
    countryisocode = models.CharField(max_length=5, null=True, blank=True)
    star_rating = models.FloatField(null=True, blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    url = models.URLField(null=True, blank=True)
    checkin = models.CharField(max_length=20, null=True, blank=True)
    checkout = models.CharField(max_length=20, null=True, blank=True)
    numberrooms = models.IntegerField(null=True, blank=True)
    numberfloors = models.IntegerField(null=True, blank=True)
    yearopened = models.IntegerField(null=True, blank=True)
    yearrenovated = models.IntegerField(null=True, blank=True)
    photo1 = models.URLField(null=True, blank=True)
    photo2 = models.URLField(null=True, blank=True)
    photo3 = models.URLField(null=True, blank=True)
    photo4 = models.URLField(null=True, blank=True)
    photo5 = models.URLField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    rates_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    continent_id = models.IntegerField(null=True, blank=True)
    continent_name = models.CharField(max_length=100, null=True, blank=True)
    city_id = models.IntegerField(null=True, blank=True)
    country_id = models.IntegerField(null=True, blank=True)
    number_of_reviews = models.IntegerField(null=True, blank=True)
    rating_average = models.FloatField(null=True, blank=True)
    rates_currency = models.CharField(max_length=20, null=True, blank=True)
    rates_from_exclusive = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    accommodation_type = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.country} - {self.hotel_name}"

    class Meta:
        verbose_name_plural = "Hotel Data"


class TourismData(models.Model):
    country = models.CharField(max_length=100, null=True, verbose_name="Continent and Destination Country")
    tourism_concept = models.CharField(max_length=50, null=True, verbose_name="Tourism Concept")
    period = models.CharField(max_length=10, null=True, verbose_name="Period")
    year = models.IntegerField(null=True, verbose_name="Year")
    month = models.CharField(max_length=20, null=True, verbose_name="Month")
    total = models.FloatField(null=True, verbose_name="Total")

    def __str__(self):
        return f"{self.country} - {self.period}"

    class Meta:
        verbose_name_plural = "Tourism Data"


class DummyWeatherData(models.Model):
    country = models.CharField(max_length=100)
    month = models.CharField(max_length=10)
    average_temperature = models.CharField(max_length=10)
    precipitation_level = models.CharField(max_length=10)
    air_speed = models.CharField(max_length=10)
    recommended_to_visit = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.country} - {self.month}"

    class Meta:
        verbose_name_plural = "Weather Data"
