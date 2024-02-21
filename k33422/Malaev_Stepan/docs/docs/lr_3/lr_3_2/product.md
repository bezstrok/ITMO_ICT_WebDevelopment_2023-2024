# Работа с продуктами

`filters.py`

```python
import django_filters
from backend.product.choices import TradeStatus
from backend.product.models import Product, ProductBatch
from django.db.models import Q


class ProductFilter(django_filters.FilterSet):
    manufacturer = django_filters.CharFilter(method='filter_manufacturer')
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    
    def filter_manufacturer(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(manufacturer__id=int(value))
        
        return queryset.filter(
            Q(manufacturer__firm_name__icontains=value) |
            Q(manufacturer__user__email__icontains=value)
        )
    
    class Meta:
        model = Product
        fields = ()


class ProductBatchFilter(django_filters.FilterSet):
    is_available = django_filters.BooleanFilter(method='filter_is_available')
    
    def filter_is_available(self, queryset, name, value):
        if value:
            return queryset.exclude(trades__status__in=TradeStatus.unavailable())
        
        return queryset.filter(trades__status__in=TradeStatus.unavailable())
    
    class Meta:
        model = ProductBatch
        fields = ()
```

`serializers.py`

```python
from backend.manufacturer.models import Manufacturer
from backend.product.models import (
    Product,
    ProductBatch
)
from backend.trade.models import Trade
from rest_framework import serializers


class ProductManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = (
            'id', 'firm_name', 'products_count'
        )


class ProductProductBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBatch
        fields = (
            'id', 'quantity', 'price'
        )


class RetrieveProductSerializer(serializers.ModelSerializer):
    manufacturer = ProductManufacturerSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name',
            'unique_code', 'category', 'weight',
            'production_date', 'expiry_date', 'measurement_unit',
            'manufacturer', 'batches_count'
        )


class ListProductsSerializer(serializers.ModelSerializer):
    manufacturer = serializers.SlugRelatedField(slug_field='firm_name', read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'unique_code',
            'category', 'weight', 'production_date',
            'expiry_date', 'measurement_unit', 'manufacturer',
            'batches_count',
        )


class CRUDProductSerializer(serializers.ModelSerializer):
    manufacturer = serializers.SlugRelatedField(slug_field='firm_name', read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'unique_code',
            'category', 'weight', 'production_date',
            'expiry_date', 'measurement_unit', 'manufacturer'
        )
        read_only_fields = ('unique_code',)


class ListProductBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBatch
        fields = (
            'id', 'quantity', 'price',
            'delivery_conditions', 'trades_count', 'is_available'
        )


class ProductBatchTradesSerializer(serializers.ModelSerializer):
    broker = serializers.CharField(source='broker.user.full_name', read_only=True)
    
    class Meta:
        model = Trade
        fields = (
            'id', 'start_time', 'end_time',
            'status', 'broker'
        )


class RetrieveProductBatchSerializer(serializers.ModelSerializer):
    trades = ProductBatchTradesSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductBatch
        fields = (
            'id', 'quantity', 'price',
            'delivery_conditions', 'trades_count', 'trades',
            'is_available'
        )


class CRUDProductBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBatch
        fields = (
            'id', 'quantity', 'price',
            'delivery_conditions'
        )
```

`urls.py`

```python
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
```

`views.py`

```python
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
from django.db.models.functions import Now
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter


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
    search_fields = ('name', '=unique_code')
    
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
```

## Основные Компоненты

### Сериализаторы

- **Продукты**: Различные сериализаторы (`ListProductsSerializer`, `RetrieveProductSerializer`, `CRUDProductSerializer`)
  предоставляют гибкость в представлении данных о продуктах, от простого списка до детального представления с
  интеграцией данных производителей.
- **Партии Продуктов**: Аналогично, для партий продуктов реализованы
  сериализаторы (`ListProductBatchSerializer`, `RetrieveProductBatchSerializer`, `CRUDProductBatchSerializer`),
  позволяющие управлять данными о партиях, включая связанные торговые операции.

### Фильтры

- **`ProductFilter` и `ProductBatchFilter`**: Использование классов фильтрации позволяет эффективно осуществлять поиск и
  фильтрацию продуктов и партий продуктов по различным критериям, улучшая пользовательский опыт.

### ViewSets

- **`ProductViewSet` и `ProductBatchViewSet`**: Реализация ViewSets с поддержкой специфичных для действий сериализаторов
  и наборов разрешений обеспечивает гибкое управление доступом и представлением данных.

### Маршрутизация

- Использование `DefaultRouter` и `NestedSimpleRouter` для создания RESTful URL-путей, поддерживающих вложенные ресурсы,
  позволяет легко навигировать по API.

## Особенности

- **Вложенные Ресурсы**: Реализация вложенности ресурсов `ProductBatch` в `Product` через `NestedSimpleRouter`
  демонстрирует продвинутые возможности маршрутизации в DRF.
- **Кастомная Фильтрация**: Разработка кастомных методов фильтрации для обработки сложных запросов, таких как поиск по
  атрибутам связанных моделей.
- **Ограничение Доступа**: Подробно настроенные разрешения для различных действий с продуктами и партиями продуктов
  гарантируют безопасность и соответствие ролям пользователей.
- **Автоматическая Фильтрация по Срокам Годности**: `ProductViewSet` автоматически фильтрует продукты, исключая те, чей
  срок годности истек, что повышает актуальность представляемой информации.
