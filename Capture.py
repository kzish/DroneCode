import picamera
import paho.mqtt.client as mqtt



#snap a picture from th eweb console and send the image to the server
def snap_pic_from_web_console():
    with picamera.PiCamera() as camera:
        camera.resolution = (1280,720)
        camera.capture("newpic.jpg")
        print("picture taken")
        #now send the picture to the server
        #now delete the image



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Capture is connected result code is: "+str(rc))
    client.subscribe("droneCommands")
    client.publish("droneCommands", "test message")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(str(msg.payload))
    command=str(msg.payload)
    if command=="snap_pic":
       snap_pic_from_web_console()
    

    


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.138.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()            