from rest_framework import serializers
from .models import Reservation
class ReservationSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source="room.number", read_only=True)
    class Meta:
        model = Reservation
        fields = ("id", "room", "room_number", "check_in", "check_out", "guests",
                  "special_requests", "status", "total_price", "created_at")
        read_only_fields = ("status", "total_price", "created_at")
    def validate(self, attrs):
        if attrs["check_out"] <= attrs["check_in"]:
            raise serializers.ValidationError("Check-out must be after check-in.")
        if attrs["check_in"] < __import__("datetime").date.today():
            raise serializers.ValidationError("Check-in cannot be in the past.")
        return attrs
