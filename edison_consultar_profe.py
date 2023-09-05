#**********************************************************************************************************
#
#Script de la funcion para consultar los objetos en la base de datos (version profesor).
#Asesor: Ing. Jorge Arturo Aguirre Beltran.
#Autor: Joaquin Bernardo Orozco Lopez.
#Instituto Tecnologico de Chihuahua.
#Este documento esta sugeto a derechos de autor. 
#El ITCH, asi como el asesor y el autor no se hacen responsables del mal uso de este material.

#Este script esta diseñado para ejecutarse fuera del sistema embebido, se encarga de obtener la 
#informacion de la base de datos y graficarla. Esta version se llama "Profesor" debido a que este
#script muestra puede mostrar la informacion de todos los sistemas embebidos asociados al servidor.

#**********************************************************************************************************
#                                             Librerias utilizadas.
import requests
import json
import matplotlib.pyplot as plt
import sys


#**********************************************************************************************************
#                                             Datos del servidor.

#Direccion IP interna del servidor.
#host = "10.8.21.130"
#Direccion IP externa del servidor.
host = "187.188.201.232"
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


#Funcion que recibe el ID y tipo del objeto a consultar y lo regresa en formato JSON.
def datos_consulta_json (id, tipo, es_expreg=False):
    val_expreg = "false"
    if es_expreg:
        val_expreg = "true"
    datos = {
        "entities":[
            {
                "type": tipo,
                "isPattern": val_expreg,
                "id": id
            }
        ]
    }
    return datos

#**********************************************************************************************************
#                                             Funciones de api.

#Funcion que accede y obtiene la informacion del objeto con el tipo y ID correspondiente.
def consulta_datos(datos_json):
    r = requests.post("http://%s:%d/v1/queryContext" % (host,puerto), headers = headers,
        data = json.dumps (datos_json))
    
    #Imprimimos toda la información de la tarjeta seleccionada en formato JSON
    #print(r.text)

    #Utilizamos el metodo loads de la libreria JSON para almacenamar en un 
    # diccionario la cadena de caracteres obtenida del servidor.
    diccionario = json.loads(r.text)

    #Guardamos los valores correspondientes a la humedad en una lista, 
    #despues generamos una lista nueva con los valores convertidos de string a float
    humedadO = [record['contextElement']['attributes'][0]['value'] for record in diccionario['contextResponses']]
    humConv=[float(elemento)for elemento in humedadO]

    #Guardamos los valores correspondientes el LDR en una lista, 
    #despues generamos una lista nueva con los valores convertidos de string a float
    ldrO = [record['contextElement']['attributes'][1]['value'] for record in diccionario['contextResponses']]
    ldrConv=[float(elemento)for elemento in ldrO]

    #Guardamos los valores correspondientes del potenciometro en una lista, 
    #despues generamos una lista nueva con los valores convertidos de string a float
    potenciometroO = [record['contextElement']['attributes'][2]['value'] for record in diccionario['contextResponses']]
    potConv=[float(elemento)for elemento in potenciometroO]

    #Guardamos los valores correspondientes a la temperatura en una lista, 
    #despues generamos una lista nueva con los valores convertidos de string a float
    temperaturaO = [record['contextElement']['attributes'][3]['value'] for record in diccionario['contextResponses']]
    tempConv=[float(elemento)for elemento in temperaturaO]

    #Guardamos los valores correspondientes a la hora en una lista, 
    horas = [record['contextElement']['attributes'][4]['value'] for record in diccionario['contextResponses']]


    #Generamos dos diccionarios los cuales funcionan como los casos en un switch case.
    #Diccionario para la opcion de la grafica a mostrar
    opciones = {
        1: lambda: test_grafica(horas, humConv, etiqueta,ylimM),
        2: lambda: test_grafica(horas, ldrConv, etiqueta,ylimM),
        3: lambda: test_grafica(horas, potConv, etiqueta,ylimM),
        4: lambda: test_grafica(horas, tempConv, etiqueta,ylimM)
    }
    #Diccionario de la variable seleccionada
    titulo = {
        1: "Humedad",
        2: "LDR",
        3: "Potenciometro",
        4: "Tempetura"
    }
    #Diccionario de la variable seleccionada
    limite = {
        1: 1023,
        2: 1023,
        3: 6,
        4: 50
    }
    #Variable para la grafica deseada a mostrar
    grafica=0
    #Ciclo while para repetir el menu en caso de introducir una opcion invalida
    while(grafica not in opciones):
        #Menu para seleccionar la grafica a mostrar
        print("¿Cual grafico quieres mostrar?")
        print("1-. Humedad")
        print("2-. LDR")
        print("3-. Potenciometro")
        print("4-. Temperatura")
        grafica=int(input())
        if (grafica not in opciones):
            print("Opción no válida")

    # Ejecutar la función correspondiente a la opción seleccionada
    if grafica in titulo:
        etiqueta = titulo[grafica]
    
    # Ejecutar la función correspondiente a la opción seleccionada
    if grafica in limite:
        ylimM = limite[grafica]

    # Ejecutar la función correspondiente a la opción seleccionada
    if grafica in opciones:
        opciones[grafica]()

    
#**********************************************************************************************************
#                                             Funciones de test.

#Funcion que Guarda el ID y tipo del objeto a consultar.
def test_consulta_edison(numT):
    datos=datos_consulta_json(("e"+numT+"_lectura*"),"edison"+numT, True)
    r=consulta_datos(datos)


#**********************************************************************************************************
#                                             Funciones de test_graficar.

def test_grafica(y,x, etiqueta,ylimM):
    plt.plot(y, x)
    plt.suptitle('Edison'+numT)
    plt.ylabel(etiqueta)
    plt.ylim(0,ylimM)
    plt.xlabel('Horas')
    plt.xlim(0,10)
    plt.show()


#**********************************************************************************************************
#                                                   Main.

if __name__  == "__main__":

    while (True):
        print("")
        print("")
        print("¿Cual numero de tarjeta edison deseas buscar?")
        print("1-. Edison8")
        print("2-. Edison10")
        print("3-. Edison11")
        print("4-. Edison13")
        print("0-. Salir")
        numT=int(input())
        
        # Ejecutar la función correspondiente a la opción seleccionada
        if numT in tarjeta:
            numT = tarjeta[numT]
            test_consulta_edison(numT)
        elif numT==0:
            sys.exit("Finalizando programa")
        else:
            print("Opción no válida")


        



