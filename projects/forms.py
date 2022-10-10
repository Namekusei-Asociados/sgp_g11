from django.forms import fields, widgets
from django import forms
from projects.models import Project, RoleProject
from sgp import widgets

class ImportRole(forms.Form):
    """
    Implementa un formulario que permite importar roles definidos de un proyecto a otro
    """

    def __init__(self, id_project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_project = id_project
        self.fields['project'] = forms.ModelChoiceField(
            queryset=Project.objects.exclude(id=id_project),
            empty_label='Seleccione un proyecto',
            label='Proyecto',widget=widgets.SelectInput())
