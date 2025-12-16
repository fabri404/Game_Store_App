from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUserOrReadOnly(BasePermission):
    # Este mensaje se devuelve cuando DRF bloquea por permisos (403)
    message = "Acceso denegado: solo el superusuario puede crear, editar o eliminar juegos."

    def has_permission(self, request, view):
        # Lectura pública
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True

        # Escritura solo superusuario autenticado
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )
