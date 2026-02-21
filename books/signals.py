from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Books
from django.core.cache import cache

@receiver([post_save, post_delete], sender=Books)
def invalidate_book_cache(sender, instance, **kwargs):
    #caches when a book is created, updated, deleted
    print("Clearing cache") 
    cache.delete_pattern('*books_list*')