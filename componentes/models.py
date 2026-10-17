
import uuid
from django.db import models
from django.conf import settings


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

    descripcion = models.CharField(max_length=255)

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


class Movimiento(models.Model):
    componente = models.ForeignKey(
        Componente,
        on_delete=models.PROTECT,
        related_name="movimientos"
    )

    ubicacion_origen = models.CharField(
        max_length=100,
        blank=True
    )

    ubicacion_destino = models.CharField(
        max_length=100
    )

    fecha_movimiento = models.DateTimeField(
        auto_now_add=True
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    observacion = models.TextField(blank=True)

    def __str__(self):
        return (
            f"{self.componente.descripcion}: "
            f"{self.ubicacion_origen} → "
            f"{self.ubicacion_destino}"
        )
