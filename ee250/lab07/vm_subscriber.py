"""EE 250L Lab 07 Skeleton Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time

	
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("anrg-pi13/ultrasonicRanger")
    #subscribe to the ultrasonic ranger topic here
    client.message_callback_add("anrg-pi13/ultraSonicRanger", ultraSonic_callback)



def ultraSonic_callback(client, userdata, message):
        print("Ultrasonic Read: " + str(message.payload))

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
        time.sleep(1)
            

