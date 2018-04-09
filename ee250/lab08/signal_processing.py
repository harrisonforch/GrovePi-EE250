import paho.mqtt.client as mqtt
import time

# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000
ultrasonic_ranger1_topic = "ultrasonic_ranger1"
ultrasonic_ranger2_topic = "ultrasonic_ranger2"

# Lists holding the ultrasonic ranger sensor distance readings. Change the 
# value of MAX_LIST_LENGTH depending on how many distance samples you would 
# like to keep at any point in time.
MAX_LIST_LENGTH = 100
ranger1_dist = []
ranger2_dist = []


ranger1_avg = []
ranger2_avg = []

count_1 = 0
count_2 = 0

ranger1_state = 0
ranger2_state = 0

def ranger1_callback(client, userdata, msg):
    global ranger1_dist
    global ranger1_avg
    global count_1
    count_1 = count_1 + 1
    cuttoff_1 = int(msg.payload)

    if cuttoff_1 >= 200:
        cuttoff_1 = 200


    ranger1_dist.append(cuttoff_1)
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]


def ranger2_callback(client, userdata, msg):
    global ranger2_dist
    global ranger2_avg
    global count_2
    count_2 = count_2 + 1
    cuttoff_2 = int(msg.payload)

    if cuttoff_2 >= 200:
        cuttoff_2 = 200


    ranger2_dist.append(cuttoff_2)
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]
    




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

    ranger1_dist = [0] * 100
    ranger2_dist = [0] * 100

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
        current_count = count_1 + 1
        current_numb = ranger1_dist[MAX_LIST_LENGTH - current_count]
        slope_1 = 0
        for i in range (1, current_count + 1):
            slope_1 += ranger1_dist[MAX_LIST_LENGTH - i]
        slope_1 /= current_count
        count_1 = 0

        #analyzing data
        if(current_count != 1):
            if (-2 <= ((((slope_1)  * current_count) - current_numb) / (current_count - 1)) - current_numb  <= 2) :
                ranger1_state = 0
            elif slope_1 < current_numb:
                ranger1_state = 1
            else:
                ranger1_state = -1
        else:
            if (-2 <= slope_1 - current_numb <=2):
                ranger1_state = 0
            elif slope_1 < current_numb:
                ranger1_state = 1
            else:
                ranger1_state = -1

        #proccessing data 2
        current_count = count_2 + 1
        current_numb = ranger2_dist[MAX_LIST_LENGTH - current_count]
        slope_2 = 0
        for i in range (1, current_count + 1):
            slope_2 += ranger2_dist[MAX_LIST_LENGTH - i]
        slope_2 /= current_count
        count_2 = 0

        #analyzing data
        if(current_count != 1):
            if (2 <= ((((slope_2)  * current_count) - current_numb) / (current_count - 1)) - current_numb  <= 2) :
                ranger2_state = 0
            elif slope_2 < current_numb:
                ranger2_state = 1
            else:
                ranger2_state = -1
        else:
            if (-2 <= slope_2-current_numb <=2):
                ranger2_state = 0
            elif slope_2 < current_numb:
                ranger2_state = 1
            else:
                ranger2_state = -1


        #final data analysis

        #walking close toward ranger1
        if(ranger1_state == 1):
            print("Walking Left")
        #walking toward ranger 2
        elif(ranger2_state == 1):
            print("Walking Right")
        #standing still
        elif(ranger1_state == 0 and ranger2_state == 0):
            #standing middle
            if(-10 <= slope_1 - slope_2 <=10):
                print("Standing Still, Middle")
            #standing on right
            elif(slope_1 > slope_2):
                print("Standing Still, Right")
            #standing on left
            elif(slope_2 > slope_1):
                print("Standing Still, Left")
        
        print("ranger1: " + str(ranger1_dist[-1:]) + ", ranger2: " + 
            str(ranger2_dist[-1:])) 
        
        time.sleep(0.2)