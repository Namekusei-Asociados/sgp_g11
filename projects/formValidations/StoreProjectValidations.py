from django.forms import ModelForm
from projects.models import Project
from django.contrib.auth.models import User


# define the class of a form
class PostForm(ModelForm):
    """
    CLase para validacion de datos en el backend
    Valida los datos recibidos en el formulario de creacion de proyecto
    """

    class Meta:
        # write the name of models for which the form is made
        model = Project

        # Custom fields
        fields = ["name", "description", "members"]

    # this function will be used for the validation
    def clean(self):

        # data from the form is fetched using super function
        super(PostForm, self).clean()

        # extract the username and text field from the data
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')
        user_id = self.cleaned_data.get('user')

        # conditions to be met for the username length
        if len(name) < 4:
            self._errors['name'] = self.error_class([
                'EL nombre debe de tener un minimo de 4 caracteres'])

        if 10 > len(description) > 500:
            self._errors['description'] = self.error_class([
                'Ingrese un minimo de 4 caracteres y maximo de 500'])

        try:
            if not User.objects.filter(id=user_id).exists():
                self._errors['user'] = self.error_class([
                    'EL usuario seleccionado no existe'])
        except:
            self._errors['user'] = self.error_class([
                'EL usuario seleccionado no existe'])

        # return any errors if found
        return self.cleaned_data
