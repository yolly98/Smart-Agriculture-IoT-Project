# Smart Agricolture IoT project


# Software

* Contiki-ng 
* Mysql
* Paho
* Coapthon

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
	
