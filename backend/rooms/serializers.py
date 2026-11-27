from rest_framework import serializers
from .models import Room, RoomImage, Amenity
class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("id", "name")
class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ("id", "image", "caption")
class RoomSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    room_type_name = serializers.CharField(source="room_type.name", read_only=True)
    class Meta:
        model = Room
        fields = ("id", "number", "room_type", "room_type_name", "description",
                  "price_per_night", "beds", "floor", "capacity", "view",
                  "is_active", "amenities", "images")
