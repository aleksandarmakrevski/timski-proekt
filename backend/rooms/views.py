from datetime import date
from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Room
from .serializers import RoomSerializer
from reservations.models import Reservation

class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Room.objects.filter(is_active=True).select_related("room_type").prefetch_related("amenities", "images")
        params = self.request.query_params
        if params.get("min_price"):
            qs = qs.filter(price_per_night__gte=params["min_price"])
        if params.get("max_price"):
            qs = qs.filter(price_per_night__lte=params["max_price"])
        if params.get("beds"):
            qs = qs.filter(beds=params["beds"])
        if params.get("floor"):
            qs = qs.filter(floor=params["floor"])
        if params.get("view"):
            qs = qs.filter(view=params["view"])
        if params.get("check_in") and params.get("check_out"):
            try:
                start = date.fromisoformat(params["check_in"])
                end = date.fromisoformat(params["check_out"])
                if end <= start:
                    return qs.none()
                busy_ids = Reservation.objects.filter(
                    status__in=["pending", "confirmed"],
                    check_in__lt=end,
                    check_out__gt=start
                ).values_list("room_id", flat=True)
                qs = qs.exclude(id__in=busy_ids)
            except ValueError:
                return qs.none()
        return qs
