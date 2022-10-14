from django import forms


class SelectInput(forms.Select):
    def __init__(self, attrs={}, **kwargs):
        attrs['class'] = 'form-control'
        attrs['style'] = 'width: 100%'
        super().__init__(attrs, **kwargs)


class SelectMultipleInput(forms.Select):
    def __init__(self, attrs={}, **kwargs):
        attrs['class'] = "select2"
        attrs['style'] = 'width: 100%'
        attrs['multiple'] = 'multiple'
        attrs['data-dropdown-css-class'] = "select2-purple"
        attrs['data-placeholder'] = "Seleccione una opcion"
        super().__init__(attrs, **kwargs)
