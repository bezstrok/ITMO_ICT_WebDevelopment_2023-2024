from rest_framework import viewsets

from backend.api.v1.core.mixins import (
    SpecificPermissionClassesMixin,
    SpecificSerializerClassesMixin
)


class SpecificModelViewSet(
    SpecificPermissionClassesMixin,
    SpecificSerializerClassesMixin,
    viewsets.ModelViewSet
):
    """ModelViewSet, поддерживающий различные классы разрешений и сериализаторов для разных действий."""
    pass
