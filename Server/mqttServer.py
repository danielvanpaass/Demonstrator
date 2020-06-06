import json
import paho.mqtt.client as mqtt
import random

try:
    from Server import maindash
except:
    import maindash

try:
    from Server import battery
except:
    import battery


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK Returned code=", rc)
    else:
        print("Bad connection Returned code= ", rc)


def on_message(client, userdata, message):
    received_data = json.loads(message.payload.decode("utf-8"))
    print(received_data)
    topic = message.topic
    if topic == "year_data":
        year_data.update(received_data)
    if topic == "realtime_data":
        realtime_data.update(received_data)
        if 'power_load_rt' in received_data:
            hour_simul = received_data['hour_simul']
            batteries_rt = battery.power_battery_realtime(received_data, hour_simul)
            year_data.update(batteries_rt)
            SoC_rt = {'EV_SoC_rt': batteries_rt['EV_SoC_rt'], 'H_SoC_rt': batteries_rt['H_SoC_rt']}
            client.publish("to_clients", json.dumps(SoC_rt))
    maindash.dash_update_solar(year_data)
    # m = message.payload.decode("utf-8")
    # with open('data.json', 'w', encoding='utf-8') as f:
    #     json.dump(m, f, ensure_ascii=False, indent=4)


def getMAC(interface='eth0'):
    # Return the MAC address used for client ID
    try:
        strs = open('/sys/class/net/%s/address' % interface).read()
    except:
        strs = 'alias_server_notpi' + str(random.randint(0, 999))
    return strs[0:21]


class N_EV():
    def __init__(self, value):
        self.value = value

    def setValue(self, value):
        self.value = value
        batteries = battery.power_battery(year_data, self.value)
        year_data.update(batteries)
        maindash.dash_update_solar(year_data)

    def getValue(self):
        return self.value


number_EV = N_EV(30)
year_data = {}
realtime_data = {}

# broker_address = "raspberrypi"  # server Pi name (you can also use IP address here)
broker_address = "test.mosquitto.org"  # use external broker
# broker_address = "mqtt.eclipse.org"  # use external broker

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
# client.subscribe("to_clients")
client.subscribe("year_data")
client.subscribe('realtime_data')
# initial publish of power values
while True:
    maindash.connect_and_run_dash(client, number_EV)
# client.publish("demon/data",power_out(600))
# client.publish("demon/data","OFF")#publish
