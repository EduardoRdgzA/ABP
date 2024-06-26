#!/bin/zsh
#Script para actualizar el repositorio de GitHub. 
#Autor: Eduardo Rdgz-Ávila.
#Sistema de actualización de repositorios de GitHub 'SARGH'
commit=$1

echo "\e[1mgit status:\e[0m"
git status
echo "Espera 2 segundos"
sleep 2

echo -e "\n\e[1mgit add .:\e[0m"
git add .
echo "Espera 2 segundos"
sleep 2

echo -e "\n\e[1mgit status:\e[0m"
git status
echo "Espera 2 segundos"
sleep 2

echo -e "\n\e[1mgit commit:\e[0m"
git commit -m "$commit"
echo "Espera 2 segundos"
sleep 2

echo -e "\n\e[1mgit pull:\e[0m"
git pull origin main
sleep 2

echo -e "\n\e[1mgit push:\e[0m"
git push origin main
echo -e "\n\e[1;32mgitup listo\e[0:32m"
