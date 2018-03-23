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


def on_message(client, userdata, msg):
    """The paho-mqtt library typically converts message payloads into a *byte* 
    string before a message is sent, even if you send an int or a float. Python
    will not convert the payload into a string for printing, so you will have
    to convert it manually. Yes, a *byte* string is different from a string in
    python! Python's approach to strings is very different from C/C++. You'll 
    have to look this one up on your own to better understand python strings."""
    #print("on_message: " + msg.topic + " " + str(msg.payload))
    #print("on_message: msg.payload is of type " + str(type(msg.payload)))


def led_callback(client, userdata, msg):
    led = 4
    message = str(msg.payload)
    print(message)
    if message == "b'LED_ON'":
        #turn on LED
        digitalWrite(led,1)
    elif message == "b'LED_OFF'":
        #turn off LED
        digitalWrite(led,0)


def lcd_callback(client, userdata, message):
    print ("message to lcd" + str(message.payload, "utf-8"))
    msg = str(message.payload, "utf-8")
    print(msg)
    setText_norefresh(msg)
    #code to be added later

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py

    #setting up where things are and ports
    led = 4
    ultrasonic = 2
    button = 3
    button_val = grovepi.digitalRead(button)

    #sets inputs outputs, lcd color
    grovepi.pinMode(led,"OUTPUT")
    setRGB(0,64,128)
    grovepi.pinMode(button, "INPUT")

    #sets client
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    #publishing
    while True:
        if button_val != grovepi.digitalRead(button):
            client.publish("anrg-pi13/button", "Button Pressed!")

        client.publish("anrg-pi13/ultrasonicRanger", grovepi.ultrasonicRead(ultrasonic))
        time.sleep(1)

