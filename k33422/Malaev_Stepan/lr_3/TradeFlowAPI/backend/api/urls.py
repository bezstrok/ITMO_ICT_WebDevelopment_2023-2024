from django.urls import include, path

urlpatterns = [
    path('v1/', include('backend.api.v1.urls', namespace='v1'))
]
