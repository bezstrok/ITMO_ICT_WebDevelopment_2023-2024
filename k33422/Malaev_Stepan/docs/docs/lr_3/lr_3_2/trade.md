# Работа с трейдами

`filters.py`

```python
import django_filters
from backend.trade.models import Trade
from django.db.models import Q


class TradeFilter(django_filters.FilterSet):
  broker = django_filters.CharFilter(method='filter_broker')
  product_batch__product = django_filters.CharFilter(method='filter_product')
  product_batch = django_filters.NumberFilter(field_name='product_batch__id')
  status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')

  def filter_broker(self, queryset, name, value):
    if value.isdigit():
      return queryset.filter(broker__id=int(value))

    return queryset.filter(broker__user__email__icontains=value)

  def filter_product(self, queryset, name, value):
    if value.isdigit():
      return queryset.filter(product_batch__product__id=int(value))

    return queryset.filter(
      Q(product_batch__product__name__icontains=value) |
      Q(product_batch__product__unique_code__iexact=value)
    )

  class Meta:
    model = Trade
    fields = ()
```

`serializers.py`

```python
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from backend.broker.models import Broker
from backend.product.models import Product, ProductBatch
from backend.trade.models import Trade


class TradeProductBatchProductSerializer(serializers.ModelSerializer):
    manufacturer = serializers.SlugRelatedField(slug_field='firm_name', read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'unique_code',
            'category', 'manufacturer'
        )


class TradeProductBatchSerializer(serializers.ModelSerializer):
    product = TradeProductBatchProductSerializer(read_only=True)
    
    class Meta:
        model = ProductBatch
        fields = (
            'id', 'product', 'quantity',
            'price', 'delivery_conditions'
        )


class TradeBrokerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    firm = serializers.SlugRelatedField(slug_field='name', read_only=True)
    
    class Meta:
        model = Broker
        fields = (
            'id', 'email', 'full_name',
            'firm', 'trades_conducted_count'
        )


class RetrieveTradeSerializer(serializers.ModelSerializer):
    broker = TradeBrokerSerializer(read_only=True)
    product_batch = TradeProductBatchSerializer(read_only=True)
    
    class Meta:
        model = Trade
        fields = (
            'id', 'start_time', 'end_time',
            'status', 'total_amount', 'broker',
            'product_batch'
        )


class ListTradeSerializer(serializers.ModelSerializer):
    broker = serializers.CharField(source='broker.user.full_name', read_only=True)
    product = serializers.CharField(source='product_batch.product.name', read_only=True)
    quantity = serializers.IntegerField(source='product_batch.quantity', read_only=True)
    
    class Meta:
        model = Trade
        fields = (
            'id', 'start_time', 'end_time',
            'status', 'total_amount', 'broker',
            'product', 'quantity'
        )


class UpdateDeleteTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            'id', 'status', 'total_amount'
        )


class CreateTradeSerializer(serializers.ModelSerializer):
    product_batch = serializers.PrimaryKeyRelatedField(queryset=ProductBatch.objects.all())
    
    class Meta:
        model = Trade
        fields = (
            'id', 'total_amount', 'product_batch'
        )
    
    def validate_product_batch(self, value):
        if not value.is_available:
            raise ValidationError(_('The selected product batch is not available for trading.'))
        return value
```

`urls.py`

```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TradeViewSet

router = DefaultRouter()
router.register(r'', TradeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

`views.py`

```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import OrderingFilter

from backend.api.v1.core.permissions import (
    IsTradeChangeable,
    IsUserBroker,
    IsUserBrokerObject
)
from backend.api.v1.core.viewsets import SpecificModelViewSet
from backend.api.v1.trade.filters import TradeFilter
from backend.api.v1.trade.serializers import (
    CreateTradeSerializer,
    ListTradeSerializer,
    RetrieveTradeSerializer,
    UpdateDeleteTradeSerializer
)
from backend.trade.models import Trade


class TradeViewSet(SpecificModelViewSet):
    queryset = Trade.objects.select_related('broker', 'product_batch').all()
    
    serializer_class = UpdateDeleteTradeSerializer
    serializer_classes_by_action = {
        'retrieve': RetrieveTradeSerializer,
        'list': ListTradeSerializer,
        'create': CreateTradeSerializer
    }
    
    permission_classes_common = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        'create': [IsUserBroker],
        'update': [IsUserBrokerObject, IsTradeChangeable],
        'partial_update': [IsUserBrokerObject, IsTradeChangeable],
        'destroy': [IsUserBrokerObject],
    }
    
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = TradeFilter
    ordering = ('product_batch', 'status', 'broker', 'id')
    
    def perform_create(self, serializer):
        serializer.save(broker=self.request.user.broker)
```

## Основные Компоненты

### Сериализаторы

- **`RetrieveTradeSerializer`**: Детализирует информацию о трейде, включая связанные данные брокера и партии продукта.
- **`ListTradeSerializer`**: Предоставляет список трейдов с основной информацией для обзора.
- **`CreateTradeSerializer`**: Используется для создания новых трейдов с проверкой доступности выбранной партии
  продукта.
- **`UpdateDeleteTradeSerializer`**: Предназначен для обновления и удаления трейдов.

### Фильтры

- **`TradeFilter`**: Класс фильтрации для модели `Trade`, позволяющий осуществлять поиск трейдов по брокеру, продукту,
  статусу и другим параметрам.

### ViewSet

- **`TradeViewSet`**: Настроенный ViewSet, обрабатывающий CRUD операции для трейдов, с расширенной логикой разрешений и
  фильтрацией.

## Особенности

- **Валидация Доступности Партии Продукта**: В `CreateTradeSerializer` реализована кастомная валидация, которая
  проверяет доступность выбранной партии продукта для торговли, предотвращая создание трейдов с недоступными партиями.
- **Разграничение Доступа**: В ViewSet применяются различные классы разрешений для контроля доступа к операциям в
  зависимости от роли пользователя и состояния трейда.
- **Гибкая Фильтрация**: Использование `TradeFilter` с кастомными методами фильтрации обеспечивает удобный поиск трейдов
  по сложным критериям.
- **Выборочное Применение Сериализаторов**: Применение разных сериализаторов для различных
  действий (`retrieve`, `list`, `create`) позволяет оптимизировать передаваемые и получаемые данные.
