import picamera
import time
from os import system
from time import sleep
import paho.mqtt.client as mqtt
import uuid






# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("result code is: "+str(rc))
    client.subscribe("droneCommands")
    client.publish("droneCommands", "test data exce")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(str(msg.payload))
    

    


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.138.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()            