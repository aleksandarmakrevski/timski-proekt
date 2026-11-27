from django.conf import settings
from django.db import models

class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"), ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"), ("completed", "Completed"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reservations")
    room = models.ForeignKey("rooms.Room", on_delete=models.PROTECT, related_name="reservations")
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveSmallIntegerField(default=1)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reservation #{self.pk} - {self.room}"
