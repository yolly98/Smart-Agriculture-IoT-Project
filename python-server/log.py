import datetime
from threading import *

def log_init():
    log_file = open("log.txt", "w")
    log_file.write("-----------------------------------------\n")

#-------------------

def log_receive(msg):

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    if not current_thread().isDaemon():
        print(" <  ", msg)

    log_file.write(f"[{current_time}]  <  {msg}\n")

#-------------------

def log_send(msg):

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    if not current_thread().isDaemon():
        print(" >  ", msg)

    log_file.write(f"[{current_time}]  >  {msg}\n")
#-------------------

def log_err(msg):

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    if not current_thread().isDaemon():
        print("[-] ", msg)

    log_file.write(f"[{current_time}] [-] {msg}\n")

#-------------------

def log_success(msg):

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    if not current_thread().isDaemon():
        print("[+] ", msg)

    log_file.write(f"[{current_time}] [+] {msg}\n")

#---------------------

def log_info(msg):

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    if not current_thread().isDaemon():
        print("[!] ", msg)

    log_file.write(f"[{current_time}] [!] {msg}\n")

#--------------------

def log_input(msg):

    key_input = input(msg)

    log_file = open("log.txt", "a")
    current_time = str(datetime.datetime.now())
    
    log_file.write(f"[{current_time}] [k] {msg}{key_input}\n")

    return key_input