from django.contrib import admin
from .models import Room, RoomType, Amenity, RoomImage
class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("number", "room_type", "price_per_night", "beds", "floor", "is_active")
    list_filter = ("room_type", "beds", "floor", "view", "is_active")
    search_fields = ("number",)
    inlines = [RoomImageInline]
admin.site.register(RoomType)
admin.site.register(Amenity)
