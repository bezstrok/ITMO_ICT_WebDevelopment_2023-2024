from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter

from backend.api.v1.broker.filters import BrokerFilter
from backend.api.v1.broker.serializers import (
    CRUDBrokerSerializer,
    ListBrokersSerializer,
    RetrieveBrokerSerializer
)
from backend.api.v1.core.mixins import ActionMeMixin
from backend.api.v1.core.permissions import IsUserRoleObject
from backend.api.v1.core.viewsets import SpecificModelViewSet
from backend.broker.models import Broker


class BrokerViewSet(ActionMeMixin, SpecificModelViewSet):
    queryset = Broker.objects.select_related('user', 'firm').all()
    
    serializer_class = CRUDBrokerSerializer
    serializer_classes_by_action = {
        'retrieve': RetrieveBrokerSerializer,
        'list': ListBrokersSerializer
    }
    
    permission_classes = [permissions.IsAuthenticated, IsUserRoleObject]
    
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = BrokerFilter
    ordering = ('fixed_monthly_amount', 'profit_percentage')
    search_fields = ('user__email',)
    
    def perform_create(self, serializer):
        if self.queryset.filter(user=self.request.user).exists():
            raise ValidationError({'detail': _('You are already broker.')})
        
        serializer.save(user=self.request.user)
