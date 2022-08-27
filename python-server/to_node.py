import json
from persistence import get_mysql_db

#--------------------COMMAND TO NODE--------------

def irr_cmd():
    print("[!] Type the arguments ...")
    land_id = input("$ land_id: ")
    node_id = input("$ node_id: ")
    enable = input("$ enable: ")
    status = input("$ status: ")
    limit = input("$ limit: ")
    irr_duration = input("$ irr_duration: ")
    
    if not land_id.isdigit():
        print("[-] land_id has to be a number [", land_id, "]")
        return

    if not node_id.isdigit():
        print("[-] node_id has to be a number [", node_id, "]")
        return

    if enable != "true" and enable != "false" and len(enable) != 0:
        print("[-] enable is not valid [", enable, "]")
        return
    elif len(enable) == 0:
        enable = "null"

    if status != "on" and status != "off" and len(status) != 0:
        print("[-] status is not valid [", status, "]")
        return
    elif len(status) == 0:
        status = "null"

    if (not limit.isdigit()) and len(limit) != 0:
        print("[-] limit has to be a number [", limit, "]")
        return
    elif len(limit) == 0:
        limit = 0

    if (not irr_duration.isdigit()) and len(irr_duration) != 0:
        print("[-] irr_duration has to be a number [", irr_duration, "]")
        return
    elif len(irr_duration) == 0:
        irr_duration = 0

    
    msg = { 'land_id': int(land_id), 'node_id': int(node_id), 'enable': enable, 'status': status, 'limit': int(limit), 'irr_duration': int(irr_duration) }
    json_msg = json.dumps(msg)
    topic = "IRR_CMD"
    print(" >  [", topic, "] ", json_msg)

#---------

def get_config(broadcast):

    if( not broadcast):
        print("[!] Type the arguments ...")
        land_id = input("$ land_id: ")
        node_id = input("$ node_id: ")
        
        if not land_id.isdigit():
            print("[-] land_id has to be a number [", land_id, "]")
            return

        if not node_id.isdigit():
            print("[-] node_id has to be a number [", node_id, "]")
            return
    else:
        land_id = 0
        node_id = 0
    
    msg = { 'land_id': int(land_id), 'node_id': int(node_id) }
    json_msg = json.dumps(msg)
    topic = "GET_CONFIG"
    print(" >  [", topic, "] ", json_msg)

#---------

def assign_config(land_id, node_id):

    config = get_mysql_db.get_config(land_id, node_id, True)

    #if is a new node, send the default configuration
    if not config:
        print("[!] (", land_id, ", ", node_id, ") is a new node")
        config = get_mysql_db.get_config(land_id, 0, True)
        if not config:
            print("[-] mysqldb: the land ", land_id, " doesn't exist or return too many result")
            return

    msg = { 'land_id': land_id, 'node_id': node_id, 'irr_config': { 'enabled': config[4], 'irr_limit':  config[5], 'irr_duration': config[6]}, 'mst_timer': config[7], 'ph_timer': config[8], 'light_timer': config[9], 'tmp_timer': config[10] }
    json_msg = json.dumps(msg)
    topic = "ASSIGN_CONFIG"
    print(" >  [", topic, "] ", json_msg)

    #save the new configuration
    if config[1] == 0:
        get_mysql_db.add_configuration(land_id, node_id, "online", config[4], config[5], config[6], config[7], config[8], config[9], config[10])
        

#--------

def timer_cmd():
    print("[!] Type the arguments ...")
    land_id = input("$ land_id: ")
    node_id = input("$ node_id: ")
    sensor = input("$ sensor: ")
    timer = input("$ timer: ")
    
    if not land_id.isdigit():
        print("[-] land_id has to be a number [", land_id, "]")
        return

    if not node_id.isdigit():
        print("[-] node_id has to be a number [", node_id, "]")
        return

    if sensor != "moisture" and sensor != "ph" and sensor != 'light' and sensor != "tmp":
        print("[-] sensor is not valid [", sensor, "]")
        return

    if (not timer.isdigit()) and len(timer) != 0:
        print("[-] timer has to be a number [", timer, "]")
        return
    elif len(timer) == 0:
        timer = 0

    msg = { 'land_id': int(land_id), 'node_id': int(node_id), 'sensor': sensor, 'timer': int(timer) }
    json_msg = json.dumps(msg)
    topic = "TIMER_CMD"
    print(" >  [", topic, "] ", json_msg)

#-------

def get_sensor():
    print("[!] Type the arguments ...")
    land_id = input("$ land_id: ")
    node_id = input("$ node_id: ")
    sensor = input("$ sensor: ")
    
    if not land_id.isdigit():
        print("[-] land_id has to be a number [", land_id, "]")
        return

    if not node_id.isdigit():
        print("[-] node_id has to be a number [", node_id, "]")
        return

    if sensor != "moisture" and sensor != "ph" and sensor != 'light' and sensor != 'tmp':
        print("[-] sensor is not valid [", sensor, "]")
        return

    msg = { 'land_id': int(land_id), 'node_id': int(node_id), 'type': sensor }
    json_msg = json.dumps(msg)
    topic = "GET_SENSOR"
    print(" >  [", topic, "] ", json_msg)

#-------

def is_alive(broadcast):

    if(not broadcast):
        print("[!] Type the arguments ...")
        land_id = input("$ land_id: ")
        node_id = input("$ node_id: ")
        
        if not land_id.isdigit():
            print("[-] land_id has to be a number [", land_id, "]")
            return

        if not node_id.isdigit():
            print("[-] node_id has to be a number [", node_id, "]")
            return
    else:
        land_id = 0
        node_id = 0

    msg = { 'land_id': int(land_id), 'node_id': int(node_id) }
    json_msg = json.dumps(msg)
    topic = "GET_SENSOR"
    print(" >  [", topic, "] ", json_msg)
