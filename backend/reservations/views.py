from decimal import Decimal
from django.db import transaction
from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Reservation
from .serializers import ReservationSerializer

class MyReservationsView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).select_related("room")

    @transaction.atomic
    def perform_create(self, serializer):
        data = serializer.validated_data
        room = data["room"]
        if not room.is_active:
            raise ValidationError("This room is not available for booking.")
        if data["guests"] > room.capacity:
            raise ValidationError("Guest count exceeds room capacity.")
        overlap = Reservation.objects.select_for_update().filter(
            room=room,
            status__in=["pending", "confirmed"],
            check_in__lt=data["check_out"],
            check_out__gt=data["check_in"],
        ).exists()
        if overlap:
            raise ValidationError("This room is already reserved for the selected dates.")
        nights = (data["check_out"] - data["check_in"]).days
        serializer.save(user=self.request.user, total_price=room.price_per_night * Decimal(nights))
