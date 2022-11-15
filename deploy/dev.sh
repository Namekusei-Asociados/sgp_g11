#!/bin/bash

# RELLENAMOS LAS VARIABLES DE ENTORNO
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


#echo "Ingresar variables de entorno..."
#echo "INSTALANDO BACKEND"
echo "Creando entorno virtual..."
virtualenv -p python3 venv
echo ""
echo "Entrando al venv..."
. ./venv/bin/activate
echo ""
echo "Intalando dependecias..."
pip install -r requirements.txt
echo ""
echo "Desea prepoblar la DB con datos de prueba? (y/n)"
read prepoblar
if [ $prepoblar = "y" ]
then
    echo 'aaaa'
    echo "Poblando DB con datos de prueba..."
    cd deploy
    sh restore_db.sh
else
    echo "Poblando DB con el estado inicial..."
    cd deploy
    sh restore_db.sh
fi