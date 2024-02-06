import uuid

from django.db import models

from backend.manufacturer.models import Manufacturer
from backend.utils.models import (
    AbstractTimeStampedModel,
)


class Product(AbstractTimeStampedModel):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    unique_code = models.CharField(max_length=8, unique=True, blank=True)
    category = models.CharField(max_length=100)
    weight = models.FloatField()
    production_date = models.DateField()
    expiry_date = models.DateField()
    measurement_unit = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = self.generate_unique_code()
        
        return super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now().date() > self.expiry_date
    
    @property
    def batches_count(self):
        return self.batches.all().count()
    
    def generate_unique_code(self):
        return str(uuid.uuid4())[:8]
    
    def __str__(self):
        return f"{self.name} {self.weight} {self.measurement_unit}"


class ProductBatch(AbstractTimeStampedModel):
    batch_number = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='batches')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_conditions = models.CharField(max_length=200)
    delivery_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.batch_number} {self.product}"
