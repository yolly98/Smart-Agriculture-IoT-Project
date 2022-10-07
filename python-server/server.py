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

# ------------MAIN-----------
IS_ALIVE_TIMER = 10*60 #1 minute

log.log_init()
mqtt_module.mqtt_init()

#functinon for thread 1(console)
def server_console():

    while True:

        cmd = log.log_input("$ Type a number or help: ")
        if cmd == "help":
            log.log_info("Command list:")
            print("----------- SHOW DATA -------------")
            print(".[1]     view lands")
            print(".[2]     view configurations")
            print(".[3]     view last measurements")
            print(".[4]     view last violations")
            print(".[5]     view last irrigations")
            print("------- COMMAND TO NODES ----------")
            print(".[6]     irr_cmd")
            print(".[7]     get_config")
            print(".[8]     assign_config")
            print(".[9]     timer_cmd")
            print(".[10]    get_sensor")
            print(".[11]    is_alive")
            print("--------- MANAGE DATA -------------")
            print("     ---- ADD DATA ----")
            print(".[12]    add new land")
            print(".[13]    add new configuration")
            print(".[14]    add irrigation event")
            print(".[15]    add measurement event")
            print("     ---- UPDATE DATA ----")
            print(".[16]    update land")
            print(".[17]    update configuration")
            print(".[18]    set node online")
            print(".[19]    set all node offline")
            print("     ---- DELETE DATA ----")
            print(".[20]    delete land")
            print(".[21]    delete configuration")
            print(".[22]    delete many irrigation events")
            print(".[23]    delete one irrigation event")
            print(".[24]    delete many measurement events")
            print(".[25]    delete one measurement event")
            print(".[26]    delete many violations")
            print(".[27]    delete one violation")
            print("--------- OTHERS ------------------")
            print(".[28]    test received messages")
            print(".[29]    list of nodes in memory")
            print(".[30]    exit")
            cmd = log.log_input("$ Type a number or help: ")

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
                print(".[1]     CONFIG_RQST")
                print(".[2]     STATUS")
                print(".[3]     IRRIGATION")
                print(".[4]     MOISTURE")
                print(".[5]     PH")
                print(".[6]     LIGHT")
                print(".[7]     TMP")
                print(".[8]     IS_ALIVE_ACK")
                print(".[9]     cancel")
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
        elif cmd.isdigit() and int(cmd) == 30:
            log.log_info("exit ...")
            log.log_info("press ctrl+C to terminate the other threads")
            time.sleep(2)
            exit()
        else:
            log.log_err(f"command not valid!")

#functino for thread 2 (daemon)
def mqtt_server_check_node():

    end_timer =  IS_ALIVE_TIMER
    start_timer = time.time()
    while True:
        
        #check if nodes are online
        if (time.time() - start_timer) >= end_timer:
            update_vw.set_all_node_offline_vw()
            to_node.is_alive(True)
            start_timer = time.time()

        time.sleep(0.1)
            
def mqtt_server_listener():
    mqtt_module.mqtt_subscribe()

def coap_server_listener():
    coap_module.listener()


t1 = threading.Thread(target = server_console, args = (), daemon = False)
t2 = threading.Thread(target = mqtt_server_check_node, args = (), daemon = True) 
t3 = threading.Thread(target = mqtt_server_listener, args = (), daemon = True) 
t4 = threading.Thread(target = coap_server_listener, args = (), daemon = True)

t1.start()
t2.start()
t3.start()
t4.start()

time.sleep(2)
#to_node.get_config(True)
to_node.is_alive(True)

t1.join()
t2.join()
t3.join()
t4.join()



