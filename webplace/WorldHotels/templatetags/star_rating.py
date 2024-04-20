from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def star_rating(rating):
    full_stars = int(rating)
    # print(full_stars)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    stars_html = (
            '<i class="fas fa-star"></i>' * full_stars +
            ('<i class="fas fa-star-half-alt"></i>' if half_star else '') +
            '<i class="far fa-star"></i>' * empty_stars
    )

    return mark_safe(stars_html)