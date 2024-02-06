from django.db.models.functions import Now
from rest_framework import permissions

from backend.api.v1.core.permissions import (
    IsUserManufacturer,
    IsUserManufacturerObject
)
from backend.api.v1.core.viewsets import SpecificModelViewSet
from backend.api.v1.product.serializers import (
    CRUDProductSerializer,
    ListProductsSerializer,
    RetrieveProductSerializer
)
from backend.product.models import Product


class ProductViewSet(SpecificModelViewSet):
    queryset = Product.objects.select_related('manufacturer').filter(expiry_date__gte=Now())
    serializer_class = CRUDProductSerializer
    serializer_classes_by_action = {
        'retrieve': RetrieveProductSerializer,
        'list': ListProductsSerializer,
    }
    
    permission_classes_common = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        'create': [IsUserManufacturer],
        'update': [IsUserManufacturerObject],
        'partial_update': [IsUserManufacturerObject],
        'destroy': [IsUserManufacturerObject]
    }
    
    def perform_create(self, serializer):
        serializer.save(manufacturer=self.request.user.manufacturer)
