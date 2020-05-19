import Client.hhub as hhub

from Client import __USEPINS__

# When running this script from the top directory, run this with -m:
# python3 -m Client.tests.test_hhub

# Make sure __USEPINS__ is set correctly

print("test_hhub.py: __USEPINS__ is set to ", __USEPINS__)
print("__________________________________________")

# Try to detect I2C devices
print("hhub.getConnected returns ", hhub.getConnected(1))

# Try to set value for solarpv
print("hhub.setModel returns ", hhub.setModel(2e6, hhub.Model.SOLARPV, 0e6, 6e6))

# Try to retrieve value from solarpv
print("hhub.getModel returns ", hhub.getModel(hhub.Model.SOLARPV, 0e6, 6e6))
