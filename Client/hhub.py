import enum
import smbus

from Client import __USEPINS__

# Enumeration class for the types of models
class Model(enum.IntEnum):
	SOLARPV = enum.auto()
	WINDTURBINE = enum.auto()
	HOUSEHOLD = enum.auto()

# I2C channel 1 is connected to the GPIO pins
channel = 1

# Initialize I2C (SMBus)
if __USEPINS__ == True:
	bus = smbus.SMBus(channel)

# Base I2C address of the chips used
base_address = 0x38

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
		print("Trying to write via GPIO pins, but __USEPINS__ is set to False")
		print("Writing value ", dac_value, " to address ", hex(address))  
		return None

# Use this function to get a value for the table-top model sensors
def getModel(model, power_min, power_max):
	address = base_address + (model - 1) * 2 + 1
	
	if __USEPINS__ == True:
		adc_value = bus.read_byte(address)
	else:
		adc_value = ADC_MAX
		print("Trying to read via GPIO pins, but __USEPINS__ is set to False")
		print("Storing ", adc_value, " in adc_value as dummy from address ", hex(address))
		
	return (power_max - power_min) / ADC_MAX * adc_value + power_min

# def getConnected():
