from django.shortcuts import render

# Create your views here.
def create(request):
    """
    Retorna un formulario de creacion de proyectos
    :param request:
    :return: documento html
    """
    return render(request,'create.html')

