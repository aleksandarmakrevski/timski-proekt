from django.contrib import admin
from .models import Reservation
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "room", "check_in", "check_out", "guests", "status", "total_price")
    list_filter = ("status", "check_in", "check_out")
    search_fields = ("user__username", "user__email", "room__number")
    readonly_fields = ("created_at",)
