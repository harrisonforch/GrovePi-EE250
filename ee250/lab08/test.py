#use 'a' and 's' keys to move target left and right between sensors

import paho.mqtt.client as mqtt
import time
from pynput import keyboard
from random import*

x=100
max_distance=300
person_width=30
noise_factor=2
sensor_1 = 0
sensor_2 = 0

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload)) 

def on_press(key):
    
    global x

    try: 
        k = key.char 
    except: 
        k = key.name 
       
    if k == 'a':
        
        if(sensor_1>5):
            x=x-1

    elif k == 's':
        
        if(sensor_1<max_distance-5):
            x=x+1
    
        
        
if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()


    while True:
          
        sensor_1 = x-(person_width/2)+randint(-noise_factor,noise_factor)
        sensor_2 = max_distance-((x-person_width/2))++randint(-noise_factor,noise_factor)

<<<<<<< HEAD
        client.publish("az/ultrasonic_ranger1", sensor_1)
        client.publish("az/ultrasonic_ranger2", sensor_2)
        print("Sensor 1:", sensor_1, " ........ Sensor 2:", sensor_2 )
        time.sleep(.2)
=======
<<<<<<< HEAD
        client.publish("test/ultrasonic_ranger1", sensor_1)
        client.publish("test/ultrasonic_ranger2", sensor_2)
        print("Sensor 1:", sensor_1, " ........ Sensor 2:", sensor_2 )
        time.sleep(.2)
            
=======
        client.publish("az/ultrasonic_ranger1", sensor_1)
        client.publish("az/ultrasonic_ranger2", sensor_2)
        print("Sensor 1:", sensor_1, " ........ Sensor 2:", sensor_2 )
        time.sleep(.2)
>>>>>>> 3862d01635ebaf6c24294fbb265bb61dca71889e
>>>>>>> 6df2931d341a3647d66853f9d31bb783f6f410e3
