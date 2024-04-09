from django.contrib import admin

from . import models

admin.site.register(models.Agency)
admin.site.register(models.Tour)
admin.site.register(models.Booking)
admin.site.register(models.Review)
admin.site.register(models.TourImage)
