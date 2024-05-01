from django.contrib import admin

from .models import Hotel, TravelHackLink, TravelHackImage, TravelHack, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class TravelHackImageInline(admin.TabularInline):
    model = TravelHackImage
    extra = 1


class TravelHackLinkInline(admin.TabularInline):
    model = TravelHackLink
    extra = 1


class TravelHackAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date']
    inlines = [TravelHackImageInline, TravelHackLinkInline]
    filter_horizontal = ('categories',)  # More simple to choose category from admin panel


admin.site.register(Category, CategoryAdmin)
admin.site.register(TravelHack, TravelHackAdmin)
admin.site.register(Hotel)
