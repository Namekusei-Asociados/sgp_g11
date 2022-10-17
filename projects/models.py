import json

from django.db import models

from accounts.models import User
from utilities.UProject import UProject
from utilities.UProjectDefaultRoles import UProjectDefaultRoles


#########################################################
####################### MANAGER #########################
#########################################################

class RoleProjectManager(models.Manager):
    # funcion para crear roles permisos por modelo
    def create_role(self, name, description, id_project, permissions_list):
        """
        Crear un nuevo rol del sistema

        :param id_project: id del proyecto
        :param name: nombre del rol
        :param description: descripcion del rol
        :param permissions_list: lista de permisos a ser asignados al rol
        """
        if not RoleProject.objects.filter(role_name=name).exists():
            role = RoleProject.objects.create(
                role_name=name,
                description=description,
                project=Project.objects.get(id=id_project)
            )
            self.attach_permissions(role.id, permissions_list)
            print('rol creado exitosamente')
            return True
        else:
            return False

    # funcion encargada de asignar permisos a los roles
    def attach_permissions(self, id_role, permissions_list):
        """
        Asignar peromisos al rol

        :param id_role: id del rol al cual seran asignados los permisos
        :param permissions_list: lista de permisos a ser asignados
        """
        role = RoleProject.objects.get(id=id_role)
        for permiso_temp in permissions_list:
            role.perms.add(permiso_temp)

    @staticmethod
    def assing_role(project_member, roles):
        """
        Asignar rol a usuario

        :param role: rol a ser asignado
        :param user: usuario al cual sera asignado el rol
        """
        for role in roles:
            project_member.roles.add(role)

    def get_project_roles(self, id_project):
        """
        Roles de un proyecto

        :param id_project: id del proyecto
        """
        return RoleProject.objects.filter(project_id=id_project).order_by('id')

    def get_member_roles(self, id_user, id_project):
        """
        Obtener los roles de un usuario en un proyecto

        :param id_user: id del usuario consultado
        """
        user = User.objects.get(id=id_user)
        projects = Project.objects.get(id=id_project)
        return ProjectMember.objects.get(user=user, project=projects).roles.all()

    @staticmethod
    def delete_role(id_role):
        """
        Eliminar un rol de sistema

        :param id_role: id del rol a ser eliminado
        """
        role = RoleProject.objects.get(id=id_role)
        if not ProjectMember.objects.filter(
                roles__id=id_role).count() > 0 and role.role_name != UProjectDefaultRoles.SCRUM_MASTER:
            role.delete()
            print("Eliminado exitosamente")
            return True
        else:
            return False

    @staticmethod
    def update_role(id_role, perms, name=None, description=None):
        """
        Funcion para editar un rol de sistema

        :param id_role: id del rol a editar
        :param name: nombre actualizado
        :param description: descripcion actualizada
        :param perms: lista de permisos actualizados

        :return: None
        """
        role = RoleProject.objects.get(id=id_role)  # rol a actualizar
        selected_id_perms = [item.id for item in perms]  # permisos elegidos por el usuario
        original_perms = role.perms.all()
        print("Permisos originales: ", original_perms)
        original_permissions_id = [item.id for item in original_perms]  # permisos anteriores
        # permisos a eliminar
        perms_to_remove = list(set(original_permissions_id) - set(selected_id_perms))
        print("permisos a eliminar: ", perms_to_remove)
        perms_to_add = list(set(selected_id_perms) - set(original_permissions_id))

        for perm in perms:
            if perm.id in perms_to_add:
                role.perms.add(perm)

        for perm in original_perms:
            if perm.id in perms_to_remove:
                role.perms.remove(perm)

        role.role_name = name
        role.description = description
        # guardamos los cambios
        role.save()
        print("Editado exitosamente")

    def list_role_permission(self, id_role):
        """
        Funcion para listar los permisos de un rol

        :param id_role: id del rol a buscar

        """
        role = RoleProject.objects.get(id=id_role)  # rol a listar
        permissions = role.perms.all()
        return permissions

    @staticmethod
    def update_user_role(id_user, id_project, roles):
        """
        Actualizar roles de usuario en el proyecto

        :param id_user: id del user a editar
        :param id_project: id del proyecto
        :param roles: los roles actualizados
        """

        selected_id_roles = [item.id for item in roles]  # roles elegidos por el usuario
        project_member = ProjectMember.objects.get(user_id=id_user, project_id=id_project)
        original_roles = RoleProject.objects.get_member_roles(id_user, id_project)
        print("Roles originales: ", original_roles)
        original_roles_id = [item.id for item in original_roles]  # roles anteriores
        # roles a eliminar
        roles_to_remove = list(set(original_roles_id) - set(selected_id_roles))
        print("roles a eliminar: ", roles_to_remove)
        # agregamos los que deban ser agregados
        project_member.roles.add(*roles)
        # eliminamos los roles a ser eliminados
        for role in original_roles:
            if role.id in roles_to_remove:
                project_member.roles.remove(role)

        print("Editado exitosamente")

    @staticmethod
    def has_permissions(user_id, project_id, perm):
        """
        Funcion para verificar si el usuario posee un permiso

        :param user_id: id del usuario
        :param perm: permiso a ser consultado
        """
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm
        return ProjectMember.objects.filter(user_id=user_id, project_id=project_id,
                                            roles__perms__name__in=perms).exists()

    @staticmethod
    def get_deafult_roles(id_project):
        """
        Funcion para obtener un rol scrum master

        :return: Rol Scrum Master
        """

        # get json file and then get permission list

        file = open("projects/fixtures/default_roles_project.json", "r")
        datas = json.loads(file.read())
        for data in datas:
            rol = RoleProject.objects.create(role_name=data['fields']['role_name'],
                                             description=data['fields']['description'], project_id=id_project)
            rol.perms.set(data['fields']['perms'])
            rol.save()
        file.close()


class ProjectManager(models.Manager):

    def create_project(self, name, description, scrum_master):
        # create project
        project = Project.objects.create(name=name, description=description, status=UProject.STATUS_PENDING)

        # attach default roles
        self.create_default_roles(project)

        # assign scrum master
        role = RoleProject.objects.get(project=project, role_name=UProjectDefaultRoles.SCRUM_MASTER)
        member = ProjectMember.objects.create(
            project=project,
            user=scrum_master
        )
        member.roles.add(role)

        return project

    def create_default_roles(self, project):
        RoleProject.objects.get_deafult_roles(id_project=project.id)

    def add_member(self, user_id, roles, project):
        member = ProjectMember.objects.create(
            project=project,
            user_id=user_id
        )
        member.roles.add(*roles)
        return member

    def delete_member(self, user_id, project):
        """

        :param user_id:
        :param project:

        :return: Retorna True si el miembro se pudo eliminar con exito y False si es que no
        """
        # get the current member and then delete just if doesn't have scrum master role
        member = ProjectMember.objects.get(
            project=project,
            user_id=user_id
        )

        result = member.roles.filter(role_name=UProjectDefaultRoles.SCRUM_MASTER).exists()

        if not result:
            project.members.remove(member.user)
            return True
        return False

    def get_project_members(self, id_project):
        return ProjectMember.objects.filter(project_id=id_project)


#########################################################
####################### MODELS ##########################
#########################################################
class PermissionsProj(models.Model):
    """
    Permisos de proyecto
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True)

    def __str__(self):
        return f'{self.name}'


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True)
    members = models.ManyToManyField(User, through='projects.ProjectMember')
    roles = models.ManyToOneRel('projects.RoleProject', on_delete=models.CASCADE, to='projects.Project',
                                field_name='project')
    status = models.CharField(max_length=50)
    cancellation_reason = models.TextField(max_length=500, null=True)
    objects = ProjectManager()

    # def __str__(self) -> str:
    #     text = "{0}"
    #     return text.format(self.name)
    def __str__(self):
        return f"{self.name}"


class RoleProject(models.Model):
    """
    Roles de proyecto
    """
    # campos de los roles en la base de datos
    role_name = models.CharField(max_length=40, null=True)
    description = models.CharField(max_length=250, null=True)
    project = models.ForeignKey('projects.Project', null=True, on_delete=models.CASCADE)
    # asociamos los roles a permisos
    perms = models.ManyToManyField(PermissionsProj)
    objects = RoleProjectManager()

    def __str__(self):
        return f'{self.role_name}'


class ProjectMember(models.Model):
    """
    Miembros de Proyecto
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roles = models.ManyToManyField(RoleProject)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"
