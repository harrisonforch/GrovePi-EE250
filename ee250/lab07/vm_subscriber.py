"""EE 250L Lab 07 Skeleton Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time

	
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic ranger topic here
    client.subscribe("anrg-pi13/ultrasonicRanger")
    client.subscribe("anrg-pi13/button")
    client.message_callback_add("anrg-pi13/ultrasonicRanger", ultraSonic_callback)
    client.message_callback_add("anrg-pi13/button", button_callback)



def button_callback(client, userdata, msg):
    print("Button Pressed!")

def ultraSonic_callback(client, userdata, message):
        print("here")
        print("Ultrasonic Read: " + str(message.payload, "utf-8"))


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
        #print("delete this line")
        time.sleep(1)
            

