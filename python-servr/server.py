import command
import from_node
import time
import math
import threading
import view_db

# ------------MAIN-----------

command.get_config(True)


#functinon for thread 1(console)
def server_console():
    while True:

        cmd = input("$ Type a command: ")
        if cmd == "help":
            print("[!] command list:")
            print(". view_lands")
            print(". view_configurations")
            print(". view_last_measurements")
            print(". view_last_violations")
            print(". view_last_irrigations")
            print(". irr_cmd")
            print(". get_config")
            print(". assign_config")
            print(". timer_cmd")
            print(". get_sensor")
            print(". is_alive")
            print(". test")
            print(". exit")
            print(". cancel")
            continue
        elif cmd == "cancel":
            continue
        elif cmd == "view_lands":
            view_db.view_lands()
        elif cmd == "view_configurations":
            view_db.view_configurations()
        elif cmd == "view_last_measurements":
            view_db.view_last_measurements()
        elif cmd == "view_last_violations":
            view_db.view_last_violations()
        elif cmd == "view_last_irrigations":
            view_db.view_last_irrigations()
        elif cmd == "irr_cmd":
            command.irr_cmd()
        elif cmd == "get_config":
            command.get_config(False)
        elif cmd == "assign_config":
            command.assign_config(0, 0)
        elif cmd == "timer_cmd":
            command.timer_cmd()
        elif cmd == "get_sensor":
            command.get_sensor()
        elif cmd == "is_alive":
            command.is_alive(False)
        elif cmd == "test":
            cmd = input("[!] Type the TOPIC: ")
        
            if cmd == "help":
                print(". CONFIG_RQST")
                print(". STATUS")
                print(". IRRIGATION")
                print(". MOISTURE")
                print(". PH")
                print(". LIGHT")
                print(". TMP")
                print(". IS_ALIVE_ACK")
                print(". cancel")
            elif cmd == "cancel":
                continue
            elif cmd == "CONFIG_RQST":
                from_node.config_request()
            elif cmd == "STATUS":
                from_node.status()
            elif cmd == "IRRIGATION":
                from_node.irrigation()
            elif cmd == "MOISTURE":
                from_node.moisture()
            elif cmd == "PH":
                from_node.ph()
            elif cmd == "LIGHT":
                from_node.light()
            elif cmd == "TMP":
                from_node.tmp()
            elif cmd == "IS_ALIVE_ACK":
                from_node.is_alive_ack()
            else:
                printf("[-] topic non valid!")
        else:
            print("[-] command not valid!")

#functino for thread 2 (daemon)
def server_listener():

    end_timer =  60 * 60 * 3    # 3 hours
    start_timer = time.time()
    while True:
        
        #TODO check if there is a message from nodes
        
        #check if nodes are online
        if (time.time() - start_timer) >= end_timer:
            #TODO put offline all node in mysql db (the is_alive_ack will put them online)
            start_timer = timer.time()

        time.sleep(0.1)
            
            
            

t1 = threading.Thread(target = server_console, args = (), daemon = False)
t2 = threading.Thread(target = server_listener, args = (), daemon = True) 

t1.start()
t2.start()

t1.join()
t2.join()



