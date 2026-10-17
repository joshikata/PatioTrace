from django.urls import path
from . import views

urlpatterns = [
    path(
        "qr/<uuid:componente_id>/",
        views.generar_qr,
        name="generar_qr"
    ),

    path(
        "detalle/<uuid:componente_id>/",
        views.detalle_componente,
        name="detalle_componente"
    ),
]