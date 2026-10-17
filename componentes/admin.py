
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Componente, Movimiento


@admin.register(Componente)
class ComponenteAdmin(admin.ModelAdmin):

    list_display = (
        "descripcion",
        "codigo_sap",
        "numero_serie",
        "ubicacion",
        "estado",
        "ver_qr",
    )

    search_fields = (
        "descripcion",
        "codigo_sap",
        "numero_serie",
    )

    list_filter = (
        "estado",
        "ubicacion",
    )

    # La ubicación se cambia mediante traslados.
    readonly_fields = ("ubicacion",)

    @admin.display(description="Código QR")
    def ver_qr(self, obj):
        url = reverse(
            "generar_qr",
            args=[obj.id]
        )

        return format_html(
            '<a href="{}" target="_blank">Ver QR</a>',
            url
        )


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):

    list_display = (
        "componente",
        "ubicacion_origen",
        "ubicacion_destino",
        "fecha_movimiento",
        "usuario",
    )

    list_filter = (
        "fecha_movimiento",
        "ubicacion_destino",
    )

    search_fields = (
        "componente__descripcion",
        "componente__codigo_sap",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
