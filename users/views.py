from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action

from .models import CustomUser
from .serializers import UserSerializer

# Create your views here.

#[get, post, put, patch]
class UpdateOrReadUsersView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        #for POST-requests
        if action=="create":
            return [AllowAny()]
        return [IsAdminUser()]
        