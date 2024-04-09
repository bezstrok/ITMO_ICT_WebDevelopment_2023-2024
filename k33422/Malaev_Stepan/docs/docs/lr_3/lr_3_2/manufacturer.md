# Работа с производителями

`serializers.py`

```python
from backend.manufacturer.models import Manufacturer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ManufacturerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'full_name', 'email'
        )


class RetrieveManufacturerSerializer(serializers.ModelSerializer):
    user = ManufacturerUserSerializer(read_only=True)
    
    class Meta:
        model = Manufacturer
        fields = (
            'id', 'firm_name', 'address',
            'contact_info', 'user', 'products_count'
        )


class ListManufacturerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Manufacturer
        fields = (
            'id', 'firm_name', 'address',
            'contact_info', 'email', 'full_name',
            'products_count'
        )


class CRUDManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = (
            'id', 'firm_name', 'address',
            'contact_info'
        )
```

`urls.py`

```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ManufacturerViewSet

router = DefaultRouter()
router.register(r'', ManufacturerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

`views.py`

```python
from backend.api.v1.core.mixins import ActionMeMixin
from backend.api.v1.core.permissions import IsUserRoleObject
from backend.api.v1.core.viewsets import SpecificModelViewSet
from backend.api.v1.manufacturer.serializers import (
    CRUDManufacturerSerializer,
    ListManufacturerSerializer,
    RetrieveManufacturerSerializer
)
from backend.manufacturer.models import Manufacturer
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter


class ManufacturerViewSet(ActionMeMixin, SpecificModelViewSet):
    queryset = Manufacturer.objects.select_related('user').all()
    
    serializer_class = CRUDManufacturerSerializer
    serializer_classes_by_action = {
        'retrieve': RetrieveManufacturerSerializer,
        'list': ListManufacturerSerializer,
    }
    
    permission_classes = [permissions.IsAuthenticated, IsUserRoleObject]
    
    filter_backends = (OrderingFilter, SearchFilter)
    ordering = ('firm_name',)
    search_fields = ('firm_name', 'user__email')
    
    def perform_create(self, serializer):
        if self.queryset.filter(user=self.request.user).exists():
            raise ValidationError({'detail': _('You are already manufacturer.')})
        
        serializer.save(user=self.request.user)
```

## Основные Компоненты

### Сериализаторы

- **`ManufacturerUserSerializer`**: Отображает информацию о пользователе, связанном с производителем, включая
  идентификатор, полное имя и электронную почту.
- **`RetrieveManufacturerSerializer`**: Используется для детального представления производителя, включая связанные
  данные пользователя.
- **`ListManufacturerSerializer`**: Предназначен для сериализации списка производителей, предоставляя основную
  информацию о каждом, включая количество связанных продуктов.
- **`CRUDManufacturerSerializer`**: Основной сериализатор для операций создания, обновления и удаления данных о
  производителях.

### ViewSet

- **`ManufacturerViewSet`**: Настроенный ViewSet, который обрабатывает различные HTTP-запросы (GET, POST, PUT, DELETE),
  применяя соответствующие сериализаторы в зависимости от действия.

### Маршрутизация

- Использование `DefaultRouter` из DRF для автоматического создания URL-путей для всех операций, поддерживаемых ViewSet.

### Фильтрация, Сортировка и Поиск

- Применение фильтров `OrderingFilter` и `SearchFilter` для сортировки и поиска среди производителей по названию фирмы и
  электронной почте пользователя.

## Особенности

- **Разделение Сериализаторов по Действиям**: Интеллектуальное использование различных сериализаторов для операций
  чтения и обновления данных улучшает безопасность и контроль над тем, какая информация предоставляется пользователям
  API.
- **Интеграция Данных Пользователя**: Связывание информации о пользователе с данными производителя обеспечивает более
  глубокую интеграцию внутри системы и упрощает управление доступом.
- **Ограничение Создания Дубликатов**: Метод `perform_create` включает проверку на существование записи производителя
  для пользователя, предотвращая повторное создание производителей одним и тем же пользователем.
- **Доступ Только для Аутентифицированных Пользователей**: Ограничение доступа к API с
  помощью `permissions.IsAuthenticated` и `IsUserRoleObject` повышает безопасность данных.
