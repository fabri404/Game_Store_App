from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Juego
from .serializers import JuegoSerializer
from .permissions import IsSuperUserOrReadOnly

class JuegoViewSet(viewsets.ModelViewSet):
    queryset = Juego.objects.all().order_by("id")
    serializer_class = JuegoSerializer
    permission_classes = [IsSuperUserOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["plataforma"]
    search_fields = ["nombre", "plataforma"]
    ordering_fields = ["id", "nombre", "precio"]
    ordering = ["id"]
