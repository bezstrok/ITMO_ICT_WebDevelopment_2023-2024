from rest_framework import generics, permissions

from backend.broker.models import Firm
from .serializers import FirmDetailSerializer, FirmListSerializer


class FirmDetailView(generics.RetrieveAPIView):
    queryset = Firm.objects.prefetch_related('brokers').all()
    serializer_class = FirmDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class FirmListView(generics.ListAPIView):
    queryset = Firm.objects.all()
    serializer_class = FirmListSerializer
    permission_classes = [permissions.IsAuthenticated]
