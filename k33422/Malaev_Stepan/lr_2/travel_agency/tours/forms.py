from django import forms

from . import models


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['comment', 'rating']


class BookingForm(forms.ModelForm):
    class Meta:
        model = models.Booking
        fields = []
