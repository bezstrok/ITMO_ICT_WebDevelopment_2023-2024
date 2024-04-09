from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from backend.api.v1.core.mixins import ActionMeMixin
from backend.api.v1.core.permissions import IsUserRoleObject
from backend.api.v1.core.viewsets import SpecificModelViewSet
from backend.api.v1.manufacturer.serializers import (
    CRUDManufacturerSerializer,
    ListManufacturerSerializer,
    RetrieveManufacturerSerializer
)
from backend.manufacturer.models import Manufacturer


class ManufacturerViewSet(ActionMeMixin, SpecificModelViewSet):
    queryset = Manufacturer.objects.select_related('user').all()
    
    serializer_class = CRUDManufacturerSerializer
    serializer_classes_by_action = {
        'retrieve': RetrieveManufacturerSerializer,
        'list': ListManufacturerSerializer,
    }
    
    permission_classes = [permissions.IsAuthenticated, IsUserRoleObject]
    
    filter_backends = (OrderingFilter, SearchFilter)
    ordering = ('firm_name',)
    search_fields = ('firm_name', 'user__email')
    
    def perform_create(self, serializer):
        if self.queryset.filter(user=self.request.user).exists():
            raise ValidationError({'detail': _('You are already manufacturer.')})
        
        serializer.save(user=self.request.user)
