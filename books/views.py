from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django.shortcuts import render
from rest_framework import generics, viewsets

from .models import Books
from .serializers import BookSerializer

from .permissions import IsAdminOrReadOnly
# Create your views here.

class BooksViewSet(viewsets.ModelViewSet):
    throttle_scope = 'books'
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    @method_decorator(cache_page(60 * 15, key_prefix='books_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()