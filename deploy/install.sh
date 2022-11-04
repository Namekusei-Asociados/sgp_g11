echo "Iniciando"
#echo "Clonando repositorio git"
#rm -Rf sgp_g11
#git clone https://github.com/Namekusei-Asociados/sgp_g11.git
cd sgp_g11
echo "Haciendo checkout del tag $1"
git checkout $1
if [ $2 = 'produccion' ]
then
    echo "Ingresando a Produccion"
    sh prod.sh $1
else
    echo "Ingresando a Desarrollo"
    sh dev.sh
fi
