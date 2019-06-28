import RPi.GPIO as GPIO
import time
from os import system
from time import sleep
import paho.mqtt.client as mqtt
import json

channel           = 17 # the selected gpio data pin
topic_to_server   = "drone_web_console_server"# when sending data to the server
topic_from_server = "server_data_to_seismic_1"# when recieving data from the server to seismic sensor 1
server_url        = "18.222.225.98"
server_port       = 1883

# method for seismic sensor
def seismic_callback(channel):
	if GPIO.input(channel):
		#make json object to send
		x={
			"type":"seismic_sensor_reading",
			"value":"100"
		  }
		client.publish(topic_to_server, json.dumps(x))
		print("data published")
	else:
		#make json object to send
		x={
			"type":"seismic_sensor_reading",
			"value":"100"
		  }
		client.publish(topic_to_server, json.dumps(x))
		print("data published")

# mqtt on connect callback
def on_connect(client, userdata, flags, rc):
    print("Mqtt connected with result code "+str(rc))
    client.subscribe(topic_from_server)#listen for messages from the server
    print("mqtt connected")

# mqtt onmessage recieved
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))# display the message from the server


#seismic sensor gpio setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN)
GPIO.add_event_detect(channel,GPIO.BOTH,bouncetime=300)
GPIO.add_event_callback(channel,seismic_callback)

#mqtt client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(server_url, server_port, 60)


print("Setup complete:\n")
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()        



#while True:
#	time.sleep(1)#wait 1 second




