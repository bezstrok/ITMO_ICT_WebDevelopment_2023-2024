from rest_framework import viewsets


class SpecificPermissionClassesMixin:
    permission_classes_by_action = {}
    permission_classes_read_only = None
    permission_classes_write = None
    
    def get_permissions(self):
        try:
            return [permission() for permission in
                    self.permission_classes_by_action.get(self.action, self.permission_classes)]
        except AttributeError:
            return [permission() for permission in self.permission_classes]


class SpecificSerializerClassesMixin:
    serializer_classes_by_action = {}
    
    def get_serializer_class(self):
        return (self.get_serializer_class_by_action() or
                self.get_serializer_default())
    
    def get_serializer_class_by_action(self):
        return self.serializer_classes_by_action.get(self.action, None)
    
    def get_serializer_default(self):
        return super().get_serializer_class()


class SpecificModelViewSet(
    SpecificPermissionClassesMixin,
    SpecificSerializerClassesMixin,
    viewsets.ModelViewSet
):
    """ModelViewSet, поддерживающий различные классы разрешений и сериализаторов для разных действий."""
    pass
