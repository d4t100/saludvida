from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medico, Paciente, Cita
from .forms import MedicoForm, PacienteForm, CitaForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect('index')
        else:
            messages.error(request, "Credenciales inválidas.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect('login')

# MEDICOS
@login_required
def medico_list(request):
    medicos = Medico.objects.all()
    return render(request, 'medicos/medico_list.html', {'medicos': medicos})

@login_required
def medico_create(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico creado correctamente.")
            return redirect('medico_list')
    else:
        form = MedicoForm()
    return render(request, 'medicos/medico_form.html', {'form': form})

@login_required
def medico_edit(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico actualizado.")
            return redirect('medico_list')
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'medicos/medico_form.html', {'form': form})

@login_required
def medico_delete(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    if request.method == 'POST':
        medico.delete()
        messages.success(request, "Médico eliminado.")
        return redirect('medico_list')
    return render(request, 'medicos/medico_confirm_delete.html', {'medico': medico})

# PACIENTES (CRUD similar)
@login_required
def paciente_list(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/paciente_list.html', {'pacientes': pacientes})

@login_required
def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente creado.")
            return redirect('paciente_list')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/paciente_form.html', {'form': form})

@login_required
def paciente_edit(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente actualizado.")
            return redirect('paciente_list')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'pacientes/paciente_form.html', {'form': form})

@login_required
def paciente_delete(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, "Paciente eliminado.")
        return redirect('paciente_list')
    return render(request, 'pacientes/paciente_confirm_delete.html', {'paciente': paciente})

# CITAS
@login_required
def cita_list(request):
    qs = Cita.objects.select_related('paciente','medico').all().order_by('-fecha_cita','hora_cita')
    # filtros GET
    medico_id = request.GET.get('medico')
    paciente_id = request.GET.get('paciente')
    fecha = request.GET.get('fecha')
    if medico_id:
        qs = qs.filter(medico_id=medico_id)
    if paciente_id:
        qs = qs.filter(paciente_id=paciente_id)
    if fecha:
        qs = qs.filter(fecha_cita=fecha)
    medicos = Medico.objects.all()
    pacientes = Paciente.objects.all()
    return render(request, 'citas/cita_list.html', {'citas': qs, 'medicos': medicos, 'pacientes': pacientes})

@login_required
def cita_create(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cita creada correctamente.")
            return redirect('cita_list')
    else:
        form = CitaForm()
    return render(request, 'citas/cita_form.html', {'form': form})

@login_required
def cita_edit(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, "Cita actualizada.")
            return redirect('cita_list')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'citas/cita_form.html', {'form': form})

@login_required
def cita_delete(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        cita.delete()
        messages.success(request, "Cita eliminada.")
        return redirect('cita_list')
    return render(request, 'citas/cita_confirm_delete.html', {'cita': cita})
