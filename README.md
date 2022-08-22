# Project management system

#### Following the next steps to run the project 

First install all dependencies comming from requirements.txt 

Then run the following commands

```
  - python3 manage.py makemigrations
  - python3 manage.py migrate
  - python3 manage.py runserver
  
```

!Remember to add your `.env` file for your local environment!

# Sistema de Gestión de Proyectos 


## Testeo
Para ejecutar el testeo ejecutar el comando 
```
pytest
```

## Documentación
Para generar la documentación automática, ejecutar los comandos en /docs/
```
sphinx-apidoc -o . ..
make html
