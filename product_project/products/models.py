# products/models.py
from django.db import models
from django.utils import timezone

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    retrieval_count = models.PositiveIntegerField(default=0)
    retrieved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def retrieve(self):
        self.retrieval_count += 1
        self.retrieved_at = timezone.now()
        self.save()
