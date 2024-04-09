from django.urls import path

from . import views

urlpatterns = [
	path('drivers/', views.all_drivers),
	path('drivers/<int:id_driver>/', views.driver_detail),
	#  path('drivers/create/', views.driver_create),
	path('drivers/create/', views.driver_register),
	path('cars/', views.CarListView.as_view()),
	path('cars/<int:pk>/', views.CarDetailView.as_view()),
	path('cars/update/<int:pk>/', views.CarUpdateView.as_view()),
	path('cars/delete/<int:pk>/', views.CarDeleteView.as_view()),
	path('cars/create/', views.CarCreateView.as_view())
]
