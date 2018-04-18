import paho.mqtt.client as mqtt
import time
import sys
sys.path.append('../../Software/Python/')

from grovepi import *
from grove_rgb_lcd import *

led = 4
led_status= 0
dht_sensor_port=7

pinMode(led,"OUTPUT")
digitalWrite(led,led_status)

def on_connect(client, userdata, flags, rc):
	print("Connected to server (i.e., broker) with result code "+str(rc))



	client.subscribe("anrg-pi13/led")
	client.message_callback_add("anrg-pi13/led", led_callback)
	client.subscribe("anrg-pi13/lcd")
	client.message_callback_add("anrg-pi13/lcd", lcd_callback)

def led_callback(client, userdata, message):
	print(str(message.payload,"utf-8"))
	print("test")
	if str(message.payload, "utf-8")=="toggle":
		if led_status == 0:
			led_status=1
			print("led on")
		else:
			led_status=0
			print("led off")
	digitalWrite(led,led_status)

def lcd_callback(client, userdata, message):
	print("message recieved")
	message = str(message.payload, "utf-8");
	setText(message)
def on_message(client, userdata, msg):
	print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))



if __name__ == '__main__':
	client = mqtt.Client()
	client.on_message = on_message
	client.on_connect = on_connect
	client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
	client.loop_start()


	setRGB(0,255,0)

	while (True):
		try:
			[temp,hum] = dht(dht_sensor_port,1)
			t=str(temp)
			h=str(hum)
			print("temp: "+str(temp)+" hum: "+str(hum))
			client.publish("anrg-pi13/temperature", t)
			client.publish("anrg-pi13/humidity", h)
			time.sleep(1)
		except (IOError, TypeError) as e:
			print("Error")
