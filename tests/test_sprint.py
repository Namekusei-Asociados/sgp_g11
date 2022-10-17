from _datetime import datetime
import pandas as pd
import pytest
from django.test import TestCase
from accounts.models import User
from user_story.models import UserStory
from type_us.models import TypeUS
from projects.models import ProjectMember
from projects.models import Project
from sprints.models import Sprint


class TestSprints(TestCase):

    fixtures = ['default_roles_system.json', 'permissions.json', 'permissionsProj.json', 'admin.json']

    @pytest.mark.django_db
    def test_create_sprint(self):
        user = User.objects.create(username='test_user', password='password')
        user.save()
        project = Project.objects.create(name='proyecto de juan', description='test_project')
        assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
        project_member = ProjectMember.objects.create(project=project, user=user)
        us_type = TypeUS.objects.create(prefix='test', name='name_test',
                                        flow=[('Pendiente', 'Pendiente'), ('Haciendo', 'Haciendo'),
                                              ('Finalizado', 'Finalizado')], project=project)
        assert us_type.name == 'name_test', "Error al crear Tipo de US"
        user_story = UserStory.objects.create(
            title='user_story_de_prueba',
            description='descripcion prueba',
            business_value=10,
            technical_priority=20,
            estimation_time=30,
            project_id=project.id,
            us_type_id=us_type.id
        )
        sprint = Sprint.objects.create(sprint_name='Sprint Test',
                                       start_at=datetime.strptime('2022/09/30', '%Y/%m/%d'),
                                       end_at=datetime.strptime('2022/10/15', '%Y/%m/%d'),
                                       duration=pd.bdate_range(start=datetime.strptime('2022/09/30', '%Y/%m/%d'),
                                                               end=datetime.strptime('2022/10/15', '%Y/%m/%d')).size,
                                       number=1,
                                       project_id=project.id)

        self.assertEqual(sprint.sprint_name, 'Sprint Test', "No se ha creado correctamente el sprint")

        user_story.sprint = sprint
        user_story.save()

        self.assertEqual(user_story.sprint.id, sprint.id, "No se han asociado correctamente el sprint y la US")
