from django.db import models
from simple_history.models import HistoricalRecords

from projects.models import Project
from sprints.models import Sprint, SprintMember
from type_us.models import TypeUS
from utilities.UProject import UProject
from utilities.UUserStory import UUserStory


class UserStoryManager(models.Manager):
    # verificamos si es el estado final del US
    def is_final_status(self, id_us):
        user_story = UserStory.objects.get(id=id_us)

        return user_story.current_status == UProject.STATUS_US_FINISHED or user_story.current_status == UProject.STATUS_US_CANCELED

    def is_initial_status(self, id_us):
        user_story = UserStory.objects.get(id=id_us)
        return user_story.current_status == UProject.STATUS_US_PENDING

    # Obtenemos el primer estado
    def get_initial_status(self):
        return UProject.STATUS_US_PENDING

    def get_us_finished(self, id_project):
        finished = [us.id for us in UserStory.objects.filter(project_id=id_project) if
                    UserStory.objects.is_final_status(us.id)]
        list_finished_us = UserStory.objects.filter(id__in=finished)
        return list_finished_us.order_by('final_priority').reverse()

    def get_us_non_finished(self, id_project):
        active = [us.id for us in UserStory.objects.filter(project_id=id_project) if
                  not UserStory.objects.is_final_status(us.id)]
        list_active_us = UserStory.objects.filter(id__in=active)

        return list_active_us.order_by('final_priority').reverse()

    def get_us_no_assigned(self, id_project, id_sprint):
        sprint = Sprint.objects.get(id=id_sprint)
        user_stories = UserStory.objects.get_us_non_finished(id_project) \
            .filter(assigned_to=None, estimation_time__lte=sprint.available_capacity) \
            .order_by('final_priority').reverse()
        return user_stories


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
    status = models.CharField(max_length=20, default=UUserStory.STATUS_PENDING)
    current_status = models.CharField(max_length=20, default=UProject.STATUS_US_PENDING)
    kanban_status = models.CharField(max_length=20,null=True)
    us_type = models.ForeignKey(TypeUS, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
    assigned_to = models.ForeignKey(SprintMember, on_delete=models.CASCADE, null=True)
    cancellation_reason = models.TextField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects = UserStoryManager()

    # historial
    history = HistoricalRecords()

    # def _get_is_
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['code']
