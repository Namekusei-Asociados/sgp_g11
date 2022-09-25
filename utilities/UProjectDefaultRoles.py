from projects.models import RoleProject


class UProjectDefaultRoles:
    """
        Esta clase contiene utilidades generales para la logica relacionada a la roles
    """
    SCRUM_MASTER = "Scrum Master"

    @staticmethod
    def get_scrum_master() -> RoleProject:
        name = UProjectDefaultRoles.SCRUM_MASTER
        description = "Este rol es de Scrum Master"
        permissions_list = [1, 2]
        rol = RoleProject.objects.create(role_name=name, description=description,project=None)
        rol.perms.set(permissions_list)
        return rol
