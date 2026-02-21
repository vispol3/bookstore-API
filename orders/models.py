from django.db import models
import uuid

from users.models import CustomUser
from books.models import Books

# Create your models here.
class OrderModel(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    books = models.ManyToManyField(Books, through="OrderItemModel", related_name='orders') #books - в множині
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    class Meta:
        db_table = 'order_table'

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    
class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Books, on_delete=models.CASCADE) #book - в однині
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'order_item_table'

    @property
    def item_subtotal(self):
        return self.book.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.book.title} in Order {self.order.order_id}"