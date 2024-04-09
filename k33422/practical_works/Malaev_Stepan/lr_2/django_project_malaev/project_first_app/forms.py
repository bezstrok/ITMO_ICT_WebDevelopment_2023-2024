from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


# from .models import Driver


# class DriverForm(forms.ModelForm):
# 	class Meta:
# 		model = Driver
# 		fields = [
# 			"first_name",
# 			"last_name",
# 			"birth_date"
# 		]


class DriverUserCreationForm(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = (
			'username', 'email', 'first_name', 'last_name', 'birth_date', 'passport_number', 'home_address',
			'nationality'
		)
