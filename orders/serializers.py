from django.db import transaction

from rest_framework import serializers
from .models import OrderModel, OrderItemModel
from books.serializers import BookSerializer

class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItemModel
            #fields that specified in OrderItemModel
            fields = ('book', 'quantity')

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        with transaction.atomic():
            orderitem_data = validated_data.pop('items', None)
            instance = super().update(instance, validated_data)

            if orderitem_data is not None:
                instance.items.all().delete()
                for item in orderitem_data:
                    OrderItemModel.objects.create(order=instance, **item)
        return instance

    def create(self, validated_data):
        orderitem_data = validated_data.pop('items')
        with transaction.atomic():
            order = OrderModel.objects.create(**validated_data)

            for item in orderitem_data:
                OrderItemModel.objects.create(order=order, **item)
        return order

    class Meta:
        model = OrderModel
        fields = (
            'order_id',
            'user', 
            'status', 
            'items', 
        )

        extra_kwargs = {'user': {'read_only': True}}

class OrderItemSerializer(serializers.ModelSerializer):
    #represent fields that are specidied in BookSerializer
    #book = BookSerializer() #needs to have the same name as in orders/models
    
    #to get some specific fields from foreighn key
    book_name = serializers.CharField(source='book.title') #book: Це назва поля ForeignKey у моделі OrderItemModel
    book_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='book.price')
    class Meta:
        model = OrderItemModel
        fields = ('book_name', 'book_price', 'quantity', )

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = OrderModel
        fields = (
            'order_id', 
            'created_at', 
            'user', 
            'status', 
            'items', 
            'total_price'
            )
        read_only_fields=('order_id', 'created_at','user')