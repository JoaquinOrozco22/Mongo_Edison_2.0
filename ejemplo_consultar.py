#********************************       FUNCION BORRAR


#********************************       DEPENDENCIAS
import requests
import json
#import matplotlib.pyplot as plt
import time


#********************************   DATOS DEL SERVIDOR
host = "10.8.21.130"
puerto = 1026


#********************************   ENCABEZADOS Y FORMATO
#Encabezados para indicar el formato de los datos de solicitud y respuesta
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


#********************************   API
def consulta_datos(datos_json):
    r = requests.post("http://%s:%d/v1/queryContext" % (host,puerto), headers = headers,
        data = json.dumps (datos_json))

    #Imprimimos toda la información obtenida 
    print(r.text)


#********************************   TEST
def test_consulta_habitaciones():
    datos=datos_consulta_json("habitacion1", False)
    r=consulta_datos(datos)


#********************************   MAIN
if __name__  == "__main__":
    test_consulta_habitaciones()