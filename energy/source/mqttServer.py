import paho.mqtt.client as mqtt
import time
from solar_power_calc import power_out_solar

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code= ",rc)

def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)

def getMAC(interface='eth0'):
  # Return the MAC address used for client ID
  try:
    str = open('/sys/class/net/%s/address' %interface).read()
  except:
    str = 'alias_for_getMACerror'
  return str[0:17]

broker_address = "192.168.2.199" #server Pi address
# broker_address="test.mosquitto.org" #use external broker

#instantiate client with MAC client ID for the session
client = mqtt.Client(getMAC('eth0'))
# set to false to be toggled by on_connect
client.connected_flag=False
#bind call back functions
client.on_connect=on_connect
client.on_message=on_message

client.connect(broker_address)
#in the loop, call back functions can be activated
client.subscribe("demon/data")
client.loop_start()

while not client.connected_flag: #wait in loop
     time.sleep(1)



# client.publish("demon/data",power_out_solar(600))
client.publish("demon/data","OFF")#publish
time.sleep(3)
client.loop_stop()    #Stop loop
client.disconnect()