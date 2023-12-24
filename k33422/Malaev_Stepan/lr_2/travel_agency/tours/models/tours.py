from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Agency(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	contacts = models.JSONField(default=dict)
	
	def __str__(self):
		return f"{self.name}"


class Tour(models.Model):
	name = models.CharField(max_length=200)
	agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
	description = models.TextField()
	start_date = models.DateField()
	end_date = models.DateField()
	payment_conditions = models.JSONField(default=dict)
	
	def clean(self):
		if self.start_date > self.end_date:
			raise ValidationError("Start date must be before end date")
	
	def save(self, *args, **kwargs):
		self.clean()
		super().save(*args, **kwargs)
	
	@property
	def duration(self):
		return (self.end_date - self.start_date).days + 1
	
	def is_available(self):
		return self.start_date > timezone.localdate()
	
	def __str__(self):
		return f"{self.name}"
