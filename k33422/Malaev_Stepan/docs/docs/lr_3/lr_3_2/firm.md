# Работа с фирмами

`serializers.py`

```python
from backend.broker.models import Broker, Firm
from rest_framework import serializers


class FirmBrokerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Broker
        fields = (
            'id', 'profit_percentage', 'fixed_monthly_amount',
            'email', 'full_name'
        )


class FirmDetailSerializer(serializers.ModelSerializer):
    brokers = FirmBrokerSerializer(read_only=True, many=True)
    
    class Meta:
        model = Firm
        fields = (
            'id', 'name', 'address',
            'brokers_count', 'brokers'
        )


class FirmListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = (
            'id', 'name', 'address',
            'brokers_count'
        )
```

`urls.py`

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.FirmListView.as_view(), name='firm-list'),
    path('<int:pk>/', views.FirmDetailView.as_view(), name='detail-firm'),
]
```

`views.py`

```python
from backend.broker.models import Firm
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from .serializers import FirmDetailSerializer, FirmListSerializer


class FirmDetailView(generics.RetrieveAPIView):
    queryset = Firm.objects.prefetch_related('brokers').all()
    
    serializer_class = FirmDetailSerializer
    
    permission_classes = [permissions.IsAuthenticated]


class FirmListView(generics.ListAPIView):
    queryset = Firm.objects.all()
    
    serializer_class = FirmListSerializer
    
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = (OrderingFilter, SearchFilter)
    ordering = ('name',)
    search_fields = ('name',)
```

## Основные Компоненты

### Сериализаторы

- **`FirmListSerializer`**: Используется для сериализации списка фирм, предоставляя основную информацию о каждой фирме.
- **`FirmDetailSerializer`**: Предоставляет детальную информацию о фирме, включая список брокеров, ассоциированных с
  фирмой, с их email и полным именем.
- **`FirmBrokerSerializer`**: Сериализатор для представления данных брокера в контексте фирмы.

### Views

- **`FirmListView`**: Отображает список всех фирм, поддерживая фильтрацию и сортировку.
- **`FirmDetailView`**: Предоставляет детальную информацию о фирме, включая связанных брокеров.

### URL-пути

- Определены URL-пути для доступа к списку фирм и детальной информации о фирме, обеспечивая легкость в интеграции с
  фронтендом.

## Особенности

- **Предварительная Загрузка данных (`prefetch_related`)**: Использование метода `prefetch_related` в `FirmDetailView`
  для оптимизации запросов к базе данных при получении информации о фирме и связанных с ней брокерах.
- **Фильтрация и Сортировка**: Включение возможности фильтрации и сортировки в `FirmListView` позволяет пользователям
  эффективно навигировать по списку фирм.
- **Доступность только для Аутентифицированных Пользователей**: Ограничение доступа к API только для аутентифицированных
  пользователей через `permissions.IsAuthenticated` повышает безопасность данных.
