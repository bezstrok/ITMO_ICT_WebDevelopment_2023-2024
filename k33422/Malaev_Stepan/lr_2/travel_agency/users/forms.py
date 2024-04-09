from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

User = get_user_model()


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'date_of_birth']


class PasswordChangeForm(PasswordChangeForm):
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("The two password fields didn't match.")
        
        return password2


class CancelBookingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.booking = kwargs.pop('booking', None)
        super().__init__(*args, **kwargs)
    
    def cancel_booking(self, user):
        if self.booking.user != user:
            raise ValidationError("You do not have permission to cancel this booking.")
        self.booking.cancel()
