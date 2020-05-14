import enum
import smbus

# Enumeration class for the types of models
class Model(enum.Enum):
	SOLARPV = enum.auto()
	WINDTURBINE = enum.auto()
	HOUSEHOLD = enum.auto()

# I2C channel 1 is connected to the GPIO pins
channel = 1

# Initialize I2C (SMBus)
bus = smbus.SMBus(channel)

# Base I2C address of the chips used
base_address = 0x38

# Bits used for the DAC and ADC
BITS_DAC = 8
DAC_MAX = 255
BITS_ADC = 8
ADC_MAX = 255

def setModel(power, model, power_min, power_max):
	# Exceptions for user input
	if (power < power_min):
		raise Exception('power should not be smaller than power_min.')
	elif (power > power_max):
		raise Exception('power should not be smaller than power_max.')

	dac_value = (power - power_min) * DAC_MAX / (power_max - power_min)
	address = base_address + model * 2
	return smbus.write_byte(address, dac_value)

def getModel(model, power_min, power_max):
	# Exceptions for user input
	if (power < power_min):
		raise Exception('power should not be smaller than power_min.')
	elif (power > power_max):
		raise Exception('power should not be smaller than power_max.')
	
	address = base_address + model * 2 + 1
	adc_value = smbus.read_byte(address)
	return (power_max - power_min) / ADC_MAX * adc_value + power_min

# def getConnected():
