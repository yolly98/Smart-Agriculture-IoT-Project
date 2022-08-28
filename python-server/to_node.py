import json
import log
from persistence import get_mysql_db
from persistence import add_mysql_db

#--------------------COMMAND TO NODE--------------

def irr_cmd():
    log.log_info("irr_cmd command selected")
    log.log_info("Type the arguments ...")
    land_id = log.log_input("$ land_id: ")
    node_id = log.log_input("$ node_id: ")
    enable = log.log_input("$ enable: ")
    status = log.log_input("$ status: ")
    limit = log.log_input("$ limit: ")
    irr_duration = log.log_input("$ irr_duration: ")
    
    if not land_id.isdigit():
        log.log_err(f"land_id has to be a number > 0 [{land_id}]")
        return

    if not node_id.isdigit():
        log.log_err(f"node_id has to be a number > 0 [{node_id}]")
        return

    if enable != "true" and enable != "false" and len(enable) != 0:
        log.log_err(f"enable is not valid [{enable}]")
        return
    elif len(enable) == 0:
        enable = "null"

    if status != "on" and status != "off" and len(status) != 0:
        log.log_err(f"status is not valid [{status}]")
        return
    elif len(status) == 0:
        status = "null"

    if (not limit.isdigit()) and len(limit) != 0:
        log.log_err(f"limit has to be a number > 0 [{limit}]")
        return
    elif len(limit) == 0:
        limit = 0

    if (not irr_duration.isdigit()) and len(irr_duration) != 0:
        log.log_err(f"irr_duration has to be a number > 0 [{irr_duration}]")
        return
    elif len(irr_duration) == 0:
        irr_duration = 0

    msg = { 'cmd': 'irr_cmd', 'body': { 'enable': enable, 'status': status, 'limit': int(limit), 'irr_duration': int(irr_duration) } }
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_receive(f"[{topic}] {json_msg}")

#---------

def get_config(broadcast):

    log.log_info("get_config command selected")
    if( not broadcast):
        log.log_info("Type the arguments ...")
        land_id = log.log_input("$ land_id: ")
        node_id = log.log_input("$ node_id: ")
        
        if not land_id.isdigit():
            log.log_err(f"land_id has to be a number > 0 [{land_id}]")
            return

        if not node_id.isdigit():
            log.log_err(f"node_id has to be a number > 0 [{node_id}]")
            return
    else:
        land_id = 0
        node_id = 0
    
    msg = { 'cmd': 'get_config' }
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_receive(f"[{topic}] {json_msg}")

#---------

def assign_config(land_id, node_id, protocol):

    log.log_info("assign_config command")
    config = get_mysql_db.get_config(land_id, node_id, True)

    #if is a new node, send the default configuration
    if not config:
        log.log_info(f"({land_id}, {node_id}) is a new node")
        config = get_mysql_db.get_config(land_id, 0, True)
        if not config:
            log.log_err(f"mysqldb: the land {land_id} doesn't exist or return too many results")
            return

    msg = { 'cmd': 'assign_config', 'body': { 'irr_config': { 'enabled': config[5], 'irr_limit':  config[6], 'irr_duration': config[7]}, 'mst_timer': config[8], 'ph_timer': config[9], 'light_timer': config[10], 'tmp_timer': config[11] } }
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_receive(f"[{topic}] {json_msg}")

    #save the new configuration
    if config[1] == 0:
        add_mysql_db.add_configuration(land_id, node_id, protocol, "online", config[5], config[6], config[7], config[8], config[9], config[10], config[11])
        

#--------

def timer_cmd():

    log.log_info("timer_cmd command selected")
    log.log_info("Type the arguments ...")
    land_id = log.log_input("$ land_id: ")
    node_id = log.log_input("$ node_id: ")
    sensor = log.log_input("$ sensor: ")
    timer = log.log_input("$ timer: ")
    
    if not land_id.isdigit():
        log.log_err(f"land_id has to be a number > 0 [{land_id}]")
        return

    if not node_id.isdigit():
        log.log_err(f"node_id has to be a number > 0 [{node_id}]")
        return

    if sensor != "moisture" and sensor != "ph" and sensor != 'light' and sensor != "tmp":
        log.log_err(f"sensor is not valid [{sensor}]")
        return

    if (not timer.isdigit()) and len(timer) != 0:
        log.log_err(f"timer has to be a number > 0 [{timer}]")
        return
    elif len(timer) == 0:
        timer = 0

    msg = { 'cmd': 'timer_cmd', 'body': { 'sensor': sensor, 'timer': int(timer) } }
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_receive(f"[{topic}] {json_msg}")

#-------

def get_sensor():

    log.log_info("get_sensor command selected")
    log.log_info("Type the arguments ...")
    land_id = log.log_input("$ land_id: ")
    node_id = log.log_input("$ node_id: ")
    sensor = log.log_input("$ sensor: ")
    
    if not land_id.isdigit():
        log.log_err(f"land_id has to be a number > 0 [{land_id}]")
        return

    if not node_id.isdigit():
        log.log_err(f"node_id has to be a number > 0 [{node_id}]")
        return

    if sensor != "moisture" and sensor != "ph" and sensor != 'light' and sensor != 'tmp':
        log.log_err(f"sensor is not valid [{sensor}]")
        return

    msg = { 'cmd': 'get_sensor', 'type': sensor }
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_receive(f"[{topic}] {json_msg}")

#-------

def is_alive(broadcast):

    log.log_info("is_alive command selected")
    if(not broadcast):
        log.log_info("Type the arguments ...")
        land_id = log.log_input("$ land_id: ")
        node_id = log.log_input("$ node_id: ")
        
        if not land_id.isdigit():
            log.log_err(f"land_id has to be a number > 0 [{land_id}]")
            return

        if not node_id.isdigit():
            log.log_err(f"node_id has to be a number > 0 [{node_id}]")
            return
    else:
        land_id = 0
        node_id = 0

    msg = { 'cmd': 'is_alive' }
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_receive(f"[{topic}] {json_msg}")
