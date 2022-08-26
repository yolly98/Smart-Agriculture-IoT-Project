import command
import from_node
import time
import math
import threading

# ------------MAIN-----------

command.get_config(True)


#functinon for thread 1(console)
def server_console():
    while True:

        cmd = input("$ Type a command: ")
        if cmd == "help":
            print("[!] command list:")
            print(". irr_cmd")
            print(". get_config")
            print(". assign_config")
            print(". timer_cmd")
            print(". get_sensor")
            print(". is_alive")
            print(". test")
            print(". cancel")
            continue
        elif cmd == "cancel":
            continue
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
            command.is_alive()
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

    start_timer = time.time()
    while True:
        #TODO check if there is a message from nodes
        time.sleep(0.1)
        day = 60 * 60 * 24
        timer = math.floor((time.time()-start_timer)/day)
        if timer >= 1:
            start_timer = timer.time()
            #TODO put offline the node that the last message is older than 12 hours
            

t1 = threading.Thread(target = server_console, args = (), daemon = False)
t2 = threading.Thread(target = server_listener, args = (), daemon = True) 

t1.start()
t2.start()

t1.join()
t2.join()



