from rest_framework.decorators import action


class ActionMeMixin:
    @action(detail=False, methods=['get', 'put', 'patch', 'delete'])
    def me(self, request, *args, **kwargs):
        """
        Возвращает информацию о роли, ассоциированном с текущим аутентифицированным пользователем.
        """
        # Переопределяем атрибуты для `get_object`
        self.lookup_field = 'user'
        self.kwargs[self.lookup_field] = self.request.user
        
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


class SpecificPermissionClassesMixin:
    permission_classes_by_action = {}
    permission_classes_common = []
    
    def get_permissions(self):
        permission_classes = (self.get_permissions_by_action() or
                              self.get_permissions_default())
        
        return [*self.get_permissions_common(), *permission_classes]
    
    def get_permissions_common(self):
        return [permission() for permission in self.permission_classes_common]
    
    def get_permissions_by_action(self):
        return [permission() for permission in self.permission_classes_by_action.get(self.action, [])]
    
    def get_permissions_default(self):
        return super().get_permissions()


class SpecificSerializerClassesMixin:
    serializer_classes_by_action = {}
    
    def get_serializer_class(self):
        return (self.get_serializer_class_by_action() or
                self.get_serializer_class_default())
    
    def get_serializer_class_by_action(self):
        return self.serializer_classes_by_action.get(self.action, None)
    
    def get_serializer_class_default(self):
        return super().get_serializer_class()
