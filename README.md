# Smart Agricolture IoT project

# components

* Python server
* MQTT node
* COAP node
* border router node
* MQTT broker (mosquitto)

# test on cooja

* enter in the contiki docker's container in witch is the project folder
	> sudo docker ps -i
	> sudo docker start [id contiki] (if not already started)
	> sudo docker exec -it [id contiki] bash
	> cd tools/cooja
	> ant run

* start mqtt broker by the terminal of your machine (not in container)
	> mosquitto -v

* start cooja simulation by opening the simulation "smart_agricolture_iot_project.csc"

* open a new terminal in your machine and go to project folder
	> cd border-router/web-server
	> make TARGET=cooja connect-router-cooja

* open a new terminal in your machine and go to project folder
	> cd python-server
	> python3 server.py

* configure nodes by clicking on button in their menu (right click)

* use server, enter "help" to see command, view server log
	
