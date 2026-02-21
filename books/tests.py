from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from .models import Books

from users.models import CustomUser

# Create your tests here.
class BooksAPITestCase(APITestCase):
    #code that will run before each test case
    def setUp(self):
        self.admin_user = CustomUser.objects.create_superuser(username="admin", password="adminpass")
        self.normal_user = CustomUser.objects.create_user(username="user", password="userpass")
        self.book = Books.objects.create(
            title="Test Book",
            author = "Test Author",
            pages = 99,
            description="Test Description",
            price = 333.33
        )
        self.url = reverse('books-detail', kwargs={'pk': self.book.pk})

    def test_get_book(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #make sure we are getting the right objects. title field is the part of data that will be returned in that response
        self.assertEqual(response.data['title'], self.book.title) 
    
    #by default request comes from anonymus user
    def test_unauthorized_update_book(self):
        data = {'title': 'Updated Title'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_book(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_admin_can_delete_book(self):
        #test normal user
        self.client.login(username="user", password="userpass")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Books.objects.filter(pk=self.book.pk).exists())
        #test admin user
        self.client.login(username="admin", password="adminpass")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Books.objects.filter(pk=self.book.pk).exists())