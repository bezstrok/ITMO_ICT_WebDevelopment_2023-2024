from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = settings.AUTH_USER_MODEL


class Firm(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    
    def __str__(self):
        return f"{self.name}"
    
    @property
    def brokers_count(self):
        return self.brokers.all().count()


class Broker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="broker")
    profit_percentage = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    fixed_monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE, related_name='brokers')
    
    def __str__(self):
        return f"{self.user}"
