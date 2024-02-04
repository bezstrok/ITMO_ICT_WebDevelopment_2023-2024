from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ManufacturerViewSet

router = DefaultRouter()
router.register(r'', ManufacturerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
