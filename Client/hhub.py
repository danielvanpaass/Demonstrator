import enum
from time import sleep

from Client import __USEPINS__

if __USEPINS__ == True:
	import smbus
	import RPi.GPIO as GPIO

# Enumeration class for the types of models
class Model(enum.IntEnum):
	SOLARPV = enum.auto()
	WINDTURBINE = enum.auto()
	HOUSEHOLD = enum.auto()

# I2C channel 1 is connected to the GPIO pins
channel = 1

if __USEPINS__ == True:
	# Initialize I2C (SMBus)
	bus = smbus.SMBus(channel)
	
	# Choose BCM or BOARD for demux
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(DEMUX_PIN_1, GPIO.OUT)
	GPIO.setup(DEMUX_PIN_2, GPIO.OUT)

# Demux GPIO pins
DEMUX_PIN_1 = 17 # In wiringpi 0. Is BCM 17, and physical 11
DEMUX_PIN_2 = 13 # In wiringpi 2. Is BCM 13, and physical 27

# Base I2C address of the chips used
base_address = 0x20

# Bits used for the DAC and ADC
BITS_DAC = 8
DAC_MAX = 255
BITS_ADC = 8
ADC_MAX = 255

# Use this function to set a value for the table-top models
def setModel(power, model, power_min, power_max):
	# Exceptions for user input
	if (power < power_min):
		raise Exception('power should not be smaller than power_min.')
	elif (power > power_max):
		raise Exception('power should not be smaller than power_max.')

	dac_value = round((power - power_min) * DAC_MAX / (power_max - power_min))
	address = base_address + (model - 1) * 2
	
	if __USEPINS__ == True:
		return bus.write_byte(address, dac_value)
	else:
		print("Trying to write via I2C pins, but __USEPINS__ is set to False")
		print("Writing value ", dac_value, " to address ", hex(address))  
		return None

# Use this function to get a value for the table-top model sensors
def getModel(model, power_min, power_max):
	address = base_address + (model - 1) * 2 + 1
	
	if __USEPINS__ == True:
		adc_value = bus.read_byte(address)
	else:
		adc_value = ADC_MAX
		print("Trying to read via I2C pins, but __USEPINS__ is set to False")
		print("Storing ", adc_value, " in adc_value as dummy from address ", hex(address))
		
	return (power_max - power_min) / ADC_MAX * adc_value + power_min


def _read_i2c(pin1,pin2):
	id_address_table = []
	for sub_address in range(0,8,2):
		address = base_address + sub_address
		try:
			byte = uint8(bus.read_byte(base_address + sub_address))
			byte = 0x6E
			id = (byte & 0x0F)
			id_address_table.append([id,address,pin1,pin2])
		except: # exception if read_byte fails
			pass
	return id_address_table

def getConnected(demux_settle_time):
	id_address_table = []
	if __USEPINS__ == True:
		for pin1 in [0,1]:
			for pin2 in [0,1]:
				GPIO.output(DEMUX_PIN_1,pin1)
				GPIO.output(DEMUX_PIN_2,pin2)
				sleep(demux_settle_time)
				id_address_table.extend(_read_i2c(pin1,pin2))
	else:
		print("Trying to detect I2C devices, but __USEPINS__ is set to False")
	return id_address_table
