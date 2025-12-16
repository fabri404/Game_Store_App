import re
from django.db import models


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


def _collapse_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def normalize_title(text: str) -> str:
    """
    Primera letra en mayúscula por palabra (tipo Title Case).
    Ej: "god oF WAR 3" -> "God Of War 3"
    """
    text = _collapse_spaces(text)
    if not text:
        return text

    words = []
    for w in text.split(" "):
        # Mantener números tal cual
        if w.isdigit():
            words.append(w)
        else:
            words.append(w[:1].upper() + w[1:].lower())
    return " ".join(words)


def _parse_platform_items(raw: str) -> list[str]:
    """
    Acepta plataformas separadas por coma, punto y coma, pipe o espacios.
    Hace matching greedy para plataformas multi-palabra (xbox series x).
    """
    raw = _collapse_spaces(raw)
    if not raw:
        return []

    # Unificar separadores comunes en coma
    raw = re.sub(r"[;|]+", ",", raw)

    chunks = [c.strip() for c in raw.split(",") if c.strip()]
    items: list[str] = []

    for chunk in chunks:
        tokens = chunk.lower().split()
        i = 0
        while i < len(tokens):
            matched = None

            # intentar match de la frase más larga posible (greedy)
            for j in range(len(tokens), i, -1):
                phrase = " ".join(tokens[i:j])
                if phrase in PLATFORM_CANONICAL:
                    matched = PLATFORM_CANONICAL[phrase]
                    i = j
                    break

            if matched is None:
                # fallback: token simple
                tok = tokens[i]
                matched = PLATFORM_CANONICAL.get(tok, tok[:1].upper() + tok[1:].lower())
                i += 1

            items.append(matched)

    # Deduplicar preservando orden
    out, seen = [], set()
    for it in items:
        key = it.lower()
        if key not in seen:
            seen.add(key)
            out.append(it)

    return out


def normalize_platforms(raw: str) -> str:
    """
    Devuelve siempre un formato único: "PS2, PS3, PC"
    aunque se ingrese "ps2 ps3, pc" o "ps2 ps3 pc"
    """
    items = _parse_platform_items(raw)
    return ", ".join(items)


class Juego(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    plataforma = models.CharField(max_length=100)

    def clean(self):
        self.nombre = normalize_title(self.nombre)
        self.plataforma = normalize_platforms(self.plataforma)

    def save(self, *args, **kwargs):
        # Esto asegura normalización incluso si guardás desde API o scripts
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
