# Smart Agricolture IoT project


# Software

* Contiki-ng 
* Mysql
* Paho
* Coapthon

To test the project it was used docker

# components

* Python server
* MQTT node
* COAP node
* border router node
* MQTT broker (mosquitto)

# test on cooja

1. enter in the contiki docker's container in witch is the project folder
	* > sudo docker ps -i
	* > sudo docker start [id contiki] (if not already started)
	* > sudo docker exec -it [id contiki] bash
	* > cd tools/cooja
	* > ant run

2. start mqtt broker by the terminal of your machine (not in container)
	* > mosquitto -v

3. start cooja simulation by opening the simulation "smart_agricolture_cooja_sim.csc"

4. open a new terminal in your machine
	* go to project folder
	* > cd border-router/web-server
	* > make TARGET=cooja connect-router-cooja

5. open a new terminal in your machine
	* go to project folder
	* > cd python-server
	* > python3 server.py

6. configure nodes by clicking on button in their menu (right click)

7. use server, enter "help" to see command, view server log

# test on real node

0. flash all nodes
* for each node connected to the pc i have to know the port tty
* cd /dev
* ls
* cat ttyACM0 (see serial optuput)
* try all ttyACM?, the correct one is that respond you from serial
* remember that in the commands to flash and get output you have to replace "ttyACMX" with the correct port and you have to assign different NODE-ID for each node.

1. How to flash and get otput of launchpad
* flash: "make TARGET=cc26x0-cc13x0 BOARD=/launchpad/cc2650 PORT=/dev/ttyACMx NODEID=0x0001 source-code-name.upload"
* get output: "make TARGET=cc26x0-cc13x0 BOARD=/launchpad/cc2650 PORT=/dev/ttyACMx login"

2. How to flash and get output of dongle
* flash: "make TARGET=nrf52840 BOARD=dongle PORT=/dev/ttyACMx NODEID=0x0001 source-code-name.dfu-upload"
* get output: "make TARGET=nrf52840 BOARD=dongle PORT=/dev/ttyACMx login"

3. command to start the border-router server on linux machine "make TARGET=cc26x0-cc13x0 PORT=/dev/ttyACM0 connect-router" (in this case the border-router was flashed in a launcher)	


* example commands to flash 2 launcher and 3 dongle:
* make TARGET=cc26x0-cc13x0 BOARD=/launchpad/cc2650 PORT=/dev/ttyACM0 NODEID=0x0001 border-router.upload
* make TARGET=cc26x0-cc13x0 BOARD=/launchpad/cc2650 PORT=/dev/ttyACM2 NODEID=0x0002 coap-node.upload 
* make TARGET=nrf52840 BOARD=dongle PORT=/dev/ttyACM4 NODEID=0x0003 coap-node.dfu-upload
* make TARGET=nrf52840 BOARD=dongle PORT=/dev/ttyACM5 NODEID=0x0004 mqtt-node.dfu-upload
* make TARGET=nrf52840 BOARD=dongle PORT=/dev/ttyACM6 NODEID=0x0005 mqtt-node.dfu-upload
