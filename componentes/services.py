
from django.db import transaction

from .models import Componente, Movimiento


@transaction.atomic
def trasladar_componente(
    componente_id,
    destino,
    usuario,
    observacion=""
):
    componente = (
        Componente.objects
        .select_for_update()
        .get(id=componente_id)
    )

    destino = destino.strip()

    if not destino:
        raise ValueError(
            "Debes indicar una ubicación de destino."
        )

    if componente.ubicacion == destino:
        raise ValueError(
            "El componente ya está en esa ubicación."
        )

    movimiento = Movimiento.objects.create(
        componente=componente,
        ubicacion_origen=componente.ubicacion,
        ubicacion_destino=destino,
        usuario=usuario,
        observacion=observacion
    )

    componente.ubicacion = destino
    componente.save(update_fields=["ubicacion"])

    return movimiento
