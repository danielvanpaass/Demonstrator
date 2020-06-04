import json
import paho.mqtt.client as mqtt

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
    m = message.payload.decode("utf-8")
    received_data = json.loads(m)
    data_in.update(received_data)
    print(received_data)
    if 'power_load' in received_data:
        print('hi')
        print(*data_in)
        batteries = battery.power_battery(data_in, N_EV=30)
        print(*batteries)
        data_in.update(batteries)
    if 'hour_simul' in received_data:
        hour_simul = received_data['hour_simul']
        actuator_data = received_data['actuator_data'] #extracts a dictionary from dictionary
        year_data = data_in
        batteries_rt = battery.power_battery_realtime(actuator_data, year_data, hour_simul)
        data_in.update(batteries_rt)
        client.publish("to_clients", json.dumps(batteries_rt))
    maindash.dash_update_solar(data_in)
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


data_in = {}

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
client.subscribe("to_dash")
# initial publish of power values
while True:
    maindash.connect_and_run_dash(client)
# client.publish("demon/data",power_out(600))
# client.publish("demon/data","OFF")#publish
