#**********************************************************************************************************
#
#Script para agregar objetos y sus datos a la base de datos.
#Asesor: Ing. Jorge Arturo Aguirre Beltran.
#Autor: Joaquin Bernardo Orozco Lopez.
#Instituto Tecnologico de Chihuahua.
#Este documento esta sugeto a derechos de autor. 
#El ITCH, asi como el asesor y el autor no se hacen responsables del mal uso de este material.

#Este script esta diseñado para ejecutarse dentro del sistema embebido, generara los objetos con su 
#respectiva informacion, agregando un total de 10 lecturas a la base de datos.

#**********************************************************************************************************
#                                             Librerias utilizadas.

import requests
import json
import mraa
import time
#from upm import pyupm_jhd1313m1 as lcd
import datetime

#**********************************************************************************************************
#                                             Datos del servidor.

#Direccion IP externa.
#host = "187.188.201.232"
#Direccion IP interna.
host = "10.8.21.130"
#Puerto.
puerto = 1026


#**********************************************************************************************************
#                       Configuracion e inicializacion de los GPIO de la tarjeta EDISON.

#inicializamos AIO
ldr = mraa.Aio(0) 
lm35 = mraa.Aio(1)
pot = mraa.Aio(2)
hum = mraa.Aio(3)

# Configuracion del pin de salida para el servo
servo_pin = mraa.Pwm(6)
servo_pin.period_us(20000)  # Establece el periodo en microsegundos (50 Hz)
servo_pin.enable(True)

#**********************************************************************************************************
#                                             Funciones en formato JSON.

#Encabezados de la llamada, manda y recibe json.
headers ={'Content-Type': 'application/json', 'Accept': 'application/json'}

#Funcion que recibe el objeto con sus datos y lo regresa en estructura JSON.
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

#**********************************************************************************************************
#                                             Funciones de api.

#Funcion que accede al servidor y agrega el objeto con los datos indicados.
def inserta_datos(datos_json):
    r = requests.post("http://%s:%d/v1/updateContext" % (host,puerto), headers = headers,
        data = json.dumps (datos_json))
    #print(r.text)

#**********************************************************************************************************
#                                             Funciones de test.

#Funcion que genera el objeto del tipo edison, con el ID indicado y con los atributos asignados.
def test_agrega_edison(a,b,c,d, hora_actual_str):
    atributos_e13 = [
        {
            "name":"Humedad",
            "type":"integer",
            "value": d     

        },
        {
            "name" : "LDR",
            "type" : "float",
            "value" : a      
        },
        {
            "name":"Potenciometro",
            "type":"float",
            "value": c     
        },
        {
            "name":"Temperatura",
            "type":"integer",
            "value": b     
        },
        {
            "name" : "time",
            "type" : "float",
            "value" : hora_actual_str
        },
    ]

    edison13=datos_agregar_json("e13_lectura"+str(i),"edison13", atributos_e13)
    inserta_datos (edison13)


#**********************************************************************************************************
#                                      Funciones para mover el servomotor.
def move_servo(position):
    duty = position / 180.0 * 0.1 + 0.05  # Calcula el ciclo de trabajo segun la posicion
    servo_pin.write(duty)
    time.sleep(0.5)  # Espera 0.5 segundos para que el servo alcance la posicion


#**********************************************************************************************************
#                                                   Main.

if __name__  == "__main__":
    i=0
    toggle=0
#    EdisonLCD = lcd.Jhd1313m1(0, 0x3E, 0x62)
#    EdisonLCD.setCursor(0,0)
#    EdisonLCD.setColor(0,0,0)
#    EdisonLCD.write("Edison 10")
    try:
        while True:
            i=i+1
            a=ldr.read()
            b=((lm35.read())*455)/1024
            c=round((pot.read()*5)/1023,2)
            d=hum.read()
            
            if toggle==0:
                # Mueve el servo a la posicion inicial (0 grados)
                move_servo(-45)
                #time.sleep(2)  # Espera 2 segundos antes de cambiar la posicion
                toggle=1

            elif toggle==1:
                # Mueve el servo a 180 grados
                move_servo(-15)
                #time.sleep(2)  # Espera 2 segundos antes de cambiar la posicion
                toggle=2

            elif toggle==2:
                # Mueve el servo a 180 grados
                move_servo(30)
                #time.sleep(2)  # Espera 2 segundos antes de cambiar la posicion
                toggle=3
            
            elif toggle==3:
                # Mueve el servo a 180 grados
                move_servo(75)
                #time.sleep(2)  # Espera 2 segundos antes de cambiar la posicion
                toggle=4

            else:
                move_servo(125)
                #time.sleep(2)  # Espera 2 segundos antes de cambiar la posicion
                toggle=0

            hora_actual = datetime.datetime.now().time()
            hora_actual_str = hora_actual.strftime("%H:%M:%S")
            test_agrega_edison(a,b,c,d, hora_actual_str)
            print("--------------------")
            print("Muestra: "+ str(i))
            print("")
            print("Humedad: "+str(d))
            print("")
            print("LDR: "+str(a))
            print("")
            print("Potenciometro: "+str(c))
            print("")   
            print("Temperatura: "+str(b))
            print("--------------------")
            
            if i==10:
                i=0   
            time.sleep(1)

    except KeyboardInterrupt:
        print("Programa detenido manualmente por el usuario")

    finally:
        # Detiene el programa y libera los recursos
        servo_pin.enable(False)
