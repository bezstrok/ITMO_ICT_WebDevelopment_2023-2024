from django.contrib import admin

from .models import (
    Product,
    ProductBatch,
)

admin.site.register(Product)
admin.site.register(ProductBatch)
