#!/bin/bash
#echo "Iniciando"
#echo "Clone de git"
cd ..
rm -Rf sgp_g11
git clone https://github.com/Namekusei-Asociados/sgp_g11.git
#
cd sgp_g11
echo "Haciendo checkout del tag $1"
git checkout $1

if [ $2 = 'produccion' ]
then
    echo "Ingresando a Produccion"
    sh deploy/prod.sh $1
else
    echo "Ingresando a Desarrollo"
    sh deploy/dev.sh
fi
python3 manage.py loaddata user.json
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver