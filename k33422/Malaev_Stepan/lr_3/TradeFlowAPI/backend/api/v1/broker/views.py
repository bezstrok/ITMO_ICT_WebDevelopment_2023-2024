from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from backend.api.v1.broker.serializers import (
    CRUDBrokerSerializer,
    ListBrokersSerializer,
    RetrieveBrokerSerializer
)
from backend.api.v1.core.mixins import ActionMeMixin
from backend.api.v1.core.permissions import IsUserRole
from backend.api.v1.core.viewsets import SpecificModelViewSet
from backend.broker.models import Broker


class BrokerViewSet(ActionMeMixin, SpecificModelViewSet):
    queryset = Broker.objects.select_related('user', 'firm').all()
    serializer_class = CRUDBrokerSerializer
    serializer_classes_by_action = {
        'retrieve': RetrieveBrokerSerializer,
        'list': ListBrokersSerializer
    }
    
    permission_classes = [permissions.IsAuthenticated, IsUserRole]
    
    def perform_create(self, serializer):
        if self.queryset.filter(user=self.request.user).exists():
            raise ValidationError({'detail': _('You are already broker.')})
        
        serializer.save(user=self.request.user)
