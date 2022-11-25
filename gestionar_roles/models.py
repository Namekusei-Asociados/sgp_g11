from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q


class Permissions(models.Model):
    name = models.CharField(max_length=40, null=True)
    description = models.CharField(max_length=250, null=True)


class RoleSystemManager(models.Manager):
    # funcion para crear roles permisos por modelo
    def create_role(self, name, description, permissions_list):
        """
        Crear un nuevo rol del sistema

        :param name: nombre del rol
        :param description: descripcion del rol
        :param permissions_list: lista de permisos a ser asignados al rol
        """
        if not RoleSystem.objects.filter(role_name=name).exists():
            role = RoleSystem.objects.create(
                role_name=name,
                description=description
            )
            role.save()
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
        role = self.get_role_by_id(id_role=id_role)
        for permiso_temp in permissions_list:
            role.perms.add(permiso_temp)

    # funcion para verificar si el usuario tiene los permisos requeridos
    @staticmethod
    def has_permissions(user_id, perm):
        """
        Funcion para verificar si el usuario posee un permiso

        :param user_id: id del usuario
        :param perm: permiso a ser consultado
        :return:
        """
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm
        return RoleSystem.objects.filter(user=user_id, perms__name__in=perms).exists()

    def has_role(self, user_id, id_role):
        """
        Funcion para verificar si un usuario posee un rol

        :param user_id: id del usuario
        :param role_name: nombre del rol a ser buscado
        :return:
        """
        return RoleSystem.objects.filter(user=user_id, id=id_role).exists()

    def get_role_by_id(self, id_role):
        """
        Obtiene el rol segun  el id
        :param id_role: id del rol
        """
        return RoleSystem.objects.get(id=id_role)

    @staticmethod
    def assing_role_to_user(role, user):
        """
        Asignar rol a usuario
        :param role: rol a ser asignado
        :param user: usuario al cual sera asignado el rol
        """
        role.user.add(user)

    @staticmethod
    def update_role_user(new_role, user):
        """
        Asignar rol a usuario

        :param new_role: rol a ser deasignado
        :param user: usuario al cual sera asignado el rol
        """
        try:
            role = RoleSystem.objects.filter(user=user).first()
            role.user.remove(user)
        except RoleSystem.DoesNotExist:
            pass
        new_role.user.add(user)
        print("Actualizado exitosamente")

    def list_roles(self):
        """
        Funcion para listar todos los roles del sistema
        """
        return RoleSystem.objects.all()

    @staticmethod
    def delete_role(id_role):
        """
        Eliminar un rol de sistema

        :param id_role: id del rol a ser eliminado
        """
        role = RoleSystem.objects.get(id=id_role)
        if role.user.all().count() > 0 and role.role_name != 'Admin':
            role.delete()
            print("Eliminado exitosamente")
            return True
        else:
            return False

    @staticmethod
    def update_role(id_role, name, description, perms):
        """
        Funcion para editar un rol de sistema

        :param id_role: id del rol a editar
        :param name: nombre actualizado
        :param description: descripcion actualizada
        :param perms: lista de permisos actualizados

        :return: None
        """
        role = RoleSystem.objects.get(id=id_role)  # rol a actualizar
        selected_id_permissions = [item.id for item in perms]  # permisos elegidos por el usuario
        original_permissions = role.perms.all()
        print("Permisos originales: ", original_permissions)
        original_permissions_id = [item.id for item in original_permissions]  # permisos anteriores
        # permisos a eliminar
        perms_to_remove = list(set(original_permissions_id) - set(selected_id_permissions))
        print("permisos a eliminar: ", perms_to_remove)
        perms_to_add = list(set(selected_id_permissions) - set(original_permissions_id))

        for perm in perms:
            if perm.id in perms_to_add:
                role.perms.add(perm)

        for perm in original_permissions:
            if perm.id in perms_to_remove:
                role.perms.remove(perm)

        if name:
            role.role_name = name
        if description:
            role.description = description
        # guardamos los cambios
        role.save()
        print("Editado exitosamente")

    def list_role_permission(self, id_role):
        """
        Funcion para listar los permisos de un rol

        :param id_role: id del rol a editar

        """
        role = RoleSystem.objects.get(id=id_role)  # rol a listar
        permissions = role.perms.all()
        return permissions


# Create your models here.
class RoleSystem(models.Model):
    """
    Roles de sistema
    """
    # campos de los roles en la base de datos
    role_name = models.CharField(max_length=40, null=True)
    description = models.CharField(max_length=250, null=True)
    # asociamos el rol a la tabla de usuarios
    user = models.ManyToManyField('accounts.User', related_name='role')

    # asociamos los roles a permisos
    perms = models.ManyToManyField(Permissions)

    objects = RoleSystemManager()

    def __str__(self):
        return f'{self.role_name}'
