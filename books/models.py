from django.db import models

# Create your models here.
class Books(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    pages = models.IntegerField()
    description = models.TextField(blank=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'books_table' #table name

    def __str__(self):
        return self.title