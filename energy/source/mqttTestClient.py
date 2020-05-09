
#needs to be installed on client pi by pip(3)
import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK Returned code=",rc)
        #client.subscribe(topic)
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
    str = "00:00:00:00:00:00"
  return str[0:17]

broker_address = "192.168.2.199" #server Pi address
#broker_address="iot.eclipse.org" #use external broker

#instantiate client with MAC client ID for the session
client = mqtt.Client(getMAC('eth0'))
client.connected_flag=False# set to false to be toggled by on_connect
client.on_connect=on_connect  #bind call back function
client.on_message=on_message        #attach function to callback
client.connect(broker_address)
client.loop_start()

#could be implemted to wait until connection
while not client.connected_flag: #wait in loop
     time.sleep(1)

client.subscribe("demon/data")
client.publish("demon/data","OFF")

client.publish("house/main-light","OFF")#publish
time.sleep(4)
client.loop_stop()    #Stop loop
client.disconnect()