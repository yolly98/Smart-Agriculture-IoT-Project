import command
import from_node
import time
import math
import threading
import view_db
import mysql_module

# ------------MAIN-----------

command.get_config(True)


#functinon for thread 1(console)
def server_console():
    while True:

        cmd = input("$ Type a number or help: ")
        if cmd == "help":
            print("[!] command list:")
            print("----------- SHOW DATA -------------")
            print(".[1]     view lands")
            print(".[2]     view configurations")
            print(".[3]     view last measurements")
            print(".[4]     view last violations")
            print(".[5]     view last irrigations")
            print("------- COMMAND TO NODES-----------")
            print(".[6]     irr_cmd")
            print(".[7]     get_config")
            print(".[8]     assign_config")
            print(".[9]     timer_cmd")
            print(".[10]    get_sensor")
            print(".[11]    is_alive")
            print("--------- OTHERS ------------------")
            print(".[12]    test received messages")
            print(".[13]    exit")
            cmd = input("$ Type a number or help: ")

        if cmd.isdigit() and int(cmd) == 1:
            view_db.view_lands()
        elif cmd.isdigit() and int(cmd) == 2:
            view_db.view_configurations()
        elif cmd.isdigit() and int(cmd) == 3:
            view_db.view_last_measurements()
        elif cmd.isdigit() and int(cmd) == 4:
            view_db.view_last_violations()
        elif cmd.isdigit() and int(cmd) == 5:
            view_db.view_last_irrigations()
        elif cmd.isdigit() and int(cmd) == 6:
            command.irr_cmd()
        elif cmd.isdigit() and int(cmd) == 7:
            command.get_config(False)
        elif cmd.isdigit() and int(cmd) == 8:
            command.assign_config(0, 0)
        elif cmd.isdigit() and int(cmd) == 9:
            command.timer_cmd()
        elif cmd.isdigit() and int(cmd) == 10:
            command.get_sensor()
        elif cmd.isdigit() and int(cmd) == 11:
            command.is_alive(False)
        elif cmd.isdigit() and int(cmd) == 12:
            cmd = input("[!] Type the TOPIC or help: ")
        
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
                cmd = input("[!] Type the TOPIC or help: ")

            if cmd.isdigit() and int(cmd) == 9:
                continue
            elif cmd.isdigit() and int(cmd) == 1:
                from_node.config_request()
            elif cmd.isdigit() and int(cmd) == 2:
                from_node.status()
            elif cmd.isdigit() and int(cmd) == 3:
                from_node.irrigation()
            elif cmd.isdigit() and int(cmd) == 4:
                from_node.moisture()
            elif cmd.isdigit() and int(cmd) == 5:
                from_node.ph()
            elif cmd.isdigit() and int(cmd) == 6:
                from_node.light()
            elif cmd.isdigit() and int(cmd) == 7:
                from_node.tmp()
            elif cmd.isdigit() and int(cmd) == 8:
                from_node.is_alive_ack()
            else:
                print("[-] topic non valid!")
        elif cmd.isdigit() and int(cmd) == 13:
            print("Press Ctrl+c in order to stop the listener")
            exit()
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
            command.is_alive(True)
            mysql_module.set_all_node_offline()
            start_timer = time.time()

        time.sleep(0.1)
            
            
            

t1 = threading.Thread(target = server_console, args = (), daemon = False)
t2 = threading.Thread(target = server_listener, args = (), daemon = True) 

t1.start()
t2.start()

t1.join()
t2.join()



