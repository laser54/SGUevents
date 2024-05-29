from django.db import models
from events_available.models import Events_online, Events_offline

class Product(models.Model):
    favourite = models.ManyToManyField(Events_online, default=None, blank=True, related_name='favourite_product')
    slug = models.SlugField(unique=True, blank=True, max_length=254)
