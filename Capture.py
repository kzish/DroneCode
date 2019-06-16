import picamera
import time
from os import system
from time import sleep
import paho.mqtt.client as mqtt
import uuid


class DroneCamera():
    def capture(self,image_count,time_lenght, cam_res=(1280, 720) ):
        for i in range(image_count):
            with picamera.PiCamera() as camera:
                camera.resolution = cam_res
                time.sleep(1) # Camera warm-up time
                filename = 'image%02d.jpg' % i
                camera.capture(filename)
                print('Captured %s' % filename)
            # Capture one image a minute
            time.sleep(time_lenght)

    def snap_pic_from_web_console(self,cam_res=(1280, 720) ):
            with picamera.PiCamera() as camera:
                camera.resolution = cam_res
                time.sleep(1) # Camera warm-up time
                filename = uuid.uuid4()+".jpg"
                camera.capture(filename)
                print('Captured %s' % filename)
                return filename
            
    def gif(self,image_count,time_lenght,cam_res=(1280, 720)):
        self.capture(image_count,time_lenght, cam_res )
        #For making a GIF from the captured images. Needs inatallation of 
        system('convert -delay 10 -loop 0 image*.jpg animation.gif')

    def video_recstream(self):
        with picamera.PiCamera() as camera:
            with picamera.PiCameraCircularIO(camera) as stream:
                camera.start_preview()
                camera.start_recording(stream, format='h264')
                camera.wait_recording(10)
                camera.stop_recording()

    def video_record(self,video_time=60, cam_res=(1280, 720)):
        with picamera.PiCamera() as camera:
            camera.resolution = cam_res 
            camera.start_recording('my_video.h264')
            camera.wait_recording(video_time)
            camera.stop_recording()            





# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("droneCommands")
    client.publish(topic_to_server, "test data exce")

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