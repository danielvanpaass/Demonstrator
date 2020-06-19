import Client.hhub as hhub

from Client import __USEPINS__

# When running this script from the top directory, run this with -m:
# python3 -m Client.tests.test_hhub

bytes = [0x40,0x04]
hex_bytes = ["0x%02x" % n for n in bytes]
print(hex_bytes)

# Make sure __USEPINS__ is set correctly

print("test_hhub.py: __USEPINS__ is set to ", __USEPINS__)
print("__________________________________________\n")

# Startup the hardware hub
modelList = hhub.startup()

# Get a list of connected devices
hhub.update(modelList)
print("\nmodelList = {}\n".format(modelList))

# Actuate only solar PV
modelList[0].actuate(0.75) # SolarPV is at id 1

# Get sensor value from solar PV as fraction between 0 and 1
new_power = modelList[0].sense() # Same as above if solarPV is at place 1
print("\nmodelList[0].sense() = {}\n".format(new_power))

# Set LED lights in ElectricVehicle and get amount
modelList[3].actuate(0.75)
print("\nAmount of EVs = {}\n".format(modelList[3].get_amount()))