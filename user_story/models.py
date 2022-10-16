from django.db import models

from projects.models import Project
from sprints.models import Sprint, SprintMember
from type_us.models import TypeUS


class UserStoryManager(models.Manager):
    # verificamos si es el estado final del US
    def is_final_status(self, id_us):
        user_story = UserStory.objects.get(id=id_us)
        final_status = TypeUS.objects.get_final_status(id_type_us=user_story.us_type_id)

        return user_story.current_status == final_status or user_story.current_status == 'canceled'

    def is_initial_status(self, id_us):
        user_story = UserStory.objects.get(id=id_us)
        initial_status = TypeUS.objects.get_initial_status(id_type_us=user_story.us_type_id)

        return user_story.current_status == initial_status

    # Obtenemos el primer estado
    def get_initial_status(self, id_type_us):
        return TypeUS.objects.get_initial_status(id_type_us=id_type_us)


# Create your models here.
class UserStory(models.Model):
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    business_value = models.IntegerField()
    technical_priority = models.IntegerField()
    estimation_time = models.IntegerField()
    final_priority = models.IntegerField(null=True)
    old_estimation_time = models.IntegerField(default=0)
    previous_work = models.IntegerField(default=0)
    current_status = models.CharField(max_length=20)
    us_type = models.ForeignKey(TypeUS, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
    assigned_to = models.ForeignKey(SprintMember, on_delete=models.CASCADE, null=True)
    cancellation_reason = models.TextField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects = UserStoryManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['code']
