import json
import paho.mqtt.client as mqtt
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
    topic = message.topic
    if topic == "year_data":
        year_data.update(received_data)
        if 'power_load' in received_data:
            N_EV = number_EV.getValue()
            batteries = battery.power_battery(year_data, N_EV)
            year_data.update(batteries)
            SoC = {'EV_SoC': batteries['EV_SoC_rt'], 'H_SoC': batteries['H_SoC_rt']}
            client.publish("to_clients", json.dumps(SoC))
    if topic == "realtime_data":
        realtime_data.update(received_data)
        if 'power_load' in received_data:
            hour_simul = received_data['hour_simul']
            batteries_rt = battery.power_battery_realtime(received_data, hour_simul)
            SoC_rt = {'EV_SoC': batteries_rt['EV_SoC'], 'H_SoC': batteries_rt['H_SoC']}
            client.publish("to_clients", json.dumps(SoC_rt))
            for key in list(received_data.keys()):
                if key != 'hour_simul':
                    year_data[key][hour_simul]=received_data[key]


    maindash.dash_update_solar(year_data)
    # m = message.payload.decode("utf-8")
    # with open('data.json', 'w', encoding='utf-8') as f:
    #     json.dump(m, f, ensure_ascii=False, indent=4)


def getMAC(interface='eth0'):
    # Return the MAC address used for client ID
    try:
        str = open('/sys/class/net/%s/address' % interface).read()
    except:
        str = 'alias_server_notpi'
    return str[0:17]

class N_EV():
    def __init__(self, value):
        self.value = value
    def setValue(self, value):
        self.value = value
    def getValue(self):
        return self.value
number_EV = N_EV(30)
year_data = {}
realtime_data = {}

# broker_address = "raspberrypi"  # server Pi name (you can also use IP address here)
# broker_address = "test.mosquitto.org"  # use external broker
broker_address = "mqtt.eclipse.org"  # use external broker

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
