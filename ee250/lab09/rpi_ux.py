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
	client.subscribe("anrg-pi0/lcd")
	client.message_callback_add("anrg-pi0/customCallback", custom_callback)

def led_callback(client, userdata, message):
	if str(message.payload, "utf-8")=="toggle":
		if led_status == 0:
			led_status=1
		else:
			led_status=0
	digitalWrite(led,led_status)

def lcd_callback(client, userdata, message):
	message = str(message.payload, "utf-8");



if __name__ == '__main__':
	client = mqtt.Client()
	client.on_message = on_message
	client.on_connect = on_connect
	client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
	client.loop_start()

	while (True):
		try:
			[temp,hum] = dht(dht_sensor_port,1)
			client.publish("anrg-pi13/temperature", temp)
			client.publish("anrg-pi13/humidity", hum)
			time.sleep(1)
		except (IOError, TypeError) as e:
			print("Error")
