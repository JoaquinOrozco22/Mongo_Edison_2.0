#********************************   FUNCION AGREGAR


#********************************   DEPENDENCIAS
import requests
import json
#import matplotlib.pyplot as plt


#********************************   DATOS DEL SERVIDOR
host = "10.8.21.130"
puerto = 1026


#********************************   ENCABEZADOS Y FORMATO
headers ={'Content-Type': 'application/json', 'Accept': 'application/json'}


#Funcion que recibe el ID y tipo del objeto a consultar y lo regresa en formato JSON.
def datos_agregar_json (id, tipo, lista_atributos):
    datos = {
        "contextElements": [
            {
                "type": tipo,
                "isPattern": "false",
                "id": id,
                "attributes": lista_atributos
            }
        ],
        "updateAction": "APPEND"
    }
    return datos   


#********************************   API
def inserta_datos(datos_json):
    r = requests.post("http://%s:%d/v1/updateContext" % (host,puerto), headers = headers,
        data = json.dumps (datos_json))
    print(r.text)


#********************************   TEST
def test_agrega_habitaciones():
    atributos_h1 = [
        {
            "name" : "temperatura",
            "type" : "float",
            "value" : "20"       
        },
        {
            "name" : "presion",
            "type" : "integer",
            "value" : "720"     
        }
    ]
    atributos_h2 = [
        {
            "name" : "temperatura",
            "type" :"float",
            "value" : "25"       
        },
        {
            "name" : "presion",
            "type" : "integer",
            "value" : "725"     
        }
    ]

    habitacion1=datos_agregar_json("habitacion1","lecturas1", atributos_h1)   
    inserta_datos (habitacion1)



#********************************   MAIN
if __name__  == "__main__":
    test_agrega_habitaciones()

