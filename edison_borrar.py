#**********************************************************************************************************
#
#Script con la funcion para eliminar los objetos de la base de datos.
#Asesor: Ing. Jorge Arturo Aguirre Beltran.
#Autor: Joaquin Bernardo Orozco Lopez.
#Instituto Tecnologico de Chihuahua.
#Este documento esta sugeto a derechos de autor. 
#El ITCH, así como el asesor y el autor no se hacen responsables del mal uso de este material.

#Este script esta diseñado para eliminar la informacion de la base de datos, asi como el 
#objeto seleccionado. 

#**********************************************************************************************************
#                                             Librerias utilizadas.
import requests
import json
import matplotlib.pyplot as plt
import time
import sys

#**********************************************************************************************************
#                                             Datos del servidor.

#Direccion IP externa.
#host = "187.188.201.232"
#Direccion IP interna.
host = "10.8.21.130"
#Puerto.
puerto = 1026

#**********************************************************************************************************
#                                 Listas, diccionarios o variables de uso global.

#Diccionario para la selección de la tarjeta edison deseada
tarjeta = {
    1: "8",
    2: "10",
    3: "11",
    4: "13",
}

#**********************************************************************************************************
#                                             Funciones en formato JSON.

#Encabezados de la llamada, manda y recibe json
headers ={'Content-Type': 'application/json', 'Accept': 'application/json'}

#Funcion que accede y elimina la informacion del objeto con el tipo y ID correspondiente.
def borra_datos(id):
    r = requests.delete("http://%s:%d/v1/contextEntities/%s" % (host,puerto,id), headers = headers)
    return r.text

#Funcion que genera el ID para identificar el elemento en la base de datos, hace el llamado a la funcion API.
def test_borra_datos(i, numT):
    id=("e"+numT+"_lectura"+str(i))
    borra_datos(id)

#**********************************************************************************************************
#                                                   Main.

if __name__  == "__main__":
    #Se despliega un menu para mostrar las opciones disponibles.
    print("")
    print("")
    print("Qué lecturas quiere borrar?")
    print("1-. Edison8")
    print("2-. Edison10")
    print("3-. Edison11")
    print("4-. Edison13")
    numT=int(input())
    print("")
    print("")
    print("Borrando...")

    # Ejecutar la función correspondiente a la opción seleccionada
    if numT in tarjeta:
        numT = tarjeta[numT]
    else:
        print("Opción no válida")
        sys.exit("Finalizando programa")
    
    i=0
    while(True):
        i=i+1
        test_borra_datos(i,numT)
        print(i)
        if(i==10):
            print("Borrado finalizado")
            sys.exit("Finalizando programa")
 