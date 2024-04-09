from django.contrib import admin

from .models import (
    Broker,
    Firm,
)

admin.site.register(Firm)
admin.site.register(Broker)
