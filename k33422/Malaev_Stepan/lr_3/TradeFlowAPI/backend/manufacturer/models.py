from django.conf import settings
from django.db import models

from backend.utils.models import AbstractTimeStampedModel

User = settings.AUTH_USER_MODEL


class Manufacturer(AbstractTimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    contact_info = models.TextField()
    
    def __str__(self):
        return f"{self.user}"
