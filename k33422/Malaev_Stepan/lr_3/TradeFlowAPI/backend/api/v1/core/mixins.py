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
