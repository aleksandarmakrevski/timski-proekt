from django.db import models

class HotelInformation(models.Model):
    name = models.CharField(max_length=150, default="Hotel")
    description = models.TextField(blank=True)
    history = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    map_embed_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Sponsor(models.Model):
    name = models.CharField(max_length=150)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to="sponsors/", blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
