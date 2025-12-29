import re
import uuid
from django.db import models
from django.utils.text import slugify


PLATFORM_CANONICAL = {
    "pc": "PC",
    "ps2": "PS2",
    "ps3": "PS3",
    "ps4": "PS4",
    "ps5": "PS5",
    "xbox": "Xbox",
    "xbox one": "Xbox One",
    "xbox series x": "Xbox Series X",
    "xbox series s": "Xbox Series S",
    "switch": "Switch",
    "switch 2": "Switch 2",
    "switch oled": "Switch Oled",
}


def juego_upload_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    base = slugify(instance.nombre)[:60] or "juego"
    bucket = f"{(instance.pk or 0)//100:04d}"

    return f"juegos/{bucket}/{base}-{uuid.uuid4().hex[:8]}.{ext}"


def _collapse_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def normalize_title(text: str) -> str:
    text = _collapse_spaces(text)
    if not text:
        return text

    words = []
    for w in text.split(" "):
        if w.isdigit():
            words.append(w)
        else:
            words.append(w[:1].upper() + w[1:].lower())
    return " ".join(words)


def _parse_platform_items(raw: str) -> list[str]:
    raw = _collapse_spaces(raw)
    if not raw:
        return []

    raw = re.sub(r"[;|]+", ",", raw)
    chunks = [c.strip() for c in raw.split(",") if c.strip()]
    items: list[str] = []

    for chunk in chunks:
        tokens = chunk.lower().split()
        i = 0
        while i < len(tokens):
            matched = None
            for j in range(len(tokens), i, -1):
                phrase = " ".join(tokens[i:j])
                if phrase in PLATFORM_CANONICAL:
                    matched = PLATFORM_CANONICAL[phrase]
                    i = j
                    break
            if matched is None:
                tok = tokens[i]
                matched = PLATFORM_CANONICAL.get(
                    tok, tok[:1].upper() + tok[1:].lower()
                )
                i += 1
            items.append(matched)

    out, seen = [], set()
    for it in items:
        key = it.lower()
        if key not in seen:
            seen.add(key)
            out.append(it)
    return out


def normalize_platforms(raw: str) -> str:
    items = _parse_platform_items(raw)
    return ", ".join(items)


class Juego(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    plataforma = models.CharField(max_length=100)
    portada = models.ImageField(upload_to=juego_upload_path, blank=True, null=True)

    def clean(self):
        self.nombre = normalize_title(self.nombre)
        self.plataforma = normalize_platforms(self.plataforma)

    def save(self, *args, **kwargs):
        """
        - Normaliza nombre y plataformas.
        - Detecta si hay una portada nueva.
        - Guarda el modelo.
        """

        # Normalización + validaciones del modelo
        self.full_clean()

        # Detectar si se cambió la imagen
        new_file = False
        if self.pk:  # ya existe en la base
            old = type(self).objects.filter(pk=self.pk).only("portada").first()
            if old and old.portada != self.portada:
                new_file = True
        else:
            # objeto nuevo: si viene imagen, es nueva
            new_file = bool(self.portada)

        # Guardamos primero para que el archivo exista en disco
        super().save(*args, **kwargs)

        # Si no hubo cambio de imagen, no hacemos nada más
        if not new_file or not self.portada:
            return

    def __str__(self):
        return self.nombre
