from django.urls import path

from . import views

urlpatterns = [
	path('logout/', views.LogoutView.as_view(), name='logout'),
	path('login/', views.LoginView.as_view(), name='login'),
	path('register/', views.RegisterView.as_view(), name='register'),
	
	path('settings/', views.SettingsView.as_view(), name='settings'),
	path('settings/update-profile/', views.UpdateProfileView.as_view(), name='update_profile'),
	path('settings/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
