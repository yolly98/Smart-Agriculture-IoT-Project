import datetime
from threading import *
import json
import logging

LOG_MODE = 0
LOG_LOCK = Condition()

def log_init(log_mode):

    global LOG_MODE
    if log_mode == "verbose" or log_mode == "-v":
        print("selected log verbose mode")
        LOG_MODE = 1
    else:
        print("selected log normal mode")
        LOG_MODE = 0
        logging.disable(logging.CRITICAL)
    
    log_file = open("log.txt", "w")
    log_file.write("-----------------------------------------\n")
    log_file.close()

#-------------------

def log_receive(msg, land_id, node_id):

    global LOG_MODE
    global LOG_LOCK

    LOG_LOCK.acquire()

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())

    if LOG_MODE == 1 :
        print(f" <  [{msg['cmd']}] ({land_id}, {node_id})")

    log_file.write(f"[{current_time}]  <  {msg} from ({str(land_id)}, {node_id})\n")
    log_file.close()

    LOG_LOCK.release()

#-------------------

def log_send(msg, land_id, node_id):

    global LOG_MODE
    global LOG_LOCK

    LOG_LOCK.acquire()

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    if LOG_MODE == 1 :
        print(f" >  {msg} to ({land_id}, {node_id})")

    log_file.write(f"[{current_time}]  >  {msg} to ({land_id}, {node_id})\n")
    log_file.close()

    LOG_LOCK.release()

#-------------------

def log_err(msg):

    global LOG_MODE
    global LOG_LOCK

    LOG_LOCK.acquire()

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    print("[-] ", msg)

    log_file.write(f"[{current_time}] [-] {msg}\n")
    log_file.close()

    LOG_LOCK.release()

#-------------------

def log_success(msg):

    global LOG_MODE
    global LOG_LOCK

    LOG_LOCK.acquire()

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    print("[+] ", msg)

    log_file.write(f"[{current_time}] [+] {msg}\n")
    log_file.close()

    LOG_LOCK.release()

#---------------------

def log_info(msg):

    global LOG_MODE
    global LOG_LOCK

    LOG_LOCK.acquire()

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    print("[!] ", msg)

    log_file.write(f"[{current_time}] [!] {msg}\n")
    log_file.close()

    LOG_LOCK.release()
    
#--------------------

def log_input(msg):

    global LOG_MODE
    global LOG_LOCK

    key_input = input(msg)

    LOG_LOCK.acquire()

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    log_file.write(f"[{current_time}] [k] {msg}{key_input}\n")
    log_file.close()

    LOG_LOCK.release()

    return key_input