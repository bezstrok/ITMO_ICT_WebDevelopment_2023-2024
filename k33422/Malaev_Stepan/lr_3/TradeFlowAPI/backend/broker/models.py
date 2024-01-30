from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from backend.utils.models import (
    AbstractTimeStampedModel,
)

User = get_user_model()


class Firm(AbstractTimeStampedModel):
    name = models.CharField(max_length=100)
    address = models.TextField()
    
    def __str__(self):
        return f"{self.name}"


class Broker(AbstractTimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profit_percentage = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    fixed_monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user}"
