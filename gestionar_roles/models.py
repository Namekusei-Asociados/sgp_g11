from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from guardian.shortcuts import assign_perm, remove_perm


# Create your models here.
class Role(models.Model):

    # campos de los roles en la base de datos
    id = models.IntegerField
    role_name = models.CharField(max_length=40, null=False)
    description = models.CharField(max_length=250, null=True)
    # asociamos el rol a la tabla de grupos
    role_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False)
    type = models.IntegerField    #1- Sistema, 2- Proyecto
    def __str__(self):
        return self.role_name

    #funcion para crear roles permisos por modelo
    def create_role(self, name, description, type, *permissions):
        self.role_name=name; self.description=description; self.type=type;
        self.save();
        group_role, created = Group.objects.get_or_create(name=f'{name}')
        if created:
            self.attach_permissions(group_role, permissions)

    #funcion encargada de asignar permisos a los grupos de roles
    def attach_permissions(self, group_role, *permissions):
        for permiso_temp in permissions:
            if Permission.objects.filter(name=permiso_temp).exists():
                assign_perm(permiso_temp, group_role)
            else:
                print("el permiso no existe")

    #funcion encargada de asignar permisos a los grupos de roles
    def dettach_permissions(self, group_role, *permissions):
        for permiso_temp in permissions:
            if Permission.objects.filter(name=permiso_temp).exists():
                remove_perm(permiso_temp, group_role)
            else:
                print("el permiso no existe")

    #funcion para asignar rol a usuario
    def assign_role_to_user(self, id_role, user):
        try:
            rol = Role.objects.filter(id=id_role)
            grupo = Group.objects.get(id=self.role_group.id)
            grupo.user_set.add(user)
        except Role.DoesNotExist as error:
            print("El rol no existe"+id_role)
    #funcion para asignar rol a usuario
    def unassign_role_to_user(self, id_role, user):
        try:
            role = Role.objects.filter(id=id_role)
            group_role = Group.objects.get(id=role.role_group.id)
            group_role.user_set.remove(user)
        except Role.DoesNotExist as error:
            print("El rol no existe"+id_role)

    #funcion para eliminar un rol
    def delete_role(self, id_role):
        try:
            role= Role.objects.filter(id=id_role)
            group_role=Group.objects.filter(id=role.role_group.id)
        except Role.DoesNotExist as error:
            print("El rol no existe"+id_role)

    # funcion para crear roles de permisos por objeto
    def create_role_per_object(self, name, description, type, *permissions, object):
        #rellenamos los campos
        self.role_name = name; self.description = description; self.type = type;
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

    #funcion para listar los roles existentes
    def list_roles(self):
        return self.objects.all()

