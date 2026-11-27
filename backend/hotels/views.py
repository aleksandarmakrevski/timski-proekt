from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import HotelInformation, Sponsor
from .serializers import HotelInformationSerializer, SponsorSerializer

class HotelInformationView(generics.ListAPIView):
    queryset = HotelInformation.objects.all()
    serializer_class = HotelInformationSerializer
    permission_classes = [AllowAny]

class SponsorListView(generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [AllowAny]
