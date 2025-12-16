from django.http import Http404

from rest_framework import viewsets, filters
from rest_framework.exceptions import NotFound
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

    def get_object(self):
        """
        Personaliza el mensaje 404 cuando el ID no existe,
        sin ocultar errores reales del servidor.
        """
        try:
            return super().get_object()
        except Http404:
            raise NotFound("No existe un juego con el ID solicitado.")
