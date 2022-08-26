import json
import mysql.connector

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

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "SELECT * FROM configuration WHERE (land_id = %s) AND (node_id = %s)"
    mycursor.execute(sql, (land_id, node_id))
    myresult = mycursor.fetchone()

    #if is a new node, send the default configuration
    if not myresult:
        print("[!] (", land_id, ", ", node_id, ") is a new node")
        sql = "SELECT * FROM configuration WHERE (land_id = %s) AND (node_id = 0)"
        mycursor.execute(sql, (land_id,))
        myresult = mycursor.fetchone()

    if not myresult:
        print("[-] mysqldb: the land ", land_id, " doesn't exist or return too many result")
        return

    msg = { 'land_id': land_id, 'node_id': node_id, 'irr_config': { 'enabled': myresult[4], 'irr_limit':  myresult[5], 'irr_duration': myresult[6]}, 'mst_timer': myresult[7], 'ph_timer': myresult[8], 'light_timer': myresult[9], 'tmp_timer': myresult[10] }
    json_msg = json.dumps(msg)
    topic = "ASSIGN_CONFIG"
    print(" >  [", topic, "] ", json_msg)

    #save the new configuration
    if myresult[1] == 0:
        sql = "INSERT INTO configuration ( \
            land_id, node_id, status, \
            irr_enabled, irr_limit, irr_duration, \
            mst_timer, ph_timer, light_timer, tmp_timer) \
            VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql, (land_id, node_id, "online", myresult[4], myresult[5], myresult[6], myresult[7], myresult[8], myresult[9], myresult[10]))
        mydb.commit()

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
