import datetime
from threading import *
import json

LOG_MODE = 0

def log_init(log_mode):

    global LOG_MODE
    if log_mode == "verbose" or log_mode == "-v":
        print("selected log verbose mode")
        LOG_MODE = 1
    else:
        print("selected log normal mode")
        LOG_MODE = 0
    log_file = open("log.txt", "w")
    log_file.write("-----------------------------------------\n")
    log_file.close()

#-------------------

def log_receive(msg, land_id, node_id):

    global LOG_MODE
    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())

    if LOG_MODE == 1 :
        print(f" <  [{msg['cmd']}] ({land_id}, {node_id})")

    log_file.write(f"[{current_time}]  <  {msg} from ({str(land_id)}, {node_id})\n")
    log_file.close()

#-------------------

def log_send(msg, land_id, node_id):

    global LOG_MODE
    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    if LOG_MODE == 1 :
        print(f" >  {msg} to ({land_id}, {node_id})")

    log_file.write(f"[{current_time}]  >  {msg} to ({land_id}, {node_id})\n")
    log_file.close()
#-------------------

def log_err(msg):

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    print("[-] ", msg)

    log_file.write(f"[{current_time}] [-] {msg}\n")
    log_file.close()

#-------------------

def log_success(msg):

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    print("[+] ", msg)

    log_file.write(f"[{current_time}] [+] {msg}\n")
    log_file.close()

#---------------------

def log_info(msg):

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    print("[!] ", msg)

    log_file.write(f"[{current_time}] [!] {msg}\n")
    log_file.close()

#--------------------

def log_input(msg):

    key_input = input(msg)

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    log_file.write(f"[{current_time}] [k] {msg}{key_input}\n")
    log_file.close()

    return key_input