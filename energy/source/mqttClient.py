import paho.mqtt.client as mqtt
import time
import json
from solar_power_calc import power_out_solar

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code= ",rc)

def on_message(client, userdata, message):
    global N_solar #check if it really works with global
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    decoded = json.loads(message.payload.decode("utf-8"))
    if decoded['N_solar']!=N_solar:
        N_solar = decoded['N_solar']
        client.publish("demon/data", power_out_solar(N_solar))
    simu_hour = decoded['simu_hour']
    #pass simu_hour to HHUB
def getMAC(interface='eth0'):
  # Return the MAC address used for client ID
  try:
    str = open('/sys/class/net/%s/address' %interface).read()
  except:
    str = 'alias_client_notpi'
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
#before connecting, calculate power flows with initial solar panel values
N_solar = 20
data_out = power_out_solar(N_solar)
client.connect(broker_address)
#in the loop, call back functions can be activated
client.loop_start()
client.subscribe("demon/data")
#initial publish of power values
client.publish("demon/data",data_out)
while True:
    time.sleep(1)

# client.publish("demon/data",power_out_solar(600))
# client.publish("demon/data","OFF")#publish