from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.core.cache import cache

from .models import OrderModel, OrderItemModel

from users.models import CustomUser
from books.models import Books

# Create your tests here.
class OrdersAPITestCase(APITestCase):
    def setUp(self):
        cache.clear()
        self.admin_user = CustomUser.objects.create_superuser(username="admin", password="adminpass")
        self.normal_user_1 = CustomUser.objects.create_user(username="user1", password="user1pass")
        self.normal_user_2 = CustomUser.objects.create_user(username="user2", password="user2pass")

        self.book_1 = Books.objects.create(
            title="Test Book 1",
            author = "Test Author 1",
            pages = 99,
            description="Test Description 1",
            price = 333.33
        )
        self.book_2 = Books.objects.create(
            title="Test Book 2",
            author = "Test Author 2",
            pages = 199,
            description="Test Description 2",
            price = 222
        )

        self.order = OrderModel.objects.create(user=self.normal_user_1, status='Pending')
        self.order_item = OrderItemModel.objects.create(
            order=self.order,
            book=self.book_1,
            quantity=2
        )

        self.url = reverse('orders-list')
        self.url_detail = reverse('orders-detail', kwargs={'pk':self.order.pk})

    def test_admin_get_all_orders(self):
        OrderModel.objects.create(user=self.normal_user_2, status="Pending")
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_their_orders(self):
        OrderModel.objects.create(user=self.normal_user_2, status='Cancelled')
        self.client.force_authenticate(user=self.normal_user_2)
        url_list = reverse('orders-list')
        response = self.client.get(url_list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.normal_user_2.id)

    def test_create_order(self):
        self.client.force_authenticate(user=self.normal_user_1)
        data = {
            "items": [
                {"book": self.book_1.id, "quantity": 2},
                {"book": self.book_2.id, "quantity": 1}
            ],
            "status": "Pending"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_unauthorized(self):
        data = {
            "items": [
                {"book": self.book_1.id, "quantity": 2},
                {"book": self.book_2.id, "quantity": 1}
            ],
            "status": "Pending"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invalid_book(self):
        self.client.force_login(user=self.normal_user_1)
        data = {
            "items": [
                {"book": 333, "quantity": 2},
            ],
            "status": "Pending"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
