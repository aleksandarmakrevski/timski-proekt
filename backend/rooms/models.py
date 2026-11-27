from django.db import models

class RoomType(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self):
        return self.name

class Room(models.Model):
    VIEW_CHOICES = [
        ("sea", "Sea"), ("city", "City"), ("garden", "Garden"),
        ("mountain", "Mountain"), ("other", "Other"),
    ]
    number = models.CharField(max_length=20, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name="rooms")
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    beds = models.PositiveSmallIntegerField(default=1)
    floor = models.PositiveSmallIntegerField(default=0)
    capacity = models.PositiveSmallIntegerField(default=2)
    view = models.CharField(max_length=20, choices=VIEW_CHOICES, default="other")
    is_active = models.BooleanField(default=True)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="rooms")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.number}"

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="rooms/")
    caption = models.CharField(max_length=150, blank=True)
