from django.db import models
from simple_history.models import HistoricalRecords

from accounts.models import User
from projects.models import Project
from sprints.models import Sprint, SprintMember
from type_us.models import TypeUS
from utilities.UUserStory import UUserStory


class UserStoryManager(models.Manager):
    # verificamos si es el estado final del US
    def is_final_status(self, id_us):
        user_story = UserStory.objects.get(id=id_us)

        return user_story.current_status == UUserStory.STATUS_FINISHED or user_story.current_status == UUserStory.STATUS_CANCELED

    def is_initial_status(self, id_us):
        user_story = UserStory.objects.get(id=id_us)
        return user_story.current_status == UUserStory.STATUS_PENDING

    # Obtenemos el primer estado
    def get_initial_status(self):
        return UUserStory.STATUS_PENDING

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


class UserStoryAttachmentManager(models.Manager):
    @staticmethod
    def get_attachments(id_us):
        return UserStoryAttachment.objects.filter(user_story_id=id_us).order_by('-created_at')


class UserStoryTaskManager(models.Manager):
    def create_us_task(self, id_user_story, task, work_hours):
        """
        Funcion para crear Us

        :param id_user_story: id del us
        :param task: tarea
        :param work_hours: horas trabajadas en ese US

        :return: Task creado
        """
        us_task = UserStoryTask.objects.create(user_story_id=id_user_story, task=task, work_hours=work_hours)
        user_story = UserStory.objects.get(id=id_user_story)
        user_story.work_hours += work_hours
        user_story.task.add(us_task)
        return us_task

    def delete_us_task(self, id_user_story, id_task):
        """
        Eliminar tarea de US

        :param id_user_story: id user story
        :param id_task: id de la tarea

        :return: Booleano True: correcto, False: fallo en la eliminacion
        """
        user_story = UserStory.objects.get(id=id_user_story)
        task = UserStoryTask.objects.get(id=id_task)

        if user_story.tasks.filter(
                id=task.id).exists() and user_story.current_status != "finished" and user_story.current_status != "canceled":
            # Actualizamos las horas trabajadas
            user_story.horas_trabajadas -= task.horasTrabajadas
            user_story.task.remove(task)
            return True
        else:
            return None

    def list_tasks(self, id_user_story):
        user_story = UserStory.objects.get(id=id_user_story)
        tasks = user_story.tasks.all()
        return tasks


class UserStoryTask(models.Model):
    task = models.TextField(max_length=100)
    work_hours = models.IntegerField()
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(SprintMember, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserStoryTaskManager()

    def __str__(self):
        return self.task


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
    current_status = models.CharField(max_length=20, default=UUserStory.STATUS_PENDING)
    kanban_status = models.CharField(max_length=20, null=True)
    cancellation_reason = models.TextField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # tipo de Us asociado
    us_type = models.ForeignKey(TypeUS, on_delete=models.CASCADE)
    # proyecto asociado
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # sprint asociado
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
    # Usuario asignado a la US
    assigned_to = models.ForeignKey(SprintMember, on_delete=models.CASCADE, null=True)
    # Tareas de la US
    tasks = models.ManyToManyField(UserStoryTask)

    objects = UserStoryManager()

    # historial
    history = HistoricalRecords()

    # def _get_is_
    def __str__(self):
        return self.title


def us_directory_path(instance, filename):
    return f"static/us_attached_files/project{instance.user_story.project_id}/{instance.user_story.id}/{filename}"


class UserStoryAttachment(models.Model):
    file = models.FileField(upload_to=us_directory_path, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # US relacionado
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    # Manager de la clase
    objects = UserStoryAttachmentManager()

    @property
    def filename(self):
        return self.file.name.split('/')[-1]

    @property
    def size(self):
        # Return a string with the size and the unit
        amount_of_divisions = 0
        size = self.file.size
        while size > 1024:
            size = size / 1024
            amount_of_divisions += 1
        units = {
            0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB',
        }
        return f"{round(size, 2)} {units[amount_of_divisions]}"
