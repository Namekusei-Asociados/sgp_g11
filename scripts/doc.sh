#!/bin/bash
#nos ubicamos en la carpeta de documentación
cd docs
#borramos la carpeta anterior
rm -rf _build
#conservamos el index.rst
mv index.rst index.rst.temp
#eliminamos los demas rst
rm *.rst
#recuperamos el rst
mv index.rst.temp index.rst
#agregamos las apps en los toctrees
#sed -i 's/:caption: Contents:/&\n   accounts/' './index.rst'
#sed -i 's/:caption: Contents:/&\n   gestionar_roles/' './index.rst'
#sed -i 's/:caption: Contents:/&\n   projects/' './index.rst'
#sed -i 's/:caption: Contents:/&\n   sgp/' './index.rst'
#sed -i 's/:caption: Contents:/&\n   sprints/' './index.rst'
#sed -i 's/:caption: Contents:/&\n   type_us/' './index.rst'
#sed -i 's/:caption: Contents:/&\n   user_story/' './index.rst'
#sed -i 's/:caption: Contents:/&\n/' './index.rst'
#ejecutamos
sphinx-apidoc -o . ..
make html

#  Abrimos en el navegador
xdg-open "_build/html/index.html"