from django.db import models

from accounts.models import User

"""
Posibles estados de Sprint: Planificación, Ejecución, Finalizado, Cancelado
"""
SPRINT_STATUSES = (
    ('planning', 'Planificacion'),
    ('progress', 'Ejecucion'),
    ('finished', 'Finalizado'),
    ('canceled', 'Cancelado')
)


class Sprint(models.Model):
    number = models.IntegerField()
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    sprint_name = models.CharField(max_length=50)
    capacity = models.IntegerField(verbose_name='Capacidad en horas', null=True)
    duration = models.IntegerField(verbose_name='Duración en días')
    start_at = models.DateField(null=True, verbose_name='Fecha de inicio')
    end_at = models.DateField(null=True, verbose_name='Fecha de finalización')
    status = models.CharField(max_length=20, choices=SPRINT_STATUSES, default='Planificacion', verbose_name='Estado')
    members = models.ManyToManyField(User, through='sprints.SprintMember')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"Sprint {self.number} - {self.project.name}"


class SprintMember(models.Model):
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workload = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
