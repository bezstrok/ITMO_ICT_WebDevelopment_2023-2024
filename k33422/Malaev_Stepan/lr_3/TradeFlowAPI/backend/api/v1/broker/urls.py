from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BrokerViewSet

router = DefaultRouter()
router.register(r'', BrokerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
