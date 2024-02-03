from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from backend.api.v1.broker.serializers import (
    CRUDBrokerSerializer,
    ListBrokersSerializer,
    RetrieveBrokerSerializer
)
from backend.api.v1.core import viewsets
from backend.api.v1.core.permissions import IsUserBroker
from backend.broker.models import Broker


class BrokerViewSet(viewsets.SpecificModelViewSet):
    queryset = Broker.objects.select_related('user', 'firm').all()
    serializer_class = CRUDBrokerSerializer
    serializer_classes_by_action = {
        'retrieve': RetrieveBrokerSerializer,
        'list': ListBrokersSerializer
    }
    
    permission_classes = [permissions.IsAuthenticated, IsUserBroker]
    
    def perform_create(self, serializer):
        if self.queryset.filter(user=self.request.user).exists():
            raise ValidationError({'detail': _('You are already broker.')})
        
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get', 'put', 'patch', 'delete'])
    def me(self, request, *args, **kwargs):
        """
        Возвращает информацию о брокере, ассоциированном с текущим аутентифицированным пользователем.
        """
        # Переопределяем атрибуты для `get_object`
        self.lookup_field = 'user'
        self.kwargs['user'] = self.request.user
        
        match request.method:
            case 'GET':
                self.action = 'retrieve'
                return self.retrieve(request, *args, **kwargs)
            case 'PUT':
                return self.update(request, *args, **kwargs)
            case 'PATCH':
                return self.partial_update(request, *args, **kwargs)
            case 'DELETE':
                return self.destroy(request, *args, **kwargs)
