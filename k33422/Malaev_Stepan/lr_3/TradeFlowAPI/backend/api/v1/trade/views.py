from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import OrderingFilter

from backend.api.v1.core.permissions import (
    IsTradeChangeable,
    IsUserBroker,
    IsUserBrokerObject
)
from backend.api.v1.core.viewsets import SpecificModelViewSet
from backend.api.v1.trade.filters import TradeFilter
from backend.api.v1.trade.serializers import (
    CreateTradeSerializer,
    ListTradeSerializer,
    RetrieveTradeSerializer,
    UpdateDeleteTradeSerializer
)
from backend.trade.models import Trade


class TradeViewSet(SpecificModelViewSet):
    queryset = Trade.objects.select_related('broker', 'product_batch').all()
    
    serializer_class = UpdateDeleteTradeSerializer
    serializer_classes_by_action = {
        'retrieve': RetrieveTradeSerializer,
        'list': ListTradeSerializer,
        'create': CreateTradeSerializer
    }
    
    permission_classes_common = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        'create': [IsUserBroker],
        'update': [IsUserBrokerObject, IsTradeChangeable],
        'partial_update': [IsUserBrokerObject, IsTradeChangeable],
        'destroy': [IsUserBrokerObject],
    }
    
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = TradeFilter
    ordering = ('product_batch', 'status', 'broker', 'id')
    
    def perform_create(self, serializer):
        serializer.save(broker=self.request.user.broker)
