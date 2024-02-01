from django.urls import path

from . import views

urlpatterns = [
    path('', views.FirmListView.as_view(), name='firm-list'),
    path('<int:pk>/', views.FirmDetailView.as_view(), name='detail-firm'),
]
