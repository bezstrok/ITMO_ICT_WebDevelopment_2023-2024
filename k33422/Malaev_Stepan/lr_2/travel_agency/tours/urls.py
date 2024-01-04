from django.urls import path

from . import views

urlpatterns = [
	path('', views.TourListView.as_view(), name='explore'),
	path('<int:pk>/', views.TourDetailView.as_view(), name='tour_detail'),
	path('<int:pk>/add-review', views.AddReviewView.as_view(), name='add_review'),

]
