from django.db import models


"""
Posibles estados de Sprint: Planificación, Ejecución, Finalizado, Cancelado
"""
SPRINT_STATUSES = (
    ('Planificacion', 'Planificacion'),
    ('Ejecucion', 'Ejecucion'),
    ('Finalizado', 'Finalizado'),
    ('Cancelado', 'Cancelado')
)


class Sprint(models.Model):
    sprint_id = models.AutoField(primary_key=True)
    sprint_name = models.CharField(max_length=50)
    start_at = models.DateField()
    end_at = models.DateField()
    status = models.CharField(max_length=20, choices=SPRINT_STATUSES, default='Planificacion')
