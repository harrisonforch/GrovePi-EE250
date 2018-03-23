"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""
import sys
from grovepi import *
import grovepi
import paho.mqtt.client as mqtt
import time
#from pynput import keyboard

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("anrg-pi13/led")
<<<<<<< HEAD
    client.subscribe("anrg-pi13/lcd")
    client.subscribe("anrg-pi13/ultrasonicRanger")
    client.message_callback_add("anrg-pi13/led", led_callback)
    client.message_callback_add("anrg-pi13/ultraSonicRanger", ultraSonic_callback)
    client.message_callback_add("anrg-pi13/lcd", lcd_callback)

=======
    client.subscribe("anrg-pi13/ultrasonicRanger")
    client.subscribe("anrg-pi13/lcd")
    client.message_callback_add("anrg-pi13/led", led_callback)
    client.message_callback_add("anrg-pi13/lcd", lcd_callback)
>>>>>>> 156b6c9f541437eb6e5dd05e9347e889a1489836

def led_callback(client, userdata, message):
    led = 4
    pinMode(led,"OUTPUT")
    msg = str(message.payload)
    if msg == "LED_ON":
        #turn on LED
        digitalWrite(led,1)
        print("TURN ON")
    elif msg == "LED_OFF":
        #turn off LED
        digitalWrite(led,0)
        print("TURN OFF")


def lcd_callback(client, userdata, message):
    print ("essage to lcd")
    #code to be added later


#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    while True:
        print("delete this line")
        client.publish("anrg-pi13/ultrasonicRanger", grovepi.ultrasonicRead(2))
        time.sleep(1)

