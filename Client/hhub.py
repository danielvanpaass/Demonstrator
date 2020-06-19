from Client import __USEPINS__

import math

if __USEPINS__ == True:
	from smbus2 import SMBus
	import RPi.GPIO as GPIO
	
class SolarPV():
	def actuate(self, power):
		if power >= 1.0:
			print('SolarPV: power should not be >= 1.0, writing byte as 0xff')
			send_byte = 0xff
		elif power < 0.0:
			print('SolarPV: power should not be < 0.0, writing byte as 0x00')
			send_byte = 0x00
		else:
			send_byte = math.floor(power * 256)
		send_byte &= 0xff
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					bus.write_word_data(self._address + 1, self._actuate_command, send_byte)
			except:
				print('SolarPV: Could not write to I2C address {} with byte {} and command {}'.format(hex(self._address + 1), hex(send_byte), self._command))
		else:
			print('SolarPV: Actuating power as byte {} to I2C address {}'.format(hex(send_byte), hex(self._address + 1)))
		
	def sense(self):
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					retrieve_byte = bus.read_word_data(self._address + 1, self._sense_command)
			except:
				print('SolarPV: Could not read from I2C address {} with command {}'.format(hex(self._address + 1), self._sense_command))
		else:
			retrieve_byte = 10
			print('SolarPV: Sensing power as byte {} from I2C address {}'.format(hex(retrieve_byte), hex(self._address + 1)))
		return retrieve_byte * 0.00390625

	def configure(self):
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					bus.write_word_data(self._address, 6, 0xff)
					bus.write_word_data(self._address + 1, 6, [0xff, 0x00])
			except:
				print('SolarPV: Could not set configuration registers at I2C address {} or {}'.format(hex(self._address),hex(self._address + 1)))
		else:
			print('SolarPV: Setting configuration registers at I2C address {} and {}'.format(hex(self._address),hex(self._address + 1)))
		
	def set_i2c_address(self, address):
		assert address % 2 == 0, 'Address must be divisible by 2'
		self._address = address
		
	def __init__(self):
		self._id = 1
		self._sense_command = 0
		self._actuate_command = 3
		self._address = None
		self.connected = False
		
	def __repr__(self):
		if self._address == None:
			return 'HydrogenStorage(): id = {}. last address = None. connected = {}'.format(self._id, self.connected)
		else:
			return 'HydrogenStorage(): id = {}. last address = {}. connected = {}'.format(self._id, hex(self._address), self.connected)
		
class WindTurbine():
	def actuate(self, power):
		if power >= 1.0:
			print('WindTurbine: power should not be >= 1.0, writing byte as 0xff')
			send_byte = 0xff
		elif power < 0.0:
			print('WindTurbine: power should not be < 0.0, writing byte as 0x00')
			send_byte = 0x00
		else:
			send_byte = math.floor(power * 256)
		send_byte &= 0xff
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					bus.write_word_data(self._address + 1, self._actuate_command, send_byte)
			except:
				print('WindTurbine: Could not write to I2C address {} with byte {} and command {}'.format(hex(self._address + 1), hex(send_byte), self._command))
		else:
			print('WindTurbine: Actuating power as byte {} to I2C address {}'.format(hex(send_byte), hex(self._address + 1)))
		
	def sense(self):
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					retrieve_byte = bus.read_word_data(self._address + 1, self._sense_command)
			except:
				print('WindTurbine: Could not read from I2C address {} with command {}'.format(hex(self._address + 1), self._sense_command))
		else:
			retrieve_byte = 10
			print('WindTurbine: Sensing power as byte {} from I2C address {}'.format(hex(retrieve_byte), hex(self._address + 1)))
		return retrieve_byte * 0.00390625

	def configure(self):
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					bus.write_word_data(self._address, 6, 0xff)
					bus.write_word_data(self._address + 1, 6, [0xff, 0x00])
			except:
				print('WindTurbine: Could not set configuration registers at I2C address {} or {}'.format(hex(self._address),hex(self._address + 1)))
		else:
			print('WindTurbine: Setting configuration registers at I2C address {} and {}'.format(hex(self._address),hex(self._address + 1)))
		
	def set_i2c_address(self, address):
		assert address % 2 == 0, 'Address must be divisible by 2'
		self._address = address
		
	def __init__(self):
		self._id = 2
		self._sense_command = 0
		self._actuate_command = 3
		self._address = None
		self.connected = False
		
	def __repr__(self):
		if self._address == None:
			return 'HydrogenStorage(): id = {}. last address = None. connected = {}'.format(self._id, self.connected)
		else:
			return 'HydrogenStorage(): id = {}. last address = {}. connected = {}'.format(self._id, hex(self._address), self.connected)
		
class Household():
	def actuate(self, power):
		if power >= 1.0:
			print('Household: power should not be >= 1.0, writing byte as 0xff')
			send_byte = 0xff
		elif power < 0.0:
			print('Household: power should not be < 0.0, writing byte as 0x00')
			send_byte = 0x00
		else:
			send_byte = math.floor(power * 256)
		send_byte &= 0xff
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					bus.write_word_data(self._address + 1, self._actuate_command, send_byte)
			except:
				print('Household: Could not write to I2C address {} with byte {} and command {}'.format(hex(self._address + 1), hex(send_byte), self._command))
		else:
			print('Household: Actuating power as byte {} to I2C address {}'.format(hex(send_byte), hex(self._address + 1)))
		
	def sense(self):
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					retrieve_byte = bus.read_word_data(self._address + 1, self._sense_command)
			except:
				print('Household: Could not read from I2C address {} with command {}'.format(hex(self._address + 1), self._sense_command))
		else:
			retrieve_byte = 10
			print('Household: Sensing power as byte {} from I2C address {}'.format(hex(retrieve_byte), hex(self._address + 1)))
		return retrieve_byte * 0.00390625

	def configure(self):
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					bus.write_word_data(self._address, 6, 0xff)
					bus.write_word_data(self._address + 1, 6, [0xff, 0x00])
			except:
				print('Household: Could not set configuration registers at I2C address {} or {}'.format(hex(self._address),hex(self._address + 1)))
		else:
			print('Household: Setting configuration registers at I2C address {} and {}'.format(hex(self._address),hex(self._address + 1)))
		
	def set_i2c_address(self, address):
		assert address % 2 == 0, 'Address must be divisible by 2'
		self._address = address
		
	def __init__(self):
		self._id = 3
		self._sense_command = 0
		self._actuate_command = 3
		self._address = None
		self.connected = False
		
	def __repr__(self):
		if self._address == None:
			return 'HydrogenStorage(): id = {}. last address = None. connected = {}'.format(self._id, self.connected)
		else:
			return 'HydrogenStorage(): id = {}. last address = {}. connected = {}'.format(self._id, hex(self._address), self.connected)
		
class ElectricVehicle():
	def actuate(self, state_of_charge):
		if state_of_charge >= 1.0:
			print('ElectricVehicle: state_of_charge should not be >= 1.0, writing byte as 0xff')
			send_word = 0xffff
		elif state_of_charge < 0.0:
			print('ElectricVehicle: state_of_charge should not be < 0.0, writing byte as 0x00')
			send_word = 0x0000
		else:
			if state_of_charge > 0.0625:
				send_word = 1
				for i in range(2,17):
					if state_of_charge > i*0.0625:
						send_word *= 2
						send_word += 1
					else:
						break
			else:
				send_word = 0
		send_bytes = [(send_word >> 8) & 0xff, send_word & 0xff]
		hex_bytes = ["0x%02x" % n for n in send_bytes]
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					bus.write_word_data(self._address + 1, self._actuate_command, send_bytes)
			except:
				print('ElectricVehicle: Could not write to I2C address {} with bytes {} and command {}'.format(hex(self._address + 1), hex_bytes, self._command))
		else:
			print('ElectricVehicle: Actuating state_of_charge as bytes {} to I2C address {}'.format(hex_bytes, hex(self._address + 1)))
		
	def get_amount(self):
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					retrieve_byte = bus.read_word_data(self._address, self._amount_command)
			except:
				print('ElectricVehicle: Could not read from I2C address {} with command {}'.format(hex(self._address), self._amount_command))
		else:
			retrieve_byte = 0b01101001
			print('ElectricVehicle: Sensing amount as byte {} from I2C address {}'.format(hex(retrieve_byte), hex(self._address)))
		count = 0
		while count:
			retrieve_byte &= (retrieve_byte-1)
			count += 1
		return count

	def configure(self):
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					bus.write_word_data(self._address, 6, [0xff, 0xff])
					bus.write_word_data(self._address + 1, 6, [0x00, 0x00])
			except:
				print('ElectricVehicle: Could not set configuration registers at I2C address {} or {}'.format(hex(self._address),hex(self._address + 1)))
		else:
			print('ElectricVehicle: Setting configuration registers at I2C address {} and {}'.format(hex(self._address), hex(self._address + 1)))
		
	def set_i2c_address(self, address):
		assert address % 2 == 0, 'Address must be divisible by 2'
		self._address = address
		
	def __init__(self):
		self._id = 4
		self._amount_command = 1
		self._actuate_command = 2
		self._address = None
		self.connected = False
			
	def __repr__(self):
		if self._address == None:
			return 'HydrogenStorage(): id = {}. last address = None. connected = {}'.format(self._id, self.connected)
		else:
			return 'HydrogenStorage(): id = {}. last address = {}. connected = {}'.format(self._id, hex(self._address), self.connected)
		
class HydrogenStorage():
	def actuate(self, state_of_charge):
		if state_of_charge >= 1.0:
			print('HydrogenStorage: state_of_charge should not be >= 1.0, writing byte as 0xff')
			send_word = 0xffff
		elif state_of_charge < 0.0:
			print('HydrogenStorage: state_of_charge should not be < 0.0, writing byte as 0x00')
			send_word = 0x0000
		else:
			if state_of_charge > 0.0625:
				send_word = 1
				for i in range(2,17):
					if state_of_charge > i*0.0625:
						send_word *= 2
						send_word += 1
					else:
						break
			else:
				send_word = 0
		send_bytes = [(send_word >> 8) & 0xff, send_word & 0xff]
		hex_bytes = ["0x%02x" % n for n in send_bytes]
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					bus.write_word_data(self._address + 1, self._actuate_command, send_bytes)
			except:
				print('HydrogenStorage: Could not write to I2C address {} with byte {} and command {}'.format(hex(self._address + 1), hex_bytes, self._command))
		else:
			print('HydrogenStorage: Actuating state_of_charge as byte {} to I2C address {}'.format(hex_bytes, hex(self._address + 1)))
		
	def get_soc(self):
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					retrieve_byte = bus.read_word_data(self._address, self._amount_command)
			except:
				print('HydrogenStorage: Could not read from I2C address {} with command {}'.format(hex(self._address), self._amount_command))
		else:
			retrieve_byte = 10
			print('HydrogenStorage: Sensing amount as byte {} from I2C address {}'.format(hex(retrieve_byte), hex(self._address)))
		return retrieve_byte * 0.00390625

	def configure(self):
		if __USEPINS__ == True:
			try:
				with SMBus as bus:
					bus.write_word_data(self._address, 6, [0xff, 0xff])
					bus.write_word_data(self._address + 1, 6, [0x00, 0x00])
			except:
				print('HydrogenStorage: Could not set configuration registers at I2C address {} or {}'.format(hex(self._address),hex(self._address + 1)))
		else:
			print('HydrogenStorage: Setting configuration registers at I2C address {} and {}'.format(hex(self._address), hex(self._address + 1)))
		
	def set_i2c_address(self, address):
		assert address % 2 == 0, 'Address must be divisible by 2'
		self._address = address
		
	def __init__(self):
		self._id = 4
		self._amount_command = 1
		self._actuate_command = 2
		self._address = None
		self.connected = False
		
	def __repr__(self):
		if self._address == None:
			return 'HydrogenStorage(): id = {}. last address = None. connected = {}'.format(self._id, self.connected)
		else:
			return 'HydrogenStorage(): id = {}. last address = {}. connected = {}'.format(self._id, hex(self._address), self.connected)
		
def startup():
	modelList = [
		SolarPV(),
		WindTurbine(),
		Household(),
		ElectricVehicle(),
		HydrogenStorage()
		]
	
	return modelList
	
def update(modelList):
	# Set all objects to disconnnected
	for model in modelList:
		model.connected = False
	
	
	if __USEPINS__ == True:
		command = 0
		# Check all i2c addresses for models
		for address in range(0x10,0x30,2) + range(0x50,0xd0,2) + range(0x70,0x78,2):	# Would have been range(0x20,0x60,4), range(0xa0,0xd0,4), (0xe0,0xf0,4) in 8 bit interface
				try:
					with SMBus(1) as bus:
						id = bus.read_word_data(address,command)
					# if id == 0:
						# print('Found a model with id == 0 at I2C address {}. This id is reserved for special uses in future code.'.format(address) )
					# else:
					modelList[id].connected = True
					modelList[id].set_i2c_address(address)
					modelList[id].configure()
				except:
					pass
	else:
		# Connect SolarPV and EV in test cases
		modelList[0].connected = True
		modelList[0].set_i2c_address(0x10)
		modelList[0].configure()
		modelList[3].connected = True
		modelList[3].set_i2c_address(0x10)
		modelList[3].configure()
		print('Checking all i2c addresses for models. solarPV at address 0x10')
