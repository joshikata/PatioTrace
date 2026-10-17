
import io
import qrcode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import DatabaseError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)
from django.urls import reverse

from .forms import ComponenteForm, MovimientoForm
from .models import Componente, Movimiento
from .services import trasladar_componente


@login_required
def inicio(request):
    busqueda = request.GET.get("q", "").strip()

    componentes = Componente.objects.all().order_by(
        "-fecha_registro"
    )

    total = componentes.count()

    if busqueda:
        componentes = componentes.filter(
            Q(descripcion__icontains=busqueda)
            | Q(codigo_sap__icontains=busqueda)
            | Q(numero_serie__icontains=busqueda)
        )

    return render(
        request,
        "componentes/inicio.html",
        {
            "componentes": componentes,
            "total": total,
            "total_ubicaciones": (
                Componente.objects.exclude(ubicacion="")
                .values("ubicacion").distinct().count()
            ),
            "total_movimientos": Movimiento.objects.count(),
            "busqueda": busqueda,
        }
    )


@login_required
def registrar_componente(request):
    if not request.user.has_perm(
        "componentes.add_componente"
    ):
        raise PermissionDenied

    if request.method == "POST":
        formulario = ComponenteForm(request.POST)

        if formulario.is_valid():
            componente = formulario.save()

            messages.success(
                request,
                "Componente registrado correctamente."
            )

            return redirect(
                "detalle_componente",
                componente_id=componente.id
            )
    else:
        formulario = ComponenteForm()

    return render(
        request,
        "componentes/registrar.html",
        {"formulario": formulario}
    )


@login_required
def detalle_componente(request, componente_id):
    componente = get_object_or_404(
        Componente,
        id=componente_id
    )

    movimientos = (
        componente.movimientos
        .select_related("usuario")
        .order_by("-fecha_movimiento")
    )

    return render(
        request,
        "componentes/detalle.html",
        {
            "componente": componente,
            "movimientos": movimientos
        }
    )


@login_required
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

    return HttpResponse(
        imagen.getvalue(),
        content_type="image/png"
    )


@login_required
def registrar_movimiento(request, componente_id):
    if not request.user.has_perm(
        "componentes.add_movimiento"
    ):
        raise PermissionDenied

    componente = get_object_or_404(
        Componente,
        id=componente_id
    )

    if request.method == "POST":
        formulario = MovimientoForm(request.POST)

        if formulario.is_valid():
            try:
                trasladar_componente(
                    componente_id=componente.id,
                    destino=formulario.cleaned_data[
                        "ubicacion_destino"
                    ],
                    usuario=request.user,
                    observacion=formulario.cleaned_data[
                        "observacion"
                    ]
                )

            except ValueError as error:
                formulario.add_error(
                    "ubicacion_destino",
                    str(error)
                )

            except DatabaseError:
                formulario.add_error(
                    None,
                    "No se pudo registrar el movimiento."
                )

            else:
                messages.success(
                    request,
                    "Movimiento registrado correctamente."
                )

                return redirect(
                    "detalle_componente",
                    componente_id=componente.id
                )

    else:
        formulario = MovimientoForm()

    return render(
        request,
        "componentes/movimiento.html",
        {
            "componente": componente,
            "formulario": formulario
        }
    )
