import paho.mqtt.client as mqtt
import time
import requests
import json
from datetime import datetime
import time


# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000
ultrasonic_ranger1_topic = "ultrasonic_ranger1"
ultrasonic_ranger2_topic = "ultrasonic_ranger2"

# Lists holding the ultrasonic ranger sensor distance readings. Change the 
# value of MAX_LIST_LENGTH depending on how many distance samples you would 
# like to keep at any point in time.
MAX_LIST_LENGTH = 5
ranger1_dist = []
ranger2_dist = []


#moving average buffers
ranger1_avg = []
ranger2_avg = []

#ranger states
ranger1_state = 0
ranger2_state = 0

def ranger1_callback(client, userdata, msg):
    global ranger1_dist
    global ranger1_avg

    number = int(msg.payload)
    if(number > 125):
    	number = 125

    ranger1_dist.append(number)
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]

    #populates moving average for ranger 1
    avg = 0
    for i in ranger1_dist:
        avg += i
    avg /= MAX_LIST_LENGTH
    ranger1_avg.append(avg)
    ranger1_avg = ranger1_avg[-MAX_LIST_LENGTH:]

def ranger2_callback(client, userdata, msg):
    global ranger2_dist
    global ranger2_avg


    number = int(msg.payload)
    if(number > 125):
    	number = 125

    ranger2_dist.append(number)
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]

    #populates moving average for ranger 2
    avg = 0
    for i in ranger2_dist:
        avg += i
    avg /= MAX_LIST_LENGTH
    ranger2_avg.append(avg)
    ranger2_avg = ranger2_avg[-MAX_LIST_LENGTH:]



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(ultrasonic_ranger1_topic)
    client.message_callback_add(ultrasonic_ranger1_topic, ranger1_callback)
    client.subscribe(ultrasonic_ranger2_topic)
    client.message_callback_add(ultrasonic_ranger2_topic, ranger2_callback)

# The callback for when a PUBLISH message is received from the server.
# This should not be called.
def on_message(client, userdata, msg): 
    print(msg.topic + " " + str(msg.payload))


if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_hostname, broker_port, 60)
    client.loop_start()

    #initially populates the average
    ranger1_avg = [0] * MAX_LIST_LENGTH
    ranger2_avg = [0] * MAX_LIST_LENGTH
    message = "none"

    hdr = {
        'Content-Type': 'application/json',
        'Authorization': None #not using HTTP secure
    }

    # The payload of our message starts as a simple dictionary. Before sending
    # the HTTP message, we will format this into a json object
    

    while True:
        """ You have two lists, ranger1_dist and ranger2_dist, which hold a window
        of the past MAX_LIST_LENGTH samples published by ultrasonic ranger 1
        and 2, respectively. The signals are published roughly at intervals of
        200ms, or 5 samples/second (5 Hz). The values published are the 
        distances in centimeters to the closest object. Expect values between 
        0 and 512. However, these rangers do not detect people well beyond 
        ~125cm. """
        
        # TODO: detect movement and/or position

        
        #proccessing data 1
        current_numb = ranger1_avg[MAX_LIST_LENGTH - 1]
        slope_1 = 0
        for i in ranger1_avg:
            slope_1 += i
        slope_1 /= MAX_LIST_LENGTH

        #analyzing data
     
        if (-10 <= slope_1 - current_numb <= 10) :
            ranger1_state = 0
        elif slope_1 < current_numb:
            ranger1_state = 1
        else:
            ranger1_state = -1

        #proccessing data 2
        
        slope_2 = 0
        current_numb = ranger2_avg[MAX_LIST_LENGTH - 1]
        for i in ranger2_avg:
            slope_2 += i
        slope_2 /= MAX_LIST_LENGTH


        #analyzing data
        if (-10 <= slope_2 - current_numb  <= 10) :
           ranger2_state = 0
        elif slope_2 < current_numb:
           ranger2_state = 1
        else:
           ranger2_state = -1


        #final data analysis

        #walking close toward ranger1
        if(ranger1_state == 1 or ranger2_state == -1):
            print("Walking Left")
            message = "Walking Left"
        #walking toward ranger 2
        elif(ranger2_state == 1 or ranger1_state == -1):
            print("Walking Right")
            message = "Walking Right"
        #standing still
        elif(ranger1_state == 0 and ranger2_state == 0):
            #standing middle
            if(-20 <= slope_1 - slope_2 <= 20):
                print("Standing Still, Middle")
                message = "Standing Still, Middle"
            #standing on right
            elif(slope_1 > slope_2):
                print("Standing Still, Left")
                message = "Standing Still, Left"
            #standing on left
            elif(slope_2 > slope_1):
                print("Standing Still, Right")
                message = "Standing Still, Right"

        payload = {
            'time': str(datetime.now()),
            'event': message
            }
        
        #publishing the data
        response = requests.post("http://0.0.0.0:5000/post-event", headers = hdr,
                                 data = json.dumps(payload)) 
        
        time.sleep(0.2)