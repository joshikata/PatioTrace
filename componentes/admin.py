from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Componente


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