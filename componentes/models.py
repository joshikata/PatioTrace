from django.db import models
import uuid


class Componente(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    codigo_sap = models.CharField(
        max_length=30,
        blank=True
    )

    numero_serie = models.CharField(
        max_length=100,
        blank=True
    )

    descripcion = models.CharField(
        max_length=255
    )

    ubicacion = models.CharField(
        max_length=100,
        blank=True
    )

    estado = models.CharField(
        max_length=50,
        default="Sin verificar"
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.descripcion