# COAP server

## Example 1 - How to use

* 1 ) open cooja
* 2 ) create mote using "coap_server_led.c"
* 3 ) go to "Tools/Serial Socket(SERVER)" and press Start
* 4 ) install coap client on linux if is not installed
    * > sudo apt-get install libcoap-1-0-bin
* 5 ) contact the coap server
    * > coap-client -m get coap://[fd00:201:1:1:1]/led  (will be //[address]/resource_name)

## Example 2 - How to use


* 1 ) open cooja
* 2 ) create mote using "coap_server_led.c"
* 3 ) go to "Tools/Serial Socket(SERVER)" and press Start
* 4 ) install coap client on linux if is not installed
    * > sudo apt-get install libcoap-1-0-bin
* 5 ) outside the contiki container start the webserver
    * > cd project-folder
    * > sudo rm -r build
    * > make TARGET=cooja connect-router-cooja
* 6 ) contact the coap server with the following commands
    * > coap-client -m get coap://[fd00:201:1:1:1]/home                     (will be //[address]/resource_name)
    * > coap-client -m get coap://[fd00:201:1:1:1]/home?room=0              (see the room with index 0)
    * > coap-client -m post coap://[fd00:201:1:1:1]/home -e room=bathroom    (add a room)
    * > coap-client -m put coap://[fd00:201:1:1:1]/home -e index=0\&tmp=25  (set temperature 10 to room with index 0)

