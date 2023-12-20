from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
	username = None
	
	email = models.EmailField(_("email address"), unique=True)
	
	first_name = models.CharField(_("first name"), max_length=150, null=True, blank=True)
	last_name = models.CharField(_("last name"), max_length=150, null=True, blank=True)
	middle_name = models.CharField(_("middle name"), max_length=150, null=True, blank=True)
	
	date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
	
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = []
	
	@property
	def full_name(self):
		return f"{self.first_name} {self.last_name}"
	
	def __str__(self):
		return f"{self.full_name} {self.email}"
