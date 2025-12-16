from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Juego


class JuegoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(
        validators=[UniqueValidator(queryset=Juego.objects.all(), message="Ya existe un juego con ese nombre.")]
    )

    class Meta:
        model = Juego
        fields = ("id", "nombre", "precio", "plataforma")