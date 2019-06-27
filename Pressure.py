# Importing modules
import spidev # To communicate with SPI devices
from time import sleep  # To add delay
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json

channel           = 0 # the selected gpio data pin
topic_to_server   = "drone_web_console_server"# when sending data to the server
server_url        = "192.168.138.1"
server_port       = 1883



# Start SPI connection
spi = spidev.SpiDev() # Created an object
spi.open(0,0) 








# Read MCP3008 data
def analogInput(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data



# method for seismic sensor
def pressure_callback(channel):
  if GPIO.input(channel):
    #make json object to send
    pressure_output = analogInput(channel) # Reading from CH0
    x={
      "type":"pressure_sensor_reading",
      "value":pressure_output
      }
    client.publish(topic_to_server, json.dumps(x))
    print("data published")
  else:
    #make json object to send
    pressure_output = analogInput(channel) # Reading from CH0
    x={
      "type":"pressure_sensor_reading",
      "value":pressure_output
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



#mqtt client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(server_url, server_port, 60)




#pressure sensor gpio setup
'''GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN)
GPIO.add_event_detect(channel,GPIO.BOTH,bouncetime=300)
GPIO.add_event_callback(channel,pressure_callback)'''


print("Setup complete:\n")
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()        


while True:
  temp_output = analogInput(channel) # Reading from CH0
  pressure_output = analogInput(channel) # Reading from CH0
  x={
     "type":"pressure_sensor_reading",
     "value":pressure_output
    }
  client.publish(topic_to_server, json.dumps(x))
  print("data published")
  print(temp_output)
  sleep(5)