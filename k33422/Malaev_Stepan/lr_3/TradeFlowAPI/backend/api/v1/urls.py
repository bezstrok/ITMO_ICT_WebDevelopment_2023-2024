from django.urls import include, path

urlpatterns = [
    path('auth/', include('backend.api.v1.user.urls')),
    path('brokers/', include('backend.api.v1.broker.urls')),
    path('firms/', include('backend.api.v1.firm.urls')),
    path('manufacturers/', include('backend.api.v1.manufacturer.urls')),
    path('products/', include('backend.api.v1.product.urls')),
]
