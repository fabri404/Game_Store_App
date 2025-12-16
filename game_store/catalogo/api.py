from django.db import IntegrityError

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .models import Juego
from .serializers import JuegoSerializer, JuegoCreateWithIdSerializer
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

    @action(
        detail=False,
        methods=["post"],
        url_path="with-id",
        serializer_class=JuegoCreateWithIdSerializer,
    )
    def create_with_id(self, request):
        """
        POST /api/juegos/with-id/
        Crea un juego usando el ID provisto.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj = serializer.save()
        except IntegrityError:
            # Puede ser por ID ya existente o por unique de nombre en DB
            return Response(
                {"detail": "No se pudo crear: el ID ya existe o viola una restricción de unicidad."},
                status=status.HTTP_409_CONFLICT,
            )

        # Responder con el serializer normal (mismo formato que el resto del API)
        return Response(JuegoSerializer(obj).data, status=status.HTTP_201_CREATED)
