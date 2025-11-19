from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('medicos/', views.medico_list, name='medico_list'),
    path('medicos/nuevo/', views.medico_create, name='medico_create'),
    path('medicos/<int:pk>/editar/', views.medico_edit, name='medico_edit'),
    path('medicos/<int:pk>/eliminar/', views.medico_delete, name='medico_delete'),

    path('pacientes/', views.paciente_list, name='paciente_list'),
    path('pacientes/nuevo/', views.paciente_create, name='paciente_create'),
    path('pacientes/<int:pk>/editar/', views.paciente_edit, name='paciente_edit'),
    path('pacientes/<int:pk>/eliminar/', views.paciente_delete, name='paciente_delete'),

    path('citas/', views.cita_list, name='cita_list'),
    path('citas/nuevo/', views.cita_create, name='cita_create'),
    path('citas/<int:pk>/editar/', views.cita_edit, name='cita_edit'),
    path('citas/<int:pk>/eliminar/', views.cita_delete, name='cita_delete'),
]
