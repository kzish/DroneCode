import time
from adxl345 import ADXL345
import paho.mqtt.client as mqtt
import json


topic_to_server   = "drone_web_console_server"# when sending data to the server
topic_from_server = "server_data_to_seismic_1"# when recieving data from the server to seismic sensor 1
server_url        = "192.168.138.1"
server_port       = 1883


# Create an ADXL345 instance.
adxl345 = ADXL345()
axes = adxl345.get_axes()


# mqtt on connect callback
def on_connect(client, userdata, flags, rc):
    print("Mqtt connected with result code "+str(rc))
    client.subscribe(topic_from_server)#listen for messages from the server
    print("mqtt connected")

# mqtt onmessage recieved
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))# display the message from the server



#mqtt client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(server_url, server_port, 60)


print("Setup complete:\n")    

while True:
    x=axes['x']
    y=axes['y']
    z=axes['z']
    json_data={
			"type":"seismic_sensor_reading",
			"x_value":x,
			"y_value":y,
			"z_value":z
		  }
		client.publish(topic_to_server, json.dumps(json_data))
		print("data published")
    # Wait half a second and repeat.
    time.sleep(0.25)




