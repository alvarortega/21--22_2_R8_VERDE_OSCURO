import time
import paho.mqtt.client as paho
import logging
import pandas as pd
import random
import time
import uuid
from wwo_hist import retrieve_hist_data
import random
import time
import paho.mqtt.client as mqtt

def on_publish(client, userdata, mid):
    print ("Message published with mid", mid)
    
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code :: ", str(rc))

client =mqtt.Client('BData2')
client.connect('127.0.0.1',1883)

client.on_publish = on_publish
client.on_connect = on_connect

frequency=3
start_date = '11-DEC-2018'
end_date = '23- DEC-2018'
api_key = 'db4656ef4d444f3bbec94155222804'
location_list = ['bilbao']

hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)

bilbao_weather=pd.read_csv("bilbao.csv")
bilbao_weather=bilbao_weather[["tempC","humidity"]].head(70)

temp_horno = random.uniform(50, 100)
vibracion = random.uniform(0, 1000)
infrarojos = random.uniform(0,100)

sensor_temperatura=[]
sensor_vibracion=[]
sensor_infrarojos=[]
sensor_presion=[]
sensor_humo=[]
sensor_imagen=[]
sensor_gafas=[]
sensor_guantes=[]
sensor_chaleco=[]
sensor_casco=[]
sensor_temperatura_ambiente=[]
sensor_humedad=[]


datos=pd.DataFrame(columns=["temp_horno","presion","humo","infrarrojos","vibracion","id_imagen","gafas","guantes","chaleco","casco","temp_ambiente","humedad"])

tt=[]

for i,a,b in zip(range(70),bilbao_weather["tempC"],bilbao_weather["humidity"]):
    temp_horno = round(temp_horno, 2)
    vibracion = round(vibracion, 2)
    infrarojos = round(infrarojos, 2)
    presion= random.choice([1,0])
    humo=random.choice([1,0])
    gafas=random.choice([1,0])
    guantes=random.choice([1,0])
    chaleco=random.choice([1,0])
    casco=random.choice([1,0])
    id_imagen=str(uuid.uuid4())
    temp_ambiente=a
    humedad=b


    
    lista=[]

    lista.append(temp_horno)
    lista.append(vibracion)
    lista.append(infrarojos)
    lista.append(presion)
    lista.append(humo)
    lista.append(gafas)
    lista.append(guantes)
    lista.append(chaleco)
    lista.append(casco)
    lista.append(id_imagen)
    lista.append(temp_ambiente)
    lista.append(humedad)

    variacion_temp = random.uniform(0, 1)
    variacion_vibracion = random.uniform(0,5)
    variacion_infrarojos = random.uniform(0,5)


    def suma(temp_horno,variacion_temp):
        temp_horno=temp_horno + variacion_temp
        return temp_horno 
    
    def resta(temp_horno,variacion_temp):
        temp_horno=temp_horno - variacion_temp
        return temp_horno

    op=[suma,resta]
    
    funcion=random.choice(op)
    temp_horno=funcion(temp_horno,variacion_temp)
    if funcion == suma:
        vibracion = variacion_vibracion + vibracion
    else:
        vibracion = vibracion - variacion_vibracion
    #infrarojos = variacion_infrarojos
    #Si sube que el otro tambien lo haga
    if temp_horno < -10:
        temp_horno = -10
    elif temp_horno > 40:
        temp_horno = 40
    if vibracion < 0:
        vibracion = 0
    elif vibracion > 100:
        vibracion = 100
    if infrarojos < 0:
        infrarojos = 0
    elif infrarojos > 100:
        infrarojos = 100
    message = str(temp_horno)+' '+str(presion)+' '+str(infrarojos)+' '+str(vibracion)+' '+str(id_imagen)+' '+str(gafas)+' '+str(guantes)+' '+str(chaleco)+' '+str(casco)+' '+str(temp_ambiente)+' '+str(humedad)

    time.sleep(2.0)
    lista=["maquina_sensor_01","maquina_sensor_02","maquina_sensor_03"] 
    logging.info(f"Introducimos datos: {message}")    
    client.publish(random.choice(lista), message,qos=0)

client.disconnect()