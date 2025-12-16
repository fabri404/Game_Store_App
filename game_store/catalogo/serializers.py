from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Juego


class JuegoSerializer(serializers.ModelSerializer):
    precio = serializers.DecimalField(max_digits=10, decimal_places=2)
    nombre = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Juego.objects.all(),
                message="Ya existe un juego con ese nombre."
            )
        ]
    )

    class Meta:
        model = Juego
        fields = ("id", "nombre", "precio", "plataforma")
        read_only_fields = ("id",)  # POST normal no acepta id


class JuegoCreateWithIdSerializer(JuegoSerializer):
    # Para el endpoint especial, el id es obligatorio y escribible
    id = serializers.IntegerField(required=True)

    class Meta(JuegoSerializer.Meta):
        read_only_fields = ()  # permite escribir id en este serializer

    def create(self, validated_data):
        requested_id = validated_data.pop("id")
        obj = Juego(id=requested_id, **validated_data)
        obj.save(force_insert=True)  # fuerza INSERT (si existe, revienta)
        return obj
