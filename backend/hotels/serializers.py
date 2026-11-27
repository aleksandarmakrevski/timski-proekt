from rest_framework import serializers
from .models import HotelInformation, Sponsor
class HotelInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelInformation
        fields = "__all__"
class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = "__all__"
