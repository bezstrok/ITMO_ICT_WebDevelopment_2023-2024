from django.contrib import admin

from . import models

admin.site.register(models.Broker)
admin.site.register(models.Firm)
admin.site.register(models.Manufacturer)
admin.site.register(models.Product)
admin.site.register(models.ProductBatch)
admin.site.register(models.Trade)
