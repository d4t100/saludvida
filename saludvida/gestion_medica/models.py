from django.db import models

class Medico(models.Model):
    nombre_completo = models.CharField(max_length=200)
    rut = models.CharField(max_length=12, unique=True)  # ✅ Ya está bien (12 caracteres)
    especialidad = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, unique=True)  # ✅ REDUCIDO: era 254, ahora 100
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_completo} - {self.especialidad}"

    class Meta:
        db_table = 'gestion_medica_medico'
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'


class Paciente(models.Model):
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    
    nombre_completo = models.CharField(max_length=200)
    rut = models.CharField(max_length=12, unique=True)  # ✅ Ya está bien (12 caracteres)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_completo} ({self.rut})"

    class Meta:
        db_table = 'gestion_medica_paciente'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'


class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas')
    especialidad = models.CharField(max_length=100)
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'gestion_medica_cita'
        unique_together = ('medico', 'fecha_cita', 'hora_cita')  # Evita dos citas iguales para mismo médico/hora
        verbose_name = 'Cita Médica'
        verbose_name_plural = 'Citas Médicas'
        ordering = ['-fecha_cita', '-hora_cita']

    def __str__(self):
        return f"Cita {self.id}: {self.fecha_cita} {self.hora_cita} - {self.paciente}"
