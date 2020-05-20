import paho.mqtt.client as mqtt
import time
import json
import power_calc


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK Returned code=", rc)
    else:
        print("Bad connection Returned code= ", rc)


def on_message(client, userdata, message):
    m = json.loads(message.payload.decode("utf-8"))
    print("message received ", str(m))
    print("message topic=", message.topic)
    tilt_panel = m['tilt_panel']  # choice between 30,35 and 40 degrees
    N_solar = m['N_solar']
    N_load = m['N_load']
    load_type = m['load_type']
    client.publish("to_dash", power_calc.power_out_solar(N_solar, tilt_panel, N_load, load_type))
    # simu_hour = decoded['simu_hour']
    # pass simu_hour to HHUB


def getMAC(interface='eth0'):
    # Return the MAC address used for client ID
    try:
        str = open('/sys/class/net/%s/address' % interface).read()
    except:
        str = 'alias_client_notpis'
    return str[0:17]


#broker_address = "raspberrypi"  # "raspberrypi"  # server Pi name
#broker_address="test.mosquitto.org" #use external broker
broker_address="mqtt.eclipse.org" #use external broker

# instantiate client with MAC client ID for the session
client = mqtt.Client(getMAC('eth0'))
# set to false to be toggled by on_connect
client.connected_flag = False
# bind call back functions
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address)
# in the loop, call back functions can be activated
client.loop_start()
client.subscribe("to_clients")
while True:
    time.sleep(1)

# client.publish("demon/data",power_out_solar(600))
# client.publish("demon/data","OFF")#publish
