from django.contrib.auth import get_user_model
from django.db import models

from .audit import TimeStampedModel

User = get_user_model()


class Manufacturer(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    contact_info = models.TextField()
    
    def __str__(self):
        return f"{self.user}"
