"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import grovepi
import paho.mqtt.client as mqtt
import time
import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `from grovepi import *`
sys.path.append('../../Software/Python/')

from grovepi import *
from grove_rgb_lcd import *
#from pynput import keyboard

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("anrg-pi13/led")
    client.subscribe("anrg-pi13/button")
    client.subscribe("anrg-pi13/lcd")
    client.subscribe("anrg-pi13/ultrasonicRanger")
    client.message_callback_add("anrg-pi13/led", led_callback)
    client.message_callback_add("anrg-pi13/lcd", lcd_callback)


def led_callback(client, userdata, msg):
    led = 4
    if str(msg.payload) == "LED_ON":
        #turn on LED
        digitalWrite(led,1)
        print("TURN ON")
    elif str(msg.payload) == "LED_OFF":
        #turn off LED
        digitalWrite(led,0)
        print("TURN OFF")


def lcd_callback(client, userdata, message):
    print ("message to lcd" + str(message.payload))
    setText_norefresh(str(message.payload))
    #code to be added later

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py

    led = 4
    ultrasonic = 2
    button = 3

    grovepi.pinMode(led,"OUTPUT")
    setRGB(0, 0, 0)
    grovepi.pinMode(button, "INPUT")

    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        try:
            client.publish("anrg-pi13/button", grovepi.digitalRead(button))

        print("delete this line")
        client.publish("anrg-pi13/ultrasonicRanger", grovepi.ultrasonicRead(ultrasonic))
        time.sleep(1)

