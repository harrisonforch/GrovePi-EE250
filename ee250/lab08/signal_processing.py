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
moving_avg_ranger1 = []
moving_avg_ranger2 = []

ranger1_avg = []
ranger2_avg = []

count_1 = 0
count_2 = 0

ranger1_state = 0
ranger2_state = 0

def ranger1_callback(client, userdata, msg):
    global ranger1_dist
<<<<<<< HEAD
    global ranger1_avg
    count_1 = count_1 + 1
=======
    global moving_avg_ranger1
>>>>>>> sp18-master
    ranger1_dist.append(int(msg.payload))

    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]
<<<<<<< HEAD
    avg = 0

    for i in ranger1_dist:
    	avg += i
    avg /= MAX_LIST_LENGTH
    ranger1_avg.append(avg)
    ranger1_avg = ranger1_avg[-MAX_LIST_LENGTH:]

def ranger2_callback(client, userdata, msg):
    global ranger2_dist
    global ranger2_avg
    count_2 = count_2 + 1
    ranger2_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]
    avg = 0

    for i in ranger2_dist:
    	avg += i
    avg /= MAX_LIST_LENGTH
    ranger2_avg.append(avg)
    ranger2_avg = ranger2_avg[-MAX_LIST_LENGTH:]
=======
    moving_avg_ranger1 = moving_avg_ranger1[-MAX_LIST_LENGTH]

     x = 0
    for i in ranger1_dist:
    	x += i
    x /= MAX_LIST_LENGTH
    moving_avg_ranger1.append(x)

def ranger2_callback(client, userdata, msg):
    global ranger2_dist
    global moving_avg_ranger2
    ranger2_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]
    moving_avg_ranger2 = moving_avg_ranger2[-MAX_LIST_LENGTH]

    x = 0
    for i in ranger2_dist:
    	x += i
    x /= MAX_LIST_LENGTH
    moving_avg_ranger2.append(x)
>>>>>>> sp18-master

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

def classify_mvmnt_ranger():
	firstVal1 = moving_avg_ranger1[MAX_LIST_LENGTH]
	#checks ranger 1
	for i in reversed(moving_avg_ranger1[:25]):
		#case 1: person standing still on the left
		if (-2 <= firstVal1 - i <= 2):
			#checking if person is standing still on the right
			firstVal2 = moving_avg_ranger2[MAX_LIST_LENGTH]
			pos = 0
			neg = 0
			for j in reversed(moving_avg_ranger2[:25]):

				#checking if person is standing still on the right
				if (-2 <= firstVal2 - j <= 2):
					#where are you standing still
					distance = ranger1_dist[MAX_LIST_LENGTH] - ranger2_dist[MAX_LIST_LENGTH]
					if distance >= 80:
						return "standing still, right"
					elif distance <= -80:
						return "standing still, left"
					else:
						return "standing still, middle"
				#finding the direction of moving
				if (firstval2 - j >= 5):
					pos++
				else:
					neg++

				if pos > neg:
					return "moving "


if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_hostname, broker_port, 60)
    client.loop_start()

    ranger1_avg = [0] * 100
    ranger2_avg = [0] * 100

    while True:
        """ You have two lists, ranger1_dist and ranger2_dist, which hold a window
        of the past MAX_LIST_LENGTH samples published by ultrasonic ranger 1
        and 2, respectively. The signals are published roughly at intervals of
        200ms, or 5 samples/second (5 Hz). The values published are the 
        distances in centimeters to the closest object. Expect values between 
        0 and 512. However, these rangers do not detect people well beyond 
        ~125cm. """
        
        # TODO: detect movement and/or position
<<<<<<< HEAD


        #proccessing data 1
        current_count = count_1 + 1
        current_numb = ranger1_avg[MAX_LIST_LENGTH - 10]
        slope_1 = 0
        count_1 = 0
        for i in range (1, current_count):
        	slope_1 += ranger1_avg[MAX_LIST_LENGTH - i]
        slope_1 /= current_count

        #analyzing data
        if(current_count != 1):
            if (-2 <= ((((slope_1)  * current_count) - current_numb) / (current_count - 1)) - current_numb  <= 2) :
                ranger1_state = 0
            elif slope_1 < current_numb:
                ranger1_state = 1
            else:
                ranger1_state = -1

        #proccessing data 2
        current_count = count_2 + 1
        current_numb = ranger2_avg[MAX_LIST_LENGTH - current_count]
        slope_2 = 0
        count_2 = 0
        for i in range (1, current_count):
        	slope_2 += ranger2_avg[MAX_LIST_LENGTH - i]
        slope_2 /= current_count


        #analyzing data
        if(current_count != 1):
            if (2 <= ((((slope_2)  * current_count) - current_numb) / (current_count - 1)) - current_numb  <= 2) :
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
        
=======
>>>>>>> sp18-master
        print("ranger1: " + str(ranger1_dist[-1:]) + ", ranger2: " + 
            str(ranger2_dist[-1:])) 
        
        time.sleep(0.2)