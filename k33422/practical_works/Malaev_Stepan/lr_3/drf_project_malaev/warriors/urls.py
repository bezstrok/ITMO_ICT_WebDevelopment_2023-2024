from django.urls import path
from warriors_app import views

urlpatterns = [
    path('warrior/', views.WarriorAPIView.as_view(), name='warriors'),
    path('warrior_auth_only/', views.WarriorAuthenticatedOnly.as_view()),
    path('warrior_profession', views.WarriorWithProfessionView.as_view()),
    path('warrior_skill', views.WarriorWithSkillView.as_view()),
    path('warrior_generic_create', views.WarriorCreateApiView.as_view()),
    path('warrior/<int:pk>/', views.WarriorRetrieveApiView.as_view()),
    path('warrior/retriev_update_destroy/<int:pk>/', views.WarriorRetrieveUpdateDestroyApiView.as_view()),
    path('profession/', views.ProfessionApiView.as_view()),
    path('profession/create/', views.ProfessionCreateView.as_view(), name='profession_create'),
    path('skill/', views.SkillApiView.as_view()),
    path('skill/create', views.SkillCreateView.as_view()),
    path('skill_with_warrior/', views.SkillWithWarrior.as_view(), name='skill_related')
]