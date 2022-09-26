from django.db import models

from projects.models import Project, ProjectMember
from type_us.models import TypeUS


# Create your models here.
class UserStory(models.Model):
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    business_value = models.IntegerField()
    technical_priority = models.IntegerField()
    estimation_time = models.IntegerField()
    current_status = models.CharField(max_length=20)
    us_type = models.ForeignKey(TypeUS, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
    assigned_to = models.ForeignKey(ProjectMember, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['code']
