from django.urls import path
from .views import HotelInformationView, SponsorListView
urlpatterns = [
    path("", HotelInformationView.as_view()),
    path("sponsors/", SponsorListView.as_view()),
]
