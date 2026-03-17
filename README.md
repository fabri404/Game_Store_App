# 📘 Game Store App — Documentación Técnica

Proyecto de portfolio orientado a demostrar buenas prácticas de desarrollo backend con Python, Django y PostgreSQL, simulando el funcionamiento básico de una tienda de videojuegos (catálogo, gestión y panel administrativo).

---

## 0. Inicio rápido

### 0.1 Clonar el repositorio

```bash
git clone https://github.com/fabri404/Game_Store_App.git
cd Game_Store_App
```

### 0.2 Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 1. ¿Qué hace esta aplicación?

Game Store App simula una tienda virtual de videojuegos, permitiendo:

- Registrar y administrar juegos.
- Visualizar un catálogo organizado.
- Gestionar precios, plataformas y detalles.
- Cargar nuevos juegos manualmente o de manera automatizada.
- Administrar datos desde el panel de administración de Django.

Además, incluye:

- API REST disponible para integraciones futuras.
- Cifrado de contraseñas para usuarios que se registren (aunque no haya sistema de autenticación completo aún).
- Arquitectura preparada para escalar.

---

## 2. Arquitectura y tecnologías

| Componente | Descripción |
|---|---|
| Python | Lenguaje principal |
| Django | Framework backend |
| Django Admin | Panel administrativo nativo |
| PostgreSQL | Base de datos |
| ORM Django | Gestión de modelos y migraciones |
| API interna | Endpoints básicos para operaciones sobre juegos |

El uso del ORM asegura:

- Abstracción del SQL.
- Migraciones versionadas.
- Seguridad frente a inyecciones.

---

## 3. Base de datos (PostgreSQL)

### 3.1 Crear base de datos

```sql
sudo -u postgres psql -c "CREATE DATABASE game_store;"
sudo -u postgres psql -c "CREATE USER game_user WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE game_store TO game_user;"
```

### 3.2 Configurar `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'game_store',
        'USER': 'game_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3.3 Migraciones

```bash
python manage.py migrate
```

---

## 4. Seguridad y cifrado

Aunque el sistema no utiliza autenticación completa aún, las contraseñas registradas se almacenan mediante hash seguro, utilizando mecanismos del core de Django.

Esto garantiza:

- No se guardan contraseñas en texto plano.
- El proyecto sigue prácticas correctas de seguridad.

---

## 5. Panel administrativo (Django Admin)

Django incluye un panel potente y sencillo.

### 5.1 Crear superusuario

```bash
python manage.py createsuperuser
```

### 5.2 Acceso

```
http://127.0.0.1:8000/admin
```

Desde aquí puedes:

- Crear juegos.
- Editar detalles.
- Ordenar y filtrar.
- Administrar registros.

Este panel es ideal para cargar contenido de manera rápida e intuitiva, sin escribir código.

---

## 6. API y carga de juegos

### 6.1 Endpoints principales

> **Nota:** Solo accesibles con los permisos requeridos.

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/catalogo/` | Listar juegos |
| `GET` | `/catalogo/<id>` | Detalle de un juego |
| `POST` | `/catalogo/nuevo` | Cargar juego (API) |
| `DELETE` | `/catalogo/<id>` | Eliminar juego |

---

## 7. Cargar juegos de ejemplo

### Desde el panel admin (recomendado)

1. Ingresar a `/admin`
2. Seleccionar **Juegos**
3. Click en **Agregar**
4. Completar formulario
5. Guardar

---

## 8. Estructura del proyecto

```
Game_Store_App/
├── catalogo/          # App principal (modelos, vistas, templates)
├── usuarios/          # Gestión futura de usuarios / cifrado
├── game_store/        # Configuración general Django
├── templates/         # HTML compartido
├── static/            # Recursos estáticos
└── requirements.txt
```
