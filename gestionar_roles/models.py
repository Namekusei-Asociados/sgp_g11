from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from guardian.shortcuts import assign_perm, remove_perm

class RoleManager(models.Manager):
    # funcion para crear roles permisos por modelo
    def create_role(self, name, description, type_role, permissions_list):
        group_role = Group.objects.create(name=name)
        role = Role.objects.create(
            role_name=name,
            description=description,
            type_role=type_role,
            role_group=group_role
        )
        role.save()
        self.attach_permissions(role.id, permissions_list)
        print('rol creado exitosamente')

    # funcion encargada de asignar permisos a los grupos de roles
    def attach_permissions(self, id_role, permissions_list):
        role = Role.objects.get(id=id_role)
        print(role)
        nombre=role.role_name
        group_role = Group.objects.get(name=nombre)
        for permiso_temp in permissions_list:
            group_role.permissions.add(permiso_temp)


    # funcion encargada de asignar permisos a los grupos de roles
    def dettach_permissions(self, id_role, permissions_list):
        role = Role.objects.get(id=id_role)
        group_role = Group.objects.get(name=role.role_name)
        for permiso_temp in permissions_list:
            remove_perm(permiso_temp, group_role)

    #verifica la existencia de un permiso en la base de datos
    def exist_perm(self, perm):
        if Permission.objects.filter(codename=perm).exists():
            return True
        else:
            return False

    # funcion para asignar rol a usuario
    def assing_role_to_user(self, id_role, user):
        try:
            role = Role.objects.get(id=id_role)
            group_role = Group.objects.get(name=role.role_name)
            group_role.user_set.add(user)
        except Role.DoesNotExist as error:
            print("El rol no existe" + id_role)


    # funcion para asignar rol a usuarioFo
    def unassing_role_to_user(self, id_role, user):
        try:
            role = Role.objects.get(id=id_role)
            group_role = Group.objects.get(name=role.role_name)
            group_role.user_set.remove(user)
            print("Rol eliminado")
        except Role.DoesNotExist as error:
            print("El rol no existe" + id_role)


    # funcion para eliminar un rol
    def delete_role(self, id_role):
        try:
            role = Role.objects.get(id=id_role)
            group_role = Group.objects.get(name=role.role_name)
            group_role.delete()
        except Role.DoesNotExist as error:
            print("El rol no existe" + id_role)


    # funcion para crear roles de permisos por objeto
    def create_role_per_object(self, name, description, type, *permissions, object):
        # rellenamos los campos
        self.role_name = name;
        self.description = description;
        self.type = type;
        group_role, created = Group.objects.get_or_create(name=f'{id}+{object.id}')
        if created:
            self.attach_permissions(group_role, permissions, object)

    # funcion encargada de asignar permisos a los grupos de roles
    def attach_permissions_per_object(self, group_role, *permissions, object):
        for permiso_temp in permissions:
            if Permission.objects.filter(name=permiso_temp).exists():
                assign_perm(permiso_temp, group_role, object)
            else:
                print("el permiso no existe")

    ######LISTAS######
    #Roles a los que pertenece un usuario
    def list_user_roles(self, user):
        return user.groups.all()

    # funcion para listar los roles existentes
    def list_roles(self):
        return Role.objects.all()

    # funcion para listar permisos del rol
    def list_roles_perms(self, id_role):
        try:
            role = Role.objects.get(id=id_role)
            group_role = Group.objects.get(namei=role.role_name)
            return group_role.permissions.all()
        except Role.DoesNotExist as error:
            print("El rol no existe" + id_role)

# Create your models here.
class Role(models.Model):

    # campos de los roles en la base de datos
    role_name = models.CharField(max_length=40, null=True)
    description = models.CharField(max_length=250, null=True)
    # asociamos el rol a la tabla de grupos
    type_role = models.IntegerField()    #1- Sistema, 2- Proyecto
    role_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    objects=RoleManager()

    def __str__(self):
        return self.role_name

    class Meta:
        permissions = (
            ('list_role', 'Can list role'),
        )