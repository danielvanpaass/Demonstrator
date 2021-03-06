This is the project repository for the Illuminator project. It is being made by the BAP Group G of 4th quarter of year 2019-2020.

*****************
Project structure
*****************
The repository is split up into two directories, because one Raspberry Pi needs to run as a server, and the others as clients.

...Meer geblaat...

******************
Setup instructions
******************
0. Set one Pi up as a server as per the following guide: https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/net_tutorial.md
0. Make sure your Pi is up-to-date
	sudo apt update | sudo apt upgrade
1. Make sure you have pip installed on the Pis
	sudo apt install python3-pip
1. Make sure the mosquitto broker is installed (on the Server only) for communication between Pi's. (note that the addresses of the clients are probably one higher now (e.g. 103 -> 104))
    sudo apt install mosquitto
    sudo systemctl enable mosquitto
    sudo reboot
1. Change the name of the Client Pi's from raspberrypi to raspberrypiClient so that the Pi's can identify the Server during messages
    sudo sed -i 's/raspberrypi/raspberrypiClient/g' /etc/hostname
    sudo nano /etc/hosts #change the word localhost and raspberrypi to raspberrypiClient as follows (leave the middle part as is):

    ##
    #127.0.0.1       raspberrypiClient
    #.. ...
    #.. ...
    #127.0.1.1       raspberrypiClient
    ##
2. To be able to import numpy on a Raspbian you need libatlas
    sudo apt-get install libatlas-base-dev
2. Install the required packages listed in requirements.txt
	pip3 install -r requirements.txt
3. Turn on I2C on the Pi. When using the command line interface:
	sudo raspi-config
   Go to Interfacing Options and then enable I2C
   Reboot the Pi
	sudo reboot
4. Install

*****************
Using Client.hhub
*****************
The Client.hhub functions use the GPIO pins found on the Raspberry Pi. Since most of the testing is not done on the Pis themselves, this will cause an error if you try to use them on ie. a Windows machine.
Therefore there is the __USEPINS__ variable in the __INIT__.py of the Client. Import it using:
	from Client import __USEPINS__

Set it to True if you want to use the GPIO pins. If it is set to False, it will use dummy values.

To run the test_hhub, use the following command:
	python3 -m Client.tests.test_hhub

If you want to check the I2C addresses of the table-top models, install i2c-tools with:
	sudo apt install -y i2c-tools
and run the command:
	sudo i2cdetect -y 1
