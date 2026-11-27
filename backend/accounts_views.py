from django.contrib.auth.models import User
from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "password")
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "is_staff": request.user.is_staff,
        })
