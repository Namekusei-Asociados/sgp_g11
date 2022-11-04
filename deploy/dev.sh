#!/bin/bash
echo "Ingresar variables de entorno..."

echo "INSTALANDO BACKEND"
echo "Creando entorno virtual..."
virtualenv -p python3 venv
echo ""
echo "Ingresando al entorno virtual..."
source venv/bin/activate
echo ""
echo "Intalando dependecias..."
#pip install -r requirements.txt
echo ""
echo "Desea prepoblar la DB con datos de prueba? (y/n)"
read prepoblar
if [ $prepoblar = "y" ]
then
    echo "Poblando DB con datos de prueba..."
    sh ./restore_db.sh
else
    echo "Poblando DB con el estado inicial..."
    sh ./restore_db.sh
fi