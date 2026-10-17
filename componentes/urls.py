
from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.inicio,
        name="inicio"
    ),

    path(
        "registrar/",
        views.registrar_componente,
        name="registrar_componente"
    ),

    path(
        "detalle/<uuid:componente_id>/",
        views.detalle_componente,
        name="detalle_componente"
    ),

    path(
        "qr/<uuid:componente_id>/",
        views.generar_qr,
        name="generar_qr"
    ),

    path(
        "movimiento/<uuid:componente_id>/",
        views.registrar_movimiento,
        name="registrar_movimiento"
    ),
]
