import django_filters
from django.db.models import Q

from backend.trade.models import Trade


class TradeFilter(django_filters.FilterSet):
    broker = django_filters.CharFilter(method='filter_broker')
    product = django_filters.CharFilter(method='filter_product')
    product_batch = django_filters.NumberFilter(field_name='product_batch__id', lookup_expr='exact')
    
    def filter_broker(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(broker__id=int(value))
        
        return queryset.filter(
            Q(broker__user__first_name__icontains=value) |
            Q(broker__user__last_name__icontains=value) |
            Q(broker__user__email__icontains=value)
        )
    
    def filter_product(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(product_batch__product__id=int(value))
        
        return queryset.filter(
            Q(product_batch__product__name__icontains=value) |
            Q(product_batch__product__unique_code__iexact=value)
        )
    
    class Meta:
        model = Trade
        fields = ()
