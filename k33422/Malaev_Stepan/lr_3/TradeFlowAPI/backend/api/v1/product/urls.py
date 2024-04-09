from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import (
    ProductBatchViewSet,
    ProductViewSet
)

router = DefaultRouter()
router.register(r'', ProductViewSet)

product_batches_router = NestedSimpleRouter(router, r'', lookup='product')
product_batches_router.register(r'batches', ProductBatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_batches_router.urls))
]
