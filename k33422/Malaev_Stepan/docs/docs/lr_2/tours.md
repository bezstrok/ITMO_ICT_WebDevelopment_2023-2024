# Представления для работы с турами

## Листинг кода

`tours/views.py`

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView

from . import forms, mixins, models


class TourListView(ListView):
    model = models.Tour
    paginate_by = 5
    template_name = 'tours/explore.html'
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(start_date__gt=timezone.localdate())
        
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(country__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        queryset = queryset.order_by('country')
        
        return queryset


class TourDetailView(DetailView):
    model = models.Tour
    template_name = 'tours/tour_detail.html'


class AddReviewView(LoginRequiredMixin, mixins.CreateObjectMixin, View):
    form_class = forms.ReviewForm
    model = models.Tour
    related_name = 'tour'


class AddBookingView(LoginRequiredMixin, mixins.CreateObjectMixin, View):
    form_class = forms.BookingForm
    model = models.Tour
    related_name = 'tour'
```

`tours/urls.py`

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.TourListView.as_view(), name='explore'),
    path('<int:pk>/', views.TourDetailView.as_view(), name='tour_detail'),
    path('<int:pk>/add-review', views.AddReviewView.as_view(), name='add_review'),
    path('<int:pk>/book', views.AddBookingView.as_view(), name='add_booking'),
]
```

## Основные Моменты

### Список Туров (`TourListView`)

- **Фильтрация и Поиск**: Реализована фильтрация туров по дате начала и поиск по названию, стране и описанию с
  использованием `Q`-объектов для составных запросов.
- **Пагинация**: Добавлена пагинация для удобства просмотра списка туров, установлено ограничение в 5 туров на страницу.

### Детальный Просмотр Тура (`TourDetailView`)

- **Представление Деталей**: Предоставляет полную информацию о туре, включая описание, дату начала и другие параметры.

### Добавление Отзыва (`AddReviewView`)

- **Ограничение Доступа**: Доступ к функции добавления отзывов ограничен авторизованными пользователями с
  помощью `LoginRequiredMixin`.
- **Использование Миксинов**: Применены собственные миксины для обобщения логики создания связанных объектов, упрощая
  добавление отзывов к турам.

### Бронирование Тура (`AddBookingView`)

- **Форма Бронирования**: Интегрирована форма для бронирования тура, доступная только для авторизованных пользователей.
- **Создание Связанных Объектов**: Аналогично добавлению отзыва, используется механизм миксинов для упрощения процесса
  бронирования.

## Особенности

- **Миксины для Создания Объектов**: Разработка собственных миксинов для повторного использования логики создания
  объектов снижает дублирование кода и улучшает его читаемость.
- **Гибкая Система Поиска**: Использование `Q`-объектов для реализации поиска по нескольким полям модели `Tour`
  обеспечивает гибкость и мощные возможности фильтрации данных.
- **Защита Доступа**: Применение `LoginRequiredMixin` для ограничения доступа к определенным действиям повышает
  безопасность приложения.
- **Улучшенный Пользовательский Опыт**: Пагинация списка туров и динамический поиск значительно улучшают
  пользовательский опыт, делая интерфейс приложения более дружелюбным.

