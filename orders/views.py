from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from .models import OrderModel, OrderItemModel
from .serializers import OrderSerializer, OrderItemSerializer, OrderCreateSerializer

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    throttle_scope = 'orders'
    serializer_class = OrderSerializer
    permission_classes=[IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return OrderModel.objects.all()
        return OrderModel.objects.filter(user=user)

    @method_decorator([cache_page(60*15, key_prefix='order_list')])
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)

    def get_serializer_class(self):
        #if we send a POST request - use OrderCreateSerializer
        if self.action=='create' or self.action=='update':
        #if self.request.method=="POST":
            return OrderCreateSerializer
        #otherwise use serializer that specified in serializer_class
        return super().get_serializer_class()