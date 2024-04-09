import django_filters

from backend.broker.models import Broker


class BrokerFilter(django_filters.FilterSet):
    firm = django_filters.CharFilter(method='firm_filter')
    
    def firm_filter(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(firm__id=int(value))
        
        return queryset.filter(firm__name__icontains=value)
    
    class Meta:
        model = Broker
        fields = ()
