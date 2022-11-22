from django.db import models


class Meeting(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    meeting_name = models.CharField(max_length=50)
    meeting_details = models.CharField(max_length=2000, null=True)
    meeting_date = models.DateField(null=True, verbose_name='Fecha de la reunion')
