import to_node
import from_node
import time
import math
import threading
import log
from view import get_vw
from view import add_vw
from view import update_vw
from view import delete_vw
from protocol import mqtt_module
from protocol import coap_module
import sys
import os

log_mode = ""
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        log_mode = sys.argv[i]
        break

IS_ALIVE_TIMER = 10*60 #10 minutes

log.log_init(log_mode)
mqtt_module.mqtt_init()

#functinon for thread 1(console)
def server_console():

    while True:

        cmd = log.log_input("Type a number or help: ")
        if cmd == "help":
            log.log_info("Command list:")
            log.log_console("----------- SHOW DATA -----------------|---------- COMMAND TO NODES ------------")
            log.log_console("                                       |                                        ")
            log.log_console(".[1]  view lands                       | .[6]  irr_cmd                          ")
            log.log_console(".[2]  view configurations              | .[7]  get_config                       ") 
            log.log_console(".[3]  view last measurements           | .[8]  assign_config                    ")
            log.log_console(".[4]  view last violations             | .[9]  timer_cmd                        ")       
            log.log_console(".[5]  view last irrigations            | .[10] get_sensor                       ") 
            log.log_console("                                       | .[11] is_alive                         ") 
            log.log_console("                                       |                                        ")    
            log.log_console("-------------- ADD DATA ---------------|------------- UPDATE DATA --------------")
            log.log_console("                                       |                                        ")
            log.log_console(".[12] add new land                     | .[16] update land                      ")
            log.log_console(".[13] add new configuration            | .[17] update configuration             ")
            log.log_console(".[14] add irrigation event             | .[18] set node online                  ")
            log.log_console(".[15] add measurement event            | .[19] set all node offline             ")
            log.log_console("                                       |                                        ")
            log.log_console(" -------------------------------- DELETE DATA ----------------------------------")
            log.log_console("                                       |                                        ")
            log.log_console(".[20] delete land                      | .[24] delete many measurement events   ")                
            log.log_console(".[21] delete configuration             | .[25] delete one measurement event     ")           
            log.log_console(".[22] delete many irrigation events    | .[26] delete many violations           ")
            log.log_console(".[23] delete one irrigation event      | .[27] delete one violation             ")
            log.log_console("                                       |                                        ")
            log.log_console("------------------------------------ OTHERS ------------------------------------")
            log.log_console("                                                                                ")
            log.log_console(".[28] test received messages                                                    ")
            log.log_console(".[29] list of nodes in memory                                                   ")
            log.log_console(".[30] exit                                                                      ")
            log.log_console("                                                                                ")
            log.log_console("--------------------------------------------------------------------------------")
            cmd = log.log_input("Type a number or help: ")

        if cmd.isdigit() and int(cmd) == 1:
            get_vw.view_lands()
        elif cmd.isdigit() and int(cmd) == 2:
            get_vw.view_configurations()
        elif cmd.isdigit() and int(cmd) == 3:
            get_vw.view_last_measurements()
        elif cmd.isdigit() and int(cmd) == 4:
            get_vw.view_last_violations()
        elif cmd.isdigit() and int(cmd) == 5:
            get_vw.view_last_irrigations()
        elif cmd.isdigit() and int(cmd) == 6:
            to_node.irr_cmd()
        elif cmd.isdigit() and int(cmd) == 7:
            broadcast = ""
            while True:
                broadcast = log.log_input("discovery mode? (y/n): ")
                if broadcast == "cancel":
                    return
                if broadcast == "y" or broadcast == "n":
                    break
                else:
                    log.log_err(f"invalid value")
            if broadcast == "y":
                broadcast = True
            else:
                broadcast = False
            to_node.get_config(broadcast)
        elif cmd.isdigit() and int(cmd) == 8:
            to_node.assign_config_cmd()
        elif cmd.isdigit() and int(cmd) == 9:
            to_node.timer_cmd()
        elif cmd.isdigit() and int(cmd) == 10:
            to_node.get_sensor()
        elif cmd.isdigit() and int(cmd) == 11:
            broadcast = ""
            while True:
                broadcast = log.log_input("broadcast mode? (y/n): ")
                if broadcast == "cancel":
                    return
                if broadcast == "y" or broadcast == "n":
                    break
                else:
                    log.log_err(f"invalid value")
            if broadcast == "y":
                broadcast = True
            else:
                broadcast = False
            to_node.is_alive(broadcast)
        elif cmd.isdigit() and int(cmd) == 12:
            add_vw.add_land_vw()
        elif cmd.isdigit() and int(cmd) == 13:
            add_vw.add_configuration_vw()
        elif cmd.isdigit() and int(cmd) == 14:
            add_vw.add_irrigation_event_vw()
        elif cmd.isdigit() and int(cmd) == 15:
            add_vw.add_measurement_event_vw()
        elif cmd.isdigit() and int(cmd) == 16:
            update_vw.update_land_vw()
        elif cmd.isdigit() and int(cmd) == 17:
            update_vw.update_configuration_vw()
        elif cmd.isdigit() and int(cmd) == 18:
            update_vw.set_node_online_vw()
        elif cmd.isdigit() and int(cmd) == 19:
            update_vw.set_all_node_offline_vw()
        elif cmd.isdigit() and int(cmd) == 20:
            delete_vw.delete_land_vw()
        elif cmd.isdigit() and int(cmd) == 21:
            delete_vw.delete_configuration_vw()
        elif cmd.isdigit() and int(cmd) == 22:
            delete_vw.delete_irrigation_many_vw()
        elif cmd.isdigit() and int(cmd) == 23:
            delete_vw.delete_irrigation_one_vw()
        elif cmd.isdigit() and int(cmd) == 24:
            delete_vw.delete_measurement_many_vw()
        elif cmd.isdigit() and int(cmd) == 25:
            delete_vw.delete_measurement_one_vw()
        elif cmd.isdigit() and int(cmd) == 26:
            delete_vw.delete_violation_many_vw()
        elif cmd.isdigit() and int(cmd) == 27:
            delete_vw.delete_violation_one_vw()
        elif cmd.isdigit() and int(cmd) == 28:
            cmd = log.log_input("[!] Type the COMMAND or help: ")
        
            if cmd == "help":
                log.log_console(".[1] CONFIG_RQST")
                log.log_console(".[2] STATUS")
                log.log_console(".[3] IRRIGATION")
                log.log_console(".[4] MOISTURE")
                log.log_console(".[5] PH")
                log.log_console(".[6] LIGHT")
                log.log_console(".[7] TMP")
                log.log_console(".[8] IS_ALIVE_ACK")
                log.log_console(".[9] cancel")
                cmd = log.log_input("[!] Type the TOPIC or help: ")

            if cmd.isdigit() and int(cmd) == 9:
                continue
            elif cmd.isdigit() and int(cmd) == 1:
                from_node.config_request("MQTT", "", "")
            elif cmd.isdigit() and int(cmd) == 2:
                from_node.status("MQTT", "null", "")
            elif cmd.isdigit() and int(cmd) == 3:
                from_node.irrigation("")
            elif cmd.isdigit() and int(cmd) == 4:
                from_node.moisture("")
            elif cmd.isdigit() and int(cmd) == 5:
                from_node.ph("")
            elif cmd.isdigit() and int(cmd) == 6:
                from_node.light("")
            elif cmd.isdigit() and int(cmd) == 7:
                from_node.tmp("")
            elif cmd.isdigit() and int(cmd) == 8:
                from_node.is_alive_ack("")
            else:
                log.log_err(f"command non valid!")
        elif cmd.isdigit() and int(cmd) == 29:
            coap_module.show_coap_nodes()
            mqtt_module.show_mqtt_nodes()
        elif (cmd.isdigit() and int(cmd) == 30) or cmd == "exit":
            log.log_info("exit ...")
            time.sleep(2)
            exit()
        else:
            log.log_err(f"command not valid!")


def check_if_nodes_is_alive():

    end_timer =  IS_ALIVE_TIMER
    start_timer = time.time()
    while True:
        
        #check if nodes are online
        if (time.time() - start_timer) >= end_timer:
            to_node.is_alive(True)
            start_timer = time.time()

        time.sleep(0.1)
            
def mqtt_server_publisher():
    mqtt_module.mqtt_publisher_loop()

def mqtt_server_listener():
    mqtt_module.mqtt_subscribe()

def coap_server_listener():
    coap_module.listener()

t1 = threading.Thread(target = server_console, args = (), daemon = False)
t2 = threading.Thread(target = check_if_nodes_is_alive, args = (), daemon = True) 
t3 = threading.Thread(target = mqtt_server_publisher, args = (), daemon = True) 
t4 = threading.Thread(target = mqtt_server_listener, args = (), daemon = True) 
t5 = threading.Thread(target = coap_server_listener, args = (), daemon = True)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

time.sleep(1)
log.log_console("connecting to nodes ...")
to_node.get_config(True)

t1.join()
os._exit(os.EX_OK)



