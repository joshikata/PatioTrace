
from django import forms
from .models import Componente


ESTADOS = [
    ("Sin verificar", "Sin verificar"),
    ("Disponible", "Disponible"),
    ("En reparación", "En reparación"),
    ("Reservado", "Reservado"),
]


class ComponenteForm(forms.ModelForm):

    class Meta:
        model = Componente

        fields = [
            "descripcion",
            "codigo_sap",
            "numero_serie",
            "ubicacion",
            "estado",
        ]

        widgets = {
            "descripcion": forms.TextInput(attrs={
                "placeholder": "Descripción del componente"
            }),
            "codigo_sap": forms.TextInput(attrs={
                "placeholder": "Código SAP (opcional)"
            }),
            "numero_serie": forms.TextInput(attrs={
                "placeholder": "Número de serie (opcional)"
            }),
            "ubicacion": forms.TextInput(attrs={
                "placeholder": "Ej. Patio A - Sector 01"
            }),
            "estado": forms.Select(choices=ESTADOS),
        }

    def clean(self):
        cleaned_data = super().clean()

        codigo_sap = (
            cleaned_data.get("codigo_sap") or ""
        ).strip()

        numero_serie = (
            cleaned_data.get("numero_serie") or ""
        ).strip()

        if numero_serie:
            coincidencias = Componente.objects.filter(
                numero_serie__iexact=numero_serie,
                codigo_sap__iexact=codigo_sap
            )

            if coincidencias.exists():
                raise forms.ValidationError(
                    "Ya existe un componente con "
                    "este código SAP y número de serie."
                )

        return cleaned_data


class MovimientoForm(forms.Form):

    ubicacion_destino = forms.CharField(
        max_length=100,
        label="Nueva ubicación",
        widget=forms.TextInput(attrs={
            "placeholder": "Ej. Patio B - Sector 02"
        })
    )

    observacion = forms.CharField(
        required=False,
        label="Observación",
        widget=forms.Textarea(attrs={
            "rows": 3,
            "placeholder": "Motivo del traslado"
        })
    )

    def clean_ubicacion_destino(self):
        destino = self.cleaned_data[
            "ubicacion_destino"
        ].strip()

        if not destino:
            raise forms.ValidationError(
                "Debes ingresar una ubicación."
            )

        return destino
