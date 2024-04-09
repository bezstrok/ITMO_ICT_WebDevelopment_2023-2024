import django_filters
from django.db.models import Q

from backend.product.choices import TradeStatus
from backend.product.models import Product, ProductBatch


class ProductFilter(django_filters.FilterSet):
    manufacturer = django_filters.CharFilter(method='filter_manufacturer')
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    
    def filter_manufacturer(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(manufacturer__id=int(value))
        
        return queryset.filter(
            Q(manufacturer__firm_name__icontains=value) |
            Q(manufacturer__user__email__icontains=value)
        )
    
    class Meta:
        model = Product
        fields = ()


class ProductBatchFilter(django_filters.FilterSet):
    is_available = django_filters.BooleanFilter(method='filter_is_available')
    
    def filter_is_available(self, queryset, name, value):
        if value:
            return queryset.exclude(trades__status__in=TradeStatus.unavailable())
        
        return queryset.filter(trades__status__in=TradeStatus.unavailable())
    
    class Meta:
        model = ProductBatch
        fields = ()
