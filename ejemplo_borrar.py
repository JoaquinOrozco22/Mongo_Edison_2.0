#********************************   FUNCION BORRAR


#********************************   DEPENDENCIAS
import requests
#import json
#import matplotlib.pyplot as plt

#********************************   DATOS DEL SERVIDOR
host = "10.8.21.130"
puerto = 1026

#********************************   ENCABEZADOS 
headers ={'Content-Type': 'application/json', 'Accept': 'application/json'}

#********************************   API
def borra_datos(id):
    r = requests.delete("http://%s:%d/v1/contextEntities/%s" % (host,puerto,id), headers = headers)
    return r.text

#********************************   TEST
def test_borra_datos():
    id="habitacion1"
    borra_datos(id)

#********************************   MAIN
if __name__  == "__main__":
    test_borra_datos()
 