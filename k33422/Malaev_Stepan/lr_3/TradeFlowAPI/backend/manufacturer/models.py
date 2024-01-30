from django.contrib.auth import get_user_model
from django.db import models

from backend.utils.models import (
    AbstractTimeStampedModel,
)

User = get_user_model()


class Manufacturer(AbstractTimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    contact_info = models.TextField()
    
    def __str__(self):
        return f"{self.user}"
