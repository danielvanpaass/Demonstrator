This is the project repository for the Illuminator project. It is being made by the BAP Group G of 4th quarter of year 2019-2020.

*****************
Project structure
*****************
The repository is split up into two directories, because one Raspberry Pi needs to run as a server, and the others as clients.

...Meer geblaat...

******************
Setup instructions
******************
0. Make sure your Pi is up-to-date
	sudo apt update | sudo apt upgrade
1. Make sure you have pip installed on the Pis
	sudo apt install python3-pip
2. Install the required packages listed in requirements.txt
	pip3 install -r requirements.txt
3. 

*****************
Using Client.hhub
*****************
The Client.hhub functions use the GPIO pins found on the Raspberry Pi. Since most of the testing is not done on the Pis themselves, this will cause an error if you try to use them on ie. a Windows machine.
Therefore there is the __USEPINS__ variable in the __INIT__.py of the Client. Import it using:
from Client import __USEPINS__

Set it to True if you want to use the GPIO pins. If it is set to False, it will use dummy values.

To run the test_hhub, use the following command:
python3 -m Client.tests.test_hhub
