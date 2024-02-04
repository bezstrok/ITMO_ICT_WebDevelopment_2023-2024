from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Manufacturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    contact_info = models.TextField()
    
    @property
    def products_count(self):
        return self.products.all().count()
    
    def __str__(self):
        return f"{self.user}"
