from django.db.models.functions import Now
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from backend.api.v1.core.permissions import (IsProductBatchAvailable, IsUserManufacturer,
                                             IsUserManufacturerNestedProduct, IsUserManufacturerObject)
from backend.api.v1.core.viewsets import SpecificModelViewSet
from backend.api.v1.product.filters import ProductBatchFilter, ProductFilter
from backend.api.v1.product.serializers import (CRUDProductBatchSerializer, CRUDProductSerializer,
                                                ListProductBatchSerializer,
                                                ListProductsSerializer, RetrieveProductBatchSerializer,
                                                RetrieveProductSerializer)
from backend.product.models import (
    Product,
    ProductBatch
)


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
    
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = ProductFilter
    ordering = ('expiry_date', 'expiry_date', 'weight', 'name', 'id')
    search_fields = ('^name', '=unique_code')
    
    def perform_create(self, serializer):
        serializer.save(manufacturer=self.request.user.manufacturer)


class ProductBatchViewSet(SpecificModelViewSet):
    queryset = ProductBatch.objects.all()
    
    serializer_class = CRUDProductBatchSerializer
    serializer_classes_by_action = {
        'retrieve': RetrieveProductBatchSerializer,
        'list': ListProductBatchSerializer,
    }
    
    permission_classes_common = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        'create': [IsUserManufacturerNestedProduct],
        'update': [IsUserManufacturerNestedProduct, IsProductBatchAvailable],
        'partial_update': [IsUserManufacturerNestedProduct, IsProductBatchAvailable],
        'destroy': [IsUserManufacturerNestedProduct, IsProductBatchAvailable]
    }
    
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductBatchFilter
    ordering = ('price', 'quantity', 'id')
    
    def get_queryset(self):
        return super().get_queryset().filter(product=self.get_product())
    
    def get_product(self):
        return get_object_or_404(Product, pk=self.kwargs.get('product_pk'))
    
    def perform_create(self, serializer):
        serializer.save(product=self.get_product())
