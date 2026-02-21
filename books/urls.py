from django.urls import path, include

from rest_framework import routers

from .views import BooksViewSet

books_router = routers.DefaultRouter()
books_router.register(r'books', BooksViewSet)

urlpatterns = [
    path('', include(books_router.urls), name='book-detail')
]