import datetime
from threading import *
import json

def log_init():
    log_file = open("log.txt", "w")
    log_file.write("-----------------------------------------\n")
    log_file.close()

#-------------------

def log_receive(msg):

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    if not current_thread().isDaemon():
        print(" <  ", msg)
    else:
        print(f" < [{msg['cmd']}] from node ({msg['body']['land_id']},{msg['body']['node_id']})")

    log_file.write(f"[{current_time}]  <  {msg}\n")
    log_file.close()

#-------------------

def log_send(msg):

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    if not current_thread().isDaemon():
        print(" >  ", msg)

    log_file.write(f"[{current_time}]  >  {msg}\n")
    log_file.close()
#-------------------

def log_err(msg):

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    if not current_thread().isDaemon():
        print("[-] ", msg)

    log_file.write(f"[{current_time}] [-] {msg}\n")
    log_file.close()

#-------------------

def log_success(msg):

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    if not current_thread().isDaemon():
        print("[+] ", msg)

    log_file.write(f"[{current_time}] [+] {msg}\n")
    log_file.close()

#---------------------

def log_info(msg):

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    if not current_thread().isDaemon():
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