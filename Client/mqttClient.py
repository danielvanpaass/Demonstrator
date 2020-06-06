import json
import time
import sys
import paho.mqtt.client as mqtt
import ReadUsbPi
import random

try:
    import power_calc
except:
    from Client import power_calc
try:
    import write_hhub
except:
    from Client import write_hhub


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
    if wind:
        print('wind')
        try:
            turbine_type = m['turbine_type']
        except:
            turbine_type = "WES5"
            print('no turbine specified')
        # this would also work, it would return default value wes5
        # turbine_type = m.get('turbine_type', 'WES5')
        calculation = power_calc.power_out_wind(turbine_type)
        hhub_powers.update(json.loads(calculation))
        client.publish("year_data", calculation)
    if solar:
        print('solar')
        try:
            type_pvpanel = m['pv_type']
        except:
            type_pvpanel = "RSM72-6-360M"
            print('no pvpanel specified')
        tilt_panel = m['tilt_panel']  # choice between 30,35 and 40 degrees
        N_solar = m['N_solar']
        calculation = power_calc.power_out_solar(N_solar, tilt_panel, type_pvpanel)
        hhub_powers.update(json.loads(calculation))
        client.publish("year_data", calculation)
    global hour_SoC
    if hydrogen:
        print('hydrogen')
        try:
            H_SoC = m['H_SoC']
            H_SoC_rt = m['H_SoC_rt']
            hour_rt = m['hour']
        except:
            H_SoC = [0] * 8760
            H_SoC_rt = 0
            hour_rt = 0
            print('no H SoC from server')
        hhub_powers.update({'H_SoC': H_SoC, 'H_SoC_rt': H_SoC_rt})
        if (not EV):  # if EV is not present, we can already start putting in the hour for the actuators
            hour_SoC = hour_rt
    if EV:
        print('EV')
        try:
            EV_SoC = m['EV_SoC']
            EV_SoC_rt = m['H_SoC_rt']
            hour_rt = m['hour']
        except:
            EV_SoC = [0] * 8760
            EV_SoC_rt = 0
            hour_rt = 0
            print('no EV SoC from server')
        hhub_powers.update({'EV_SoC': EV_SoC, 'EV_SoC_rt': EV_SoC_rt})
        hour_SoC = hour_rt
    if load:  # it is important that load is sent back last, because the battery calculation will wait for this to start
        try:
            load_type = m['load_type']
        except:
            load_type = "saving"
            print('no load type specified')
        N_load = m['N_load']
        calculation = power_calc.power_out_load(N_load, load_type)
        hhub_powers.update(json.loads(calculation))
        client.publish("year_data", calculation)
    global hour
    if 'hhub_hour' in m:
        hour = m['hhub_hour']


def getMAC(interface='eth0'):
    # Return the MAC address used for client ID
    try:
        strs = open('/sys/class/net/%s/address' % interface).read()
    except:
        strs = 'alias_client_notpis' + str(random.randint(0, 999))
    return strs[0:21]


# broker_address = "raspberrypi"  # "raspberrypi"  # server Pi name
broker_address = "test.mosquitto.org"  # use external broker
# broker_address="mqtt.eclipse.org" #use external broker

# instantiate client with MAC client ID for the session
client = mqtt.Client(getMAC('eth0'))
# client = mqtt.Client('clienysdy')
# set to false to be toggled by on_connect
client.connected_flag = False

# bind call back functions
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address)
# initialize variables
hhub_powers = {}
hour = -1
hour_SoC = -1
# in the loop, call back functions can be activated
client.loop_start()
client.subscribe("to_clients")
while True:
    time.sleep(1)
    if sys.platform == 'linux':
        wind, solar = ReadUsbPi.connected_usb()  # gives wind = 1,0 and solar = 1,0
        load = 1
        hydrogen = 1
        EV = 1
    else:
        wind = 1
        solar = 1
        load = 1
        hydrogen = 1
        EV = 1
    if hour > -1:
        sensor_data_rt, updated_powers_year = write_hhub.sensor_hhub(hour, hhub_powers, wind, solar, load)
        client.publish("realtime_data", sensor_data_rt)
        while hour != hour_SoC:
            time.sleep(0.05)
        write_hhub.actuator_hhub(hour, updated_powers_year, wind, solar, load)
        if hour != -1:
            hour += 1
