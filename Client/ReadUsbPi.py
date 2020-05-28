import usb.core


def connected_usb():
    if usb.core.find(idProduct=25479):
        wind = 1
    else:
        wind = 0

    if usb.core.find(idProduct=39191):
        solar = 1
    else:
        solar = 0
    return wind, solar
