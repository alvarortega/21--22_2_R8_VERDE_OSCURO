import time
import paho.mqtt.client as paho
import logging

# Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s > %(name)s > %(levelname)s: %(message)s')


def on_connect(client, userdata, flags, rc):
    logging.debug(f'Connected with result code {rc}')
    logging.debug("Subscribing")
    client.subscribe("#")  # Warning! (read comment below)
    logging.debug("Subscribed")



def on_message(client, userdata, message):
    logging.info(f'On message:\n\nMessage: {message.payload.decode("utf-8")}\nTopic: {message.topic}\n')


# Connection
broker = "localhost"
client = paho.Client("client-subscribe")
client.username_pw_set(username="mosquitto", password="mosquitto")
client.on_connect = on_connect
client.on_message = on_message
logging.debug(f'Connecting to broker {broker}')
client.connect(broker)
logging.debug("Start loop")
client.loop_forever()
