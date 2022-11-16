#!/bin/bash
# Descripcion: Despliega el develop
# Parametros:
# 	$1 -> tag a deployar
# Retorno:
#   Ninguno
dev(){
    # .env
    {
        echo ''
        echo 'SECRET_KEY=django-insecure-30q7!q)cw7628s(d8k3wn6w%i+=ug=sglg5!6s-m1lo3e12uk('
        echo 'ENVIRONMENT=local'
        echo 'CLIENT_ID: 494703356382-014c3nlin2rdr5oh96u3dpphm9dc1lu9.apps.googleusercontent.com'
        echo 'CLIENT_SECRET: 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'

        echo 'DATABASE_NAME=sgp_db'
        echo 'DATABASE_USER=postgres'
        echo 'DATABASE_PASSWORD=admin'
        echo 'DATABASE_HOST=localhost'
        echo 'DATABASE_PORT=5432'
        echo 'DEBUG=True'
    } > .env
    echo "Creando entorno virtual..."
    virtualenv -p python3 venv
    echo ""
    ls
    chmod +x ./venv/bin/activate
    echo "Entrando al venv..."
    . ./venv/bin/activate
    #echo "Instalando dependecias..."
    pip install -r requirements.txt
    echo ""
    echo "Desea prepoblar la DB con datos de prueba? (y/n)"
    read prepoblar
    if [ $prepoblar = "y" ]
    then
        echo "Poblando DB con datos de prueba..."
        sh deploy/restore_db.sh
        python3 manage.py loaddata users_notario.json
        python3 manage.py makemigrations
        python3 manage.py migrate
        python3 manage.py runserver
    else
        echo "Poblando DB con el estado inicial..."


	set -e
	set -u

	export DBHOST=localhost
	export DBPORT=5432

	psql \
	    -X \
	    -U postgres \
	    password=admin \
	    -h $DBHOST \
	    -f deploy/create_db.sql \
	    --echo-all \
	    --set AUTOCOMMIT=off \
	    --set ON_ERROR_STOP=on \
	    --set VERBOSITY=verbose \
	    --set PGPASSWORD='admin' \
	    --set PGOPTIONS='--client-min-messages=warning' \
	\q


        sh scripts/Permisos.sh
        python3 manage.py runserver
    fi
}
# Variables
pathProyecto="./sgp_g11"
# Parametros desde la linea de comandos
tag=$1
tipoEntorno=$2

echo "Iniciando"
echo "Clone de git"
if [ -d $pathProyecto ]
then
    rm -Rf $pathProyecto
fi
git clone https://github.com/Namekusei-Asociados/sgp_g11.git
cd $pathProyecto

echo "Haciendo checkout del tag $tag"
git checkout $tag

if [ $tipoEntorno == 'produccion' ]
then
   echo "Ingresando a Produccion"

elif [ $tipoEntorno == 'desarrollo' ]
then
   echo "Ingresando a Desarrollo"
   dev
else
    echo 'Opcion incorrecta'
    exit
fi
