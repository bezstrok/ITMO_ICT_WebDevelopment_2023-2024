from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .tours import Tour

User = get_user_model()


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tour} - {self.rating}"
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'tour']),
        ]
