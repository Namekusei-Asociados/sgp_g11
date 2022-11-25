from django.db import models

from accounts.models import User
from utilities.USprint import USprint

"""
Posibles estados de Sprint: Planificación, Ejecución, Finalizado, Cancelado
"""
SPRINT_STATUSES = (
    ('success', 'success'),
    ('pending', 'pending'),
    ('finished', 'finished'),
    ('canceled', 'canceled'),
    ('in execution', 'in execution')
)


class Sprint(models.Model):
    number = models.IntegerField()
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    sprint_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True)
    capacity = models.IntegerField(verbose_name='Capacidad en horas', null=True, default=0)
    available_capacity = models.IntegerField(verbose_name='Capacidad en horas restantes', null=True)
    duration = models.IntegerField(verbose_name='Duración en días')
    start_at = models.DateField(null=True, verbose_name='Fecha de inicio')
    estimated_end_at = models.DateField(null=True, verbose_name='Fecha de finalización estimada')
    end_at = models.DateField(null=True, verbose_name='Fecha de finalización')
    status = models.CharField(max_length=20, choices=SPRINT_STATUSES, default=USprint.STATUS_PENDING, verbose_name='Estado')
    cancellation_reason = models.TextField(max_length=500, null=True)
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
    deleted_at = models.DateTimeField(null=True)
