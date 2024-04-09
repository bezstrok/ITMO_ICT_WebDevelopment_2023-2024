# Работа с брокерами

## Листинг кода

`filters.py`

```python
import django_filters

from backend.broker.models import Broker


class BrokerFilter(django_filters.FilterSet):
    firm = django_filters.CharFilter(method='firm_filter')
    
    def firm_filter(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(firm__id=int(value))
        
        return queryset.filter(firm__name__icontains=value)
    
    class Meta:
        model = Broker
        fields = ()
```

`serializers.py`

```python
from django.contrib.auth import get_user_model
from rest_framework import serializers

from backend.broker.models import Broker, Firm

User = get_user_model()


class BrokerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'full_name', 'email'
        )


class RetrieveBrokerFirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = (
            'id', 'name', 'address',
            'brokers_count'
        )


class RetrieveBrokerSerializer(serializers.ModelSerializer):
    user = BrokerUserSerializer(read_only=True)
    firm = RetrieveBrokerFirmSerializer(read_only=True)
    
    class Meta:
        model = Broker
        fields = (
            'id', 'profit_percentage', 'fixed_monthly_amount',
            'user', 'firm'
        )


class CRUDBrokerSerializer(serializers.ModelSerializer):
    firm = serializers.PrimaryKeyRelatedField(queryset=Firm.objects.all())
    
    class Meta:
        model = Broker
        fields = (
            'id', 'profit_percentage', 'fixed_monthly_amount',
            'firm'
        )


class ListBrokersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    firm = serializers.SlugRelatedField(slug_field='name', read_only=True)
    
    class Meta:
        model = Broker
        fields = (
            'id', 'profit_percentage', 'fixed_monthly_amount',
            'email', 'full_name', 'firm'
        )
```

`urls.py`

```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BrokerViewSet

router = DefaultRouter()
router.register(r'', BrokerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

`views.py`

```python
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter

from backend.api.v1.broker.filters import BrokerFilter
from backend.api.v1.broker.serializers import (
    CRUDBrokerSerializer,
    ListBrokersSerializer,
    RetrieveBrokerSerializer
)
from backend.api.v1.core.mixins import ActionMeMixin
from backend.api.v1.core.permissions import IsUserRoleObject
from backend.api.v1.core.viewsets import SpecificModelViewSet
from backend.broker.models import Broker


class BrokerViewSet(ActionMeMixin, SpecificModelViewSet):
    queryset = Broker.objects.select_related('user', 'firm').all()
    
    serializer_class = CRUDBrokerSerializer
    serializer_classes_by_action = {
        'retrieve': RetrieveBrokerSerializer,
        'list': ListBrokersSerializer
    }
    
    permission_classes = [permissions.IsAuthenticated, IsUserRoleObject]
    
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = BrokerFilter
    ordering = ('fixed_monthly_amount', 'profit_percentage')
    search_fields = ('user__email',)
    
    def perform_create(self, serializer):
        if self.queryset.filter(user=self.request.user).exists():
            raise ValidationError({'detail': _('You are already broker.')})
        
        serializer.save(user=self.request.user)
```

## Основные Компоненты

### Сериализаторы

- **`BrokerUserSerializer`**: Отображает данные пользователя брокера, ассоциированного с моделью `User`.
- **`RetrieveBrokerFirmSerializer`**: Предназначен для детального отображения данных фирмы в контексте брокера.
- **`RetrieveBrokerSerializer`**: Используется для детализации информации о брокере, включая связанные данные
  пользователя и фирмы.
- **`CRUDBrokerSerializer`**: Основной сериализатор для операций создания, обновления и удаления брокеров.
- **`ListBrokersSerializer`**: Сериализатор для списка брокеров, включает электронную почту, полное имя пользователя и
  название фирмы.

### Фильтрация

- **`BrokerFilter`**: Класс фильтрации для модели `Broker`, позволяющий фильтровать брокеров по `firm`, поддерживая как
  числовые ID, так и текстовое вхождение в название фирмы.

### ViewSet

- **`BrokerViewSet`**: Настраиваемый ViewSet для брокеров, поддерживающий CRUD-операции, а также дополнительные
  настройки для фильтрации, сортировки и поиска.

## Особенности

- **Гибкость Сериализаторов**: Использование разных сериализаторов для разных действий (`retrieve`, `list`) позволяет
  оптимизировать передаваемые данные в зависимости от контекста запроса.
- **Фильтрация с `django_filters`**: Применение библиотеки `django_filters` для создания сложных фильтров, улучшает
  возможности поиска и фильтрации данных на стороне клиента.
- **Разграничение Доступа**: Внедрение системы разрешений `IsUserRoleObject`, гарантирующей, что пользователи могут
  выполнять операции только с объектами, к которым у них есть доступ.
- **Кастомная Валидация**: В `perform_create` добавлена проверка на существование брокера для пользователя,
  предотвращающая создание множественных записей брокера для одного пользователя.
