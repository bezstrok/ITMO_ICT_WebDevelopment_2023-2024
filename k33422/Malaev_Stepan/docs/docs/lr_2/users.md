# Представления для работы с пользователем

## Листинг кода

`users/views.py`

```python
from common import handlers
from django.contrib.auth import authenticate, get_user_model, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView
from tours import models as tour_models

from . import forms

User = get_user_model()


class LogoutView(LogoutView):
    next_page = reverse_lazy('home')


class RegisterView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already in use'}, status=400)
        
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)
        
        User.objects.create_user(email=email, password=password)
        
        return JsonResponse({'success': True})


class LoginView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Account is disabled'}, status=403)
        
        return JsonResponse({'error': 'Invalid credentials'}, status=400)


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/settings.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = forms.UpdateProfileForm(instance=self.request.user)
        context['password_form'] = forms.PasswordChangeForm(user=self.request.user)
        
        return context


class UpdateProfileView(LoginRequiredMixin, View):
    form_class = forms.UpdateProfileForm
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        
        error_message = handlers.handle_form_errors(form)
        
        return JsonResponse({'error': error_message}, status=400)


class ChangePasswordView(LoginRequiredMixin, View):
    form_class = forms.PasswordChangeForm
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            update_session_auth_hash(request, user)
            user.save()
            return JsonResponse({'success': True})
        
        error_message = handlers.handle_form_errors(form)
        
        return JsonResponse({'error': error_message}, status=400)


class BookingsView(LoginRequiredMixin, ListView):
    model = tour_models.Booking
    template_name = 'users/bookings.html'
    context_object_name = 'bookings'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_active:
            return self.model.objects.filter(user=user).order_by('-booking_date').select_related('tour')
        else:
            return self.objects.none()


class CancelBookingView(LoginRequiredMixin, View):
    form_class = forms.CancelBookingForm
    
    def post(self, request, *args, **kwargs):
        pk = request.POST.get('booking_id')
        booking = get_object_or_404(tour_models.Booking, pk=pk, user=request.user)
        form = self.form_class(booking=booking)
        
        try:
            form.cancel_booking(request.user)
            return JsonResponse({'success': True})
        except ValidationError as e:
            error_message = e.messages[0]
            return JsonResponse({'error': error_message}, status=400)
```

`users/urls.py`

```python
from django.urls import path

from . import views

urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('settings/update-profile/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('settings/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    path('bookings/', views.BookingsView.as_view(), name='bookings'),
    path('bookings/cancel', views.CancelBookingView.as_view(), name='cancel_booking'),
]
```

## Основные Моменты

### Регистрация и Аутентификация

- **Регистрация (`RegisterView`)**: Проверяется уникальность email и совпадение пароля с подтверждением. В случае успеха
  создается новый пользователь.
- **Аутентификация (`LoginView`)**: Проверяются учетные данные пользователя. В случае успеха пользователь входит в
  систему.

### Работа с Профилем

- **Настройки Профиля (`SettingsView`)**: Отображает формы для обновления профиля и изменения пароля.
- **Обновление Профиля (`UpdateProfileView`)**: Позволяет изменить данные профиля пользователя.
- **Изменение Пароля (`ChangePasswordView`)**: Позволяет пользователю изменить свой пароль, обновляя хэш сессии для
  предотвращения выхода из системы.

### Управление Бронированиями

- **Просмотр Бронирований (`BookingsView`)**: Показывает список бронирований пользователя с возможностью отмены.
- **Отмена Бронирования (`CancelBookingView`)**: Позволяет пользователю отменить бронирование.

## Особенности

- **Миксин `LoginRequiredMixin`**: Обеспечивает доступ к страницам только аутентифицированным пользователям.
- **AJAX-ответы**: Все действия с формами обрабатываются через AJAX, возвращая JSON-ответы, что обеспечивает более
  динамичное и современное взаимодействие с пользователем.
- **Обработка Форм**: Использование кастомных форм для обработки действий пользователя, таких как изменение профиля и
  отмена бронирований.
- **Потокобезопасность**: Использование блокировок при изменении данных пользователя для предотвращения гонок данных.