from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

from .tours import Tour

User = get_user_model()


class Booking(models.Model):
	STATUS_CHOICES = (
		('pending', 'Pending'),
		('confirmed', 'Confirmed'),
		('cancelled', 'Cancelled'),
	)
	
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
	tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings')
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
	booking_date = models.DateTimeField(auto_now_add=True)
	
	def clean(self):
		if self.booking_date and self.booking_date < timezone.now():
			raise ValidationError("Booking date cannot be in the past.")
		
		if self.booking_date > self.tour.start_date:
			raise ValidationError("Booking cannot be made after the tour start date.")
	
	def save(self, *args, **kwargs):
		self.clean()
		super().save(*args, **kwargs)
	
	def cancel(self):
		with transaction.atomic():
			if self.status == 'confirmed':
				self.status = 'cancelled'
				self.save()
			else:
				raise ValidationError("Only confirmed bookings can be cancelled.")
	
	def confirm(self):
		with transaction.atomic():
			if self.status == 'pending':
				self.status = 'confirmed'
				self.save()
			else:
				raise ValidationError("Only pending bookings can be confirmed.")
	
	def __str__(self):
		return f'{self.user} - {self.tour}'
	
	class Meta:
		indexes = [
			models.Index(fields=['user', 'tour']),
		]
