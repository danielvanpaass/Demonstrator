import json
import time

import paho.mqtt.client as mqtt


# from solar_power_calc import power_out

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK Returned code=", rc)
    else:
        print("Bad connection Returned code= ", rc)


def on_message(client, userdata, message):
    # global N_solar #check if it really works with global
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    # decoded = json.loads(message.payload.decode("utf-8"))
    # if decoded['N_solar']!=N_solar:
    #    N_solar = decoded['N_solar']
    #    client.publish("demon/data", power_out(N_solar))


# simu_hour = decoded['simu_hour']
# pass simu_hour to HHUB
def getMAC(interface='eth0'):
    # Return the MAC address used for client ID
    try:
        str = open('/sys/class/net/%s/address' % interface).read()
    except:
        str = 'alias_for_getMACerrorrr'
    return str[0:17]


broker_address = "raspberrypi"  # server Pi name, also the IP could be used
# broker_address="test.mosquitto.org" #use external broker

# instantiate client with MAC client ID for the session
client = mqtt.Client(getMAC('eth0'))
print(getMAC('eth0'))
# set to false to be toggled by on_connect
client.connected_flag = False
# bind call back functions
client.on_connect = on_connect
client.on_message = on_message
# data_out = power_out(N_solar)
client.connect(broker_address)
# in the loop, call back functions can be activated
client.loop_start()
# initial publish of power values
client.subscribe("demon/data")
data = {'sth': [4, 2, 9.5, 0.4]}
data_out = json.dumps(data)
client.publish("demon/data", data_out)
while True:
    time.sleep(1)

# client.publish("demon/data",power_out(600))
# client.publish("demon/data","OFF")#publish
