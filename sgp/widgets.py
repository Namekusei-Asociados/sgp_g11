from django import forms


class SelectInput(forms.Select):
    def __init__(self, attrs={}, **kwargs):
        attrs['class'] = 'form-control select2'
        attrs['style'] ='width: 100%'
        super().__init__(attrs, **kwargs)
