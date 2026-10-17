import io
import qrcode

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import Componente


def generar_qr(request, componente_id):
    componente = get_object_or_404(
        Componente,
        id=componente_id
    )

    url = request.build_absolute_uri(
        reverse(
            "detalle_componente",
            args=[componente.id]
        )
    )

    qr = qrcode.make(url)

    imagen = io.BytesIO()
    qr.save(imagen, format="PNG")
    imagen.seek(0)

    return HttpResponse(
        imagen.getvalue(),
        content_type="image/png"
    )


def detalle_componente(request, componente_id):
    componente = get_object_or_404(
        Componente,
        id=componente_id
    )

    return HttpResponse(
        f"""
        <h1>{componente.descripcion}</h1>
        <p><b>Codigo SAP:</b> {componente.codigo_sap}</p>
        <p><b>Numero de serie:</b> {componente.numero_serie}</p>
        <p><b>Ubicacion:</b> {componente.ubicacion}</p>
        <p><b>Estado:</b> {componente.estado}</p>
        <p><b>Fecha de registro:</b> {componente.fecha_registro}</p>
        """
    )