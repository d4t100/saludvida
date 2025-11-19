from django import forms
from .models import Medico, Paciente, Cita
from django.utils import timezone
import re
from datetime import date

# Validador de nombre: al menos dos palabras, cada una >=3 letras
def validar_nombre_completo(value):
    parts = [p for p in re.split(r'\s+', value.strip()) if p]
    if len(parts) < 2:
        raise forms.ValidationError("El nombre debe contener al menos dos palabras.")
    for p in parts:
        if len(p) < 3:
            raise forms.ValidationError("Cada palabra del nombre debe tener al menos 3 letras.")

# Validador simple de RUT chileno (formato básico con dígito verificador) --- se puede mejorar
def validar_rut(value):
    rut = re.sub(r'[^0-9kK]', '', value)
    if len(rut) < 7:
        raise forms.ValidationError("RUT inválido (demasiado corto).")
    # no implementamos verificación completa por brevedad, solo formato base
    if not re.match(r'^\d{7,8}[0-9kK]$', rut):
        raise forms.ValidationError("Formato de RUT inválido.")

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = '__all__'

    def clean_nombre_completo(self):
        val = self.cleaned_data.get('nombre_completo','')
        validar_nombre_completo(val)
        return val.title()

    def clean_rut(self):
        rut = self.cleaned_data.get('rut','')
        validar_rut(rut)
        return rut

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'

    def clean_nombre_completo(self):
        val = self.cleaned_data.get('nombre_completo','')
        validar_nombre_completo(val)
        return val.title()

    def clean_rut(self):
        rut = self.cleaned_data.get('rut','')
        validar_rut(rut)
        return rut

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente','medico','especialidad','fecha_cita','hora_cita','observaciones']

    def clean_fecha_cita(self):
        fecha = self.cleaned_data.get('fecha_cita')
        if fecha < date.today():
            raise forms.ValidationError("La fecha de la cita no puede ser anterior a hoy.")
        return fecha

    def clean_especialidad(self):
        esp = self.cleaned_data.get('especialidad','').strip()
        if not esp:
            raise forms.ValidationError("La especialidad es obligatoria.")
        return esp

    def clean(self):
        cleaned = super().clean()
        paciente = cleaned.get('paciente')
        medico = cleaned.get('medico')
        fecha = cleaned.get('fecha_cita')
        hora = cleaned.get('hora_cita')
        especialidad = cleaned.get('especialidad')

        if medico and especialidad and medico.especialidad != especialidad:
            raise forms.ValidationError("La especialidad debe coincidir con la especialidad del médico seleccionado.")

        # Validación: paciente no puede tener más de una cita el mismo día en la misma especialidad
        if paciente and fecha and especialidad:
            qs = Cita.objects.filter(paciente=paciente, fecha_cita=fecha, especialidad__iexact=especialidad)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("El paciente ya tiene una cita ese día en la misma especialidad.")

        # Validación: médico no puede tener 2 citas al mismo tiempo (se duplica con unique_together, pero lo ponemos en formulario para mensajería clara)
        if medico and fecha and hora:
            qs2 = Cita.objects.filter(medico=medico, fecha_cita=fecha, hora_cita=hora)
            if self.instance.pk:
                qs2 = qs2.exclude(pk=self.instance.pk)
            if qs2.exists():
                raise forms.ValidationError("El médico ya tiene una cita asignada en ese horario.")

        return cleaned
