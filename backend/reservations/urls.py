from django.urls import path
from .views import MyReservationsView
urlpatterns = [path("", MyReservationsView.as_view())]
