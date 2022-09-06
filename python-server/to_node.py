import json
import log
from persistence import get_mysql_db
from persistence import add_mysql_db
from protocol import mqtt_module

#--------------------COMMAND TO NODE--------------

def irr_cmd():
    log.log_info("irr_cmd command selected")
    land_id = ""
    node_id = ""
    enabled = ""
    status = ""
    limit = ""
    irr_duration = ""
    log.log_info("Type the arguments or 'cancel'")
    while True:
        land_id = log.log_input("land_id: ")
        if land_id == "cancel":
            return
        if land_id.isdigit() and int(land_id) > 0:
            break
        else:
            log.log_err(f"invalid value, has to be > 0")
    while True:
        node_id = log.log_input("node_id: ")
        if node_id == "cancel":
            return
        if node_id.isdigit() and int(node_id) > 0:
            break
        else:
            log.log_err(f"invalid value, has to be > 0")
    while True:
        status = log.log_input("status (on/off/null): ")
        if status == "cancel":
            return
        if status == 'on' or status == 'off' or status == 'null':
            break
        else:
            log.log_err(f"invalid value")
    while True:
        enabled = log.log_input("enabled (true/false/null): ")
        if enabled == "cancel":
            return
        if enabled == 'true' or enabled == 'false' or enabled == 'null':
            break
        else:
            log.log_err(f"invalid value")
    while True:
        limit = log.log_input("limit (0 to not update): ")
        if limit == "cancel":
            return
        if limit.isdigit():
            break
        else:
            log.log_err(f"invalid value, , has to be >= 0")
    while True:
        irr_duration = log.log_input("irr_duration (0 to not update): ")
        if irr_duration == "cancel":
            return
        if irr_duration.isdigit():
            break
        else:
            log.log_err(f"invalid value, has to be > 0")

    msg = { 'cmd': 'irr_cmd', 'body': { 'enable': enabled, 'status': status, 'limit': int(limit), 'irr_duration': int(irr_duration) } }
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_send(f"[{topic}] {json_msg}")
    mqtt_module.mqtt_publish(topic, json_msg)

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
    log.log_send(f"[{topic}] {json_msg}")
    mqtt_module.mqtt_publish(topic, json_msg)

#---------

def assign_config_cmd():

    land_id = ""
    node_id = ""
    protocol = ""
    while True:
        land_id = log.log_input("land_id: ")
        if land_id == "cancel":
            return
        if land_id.isdigit() and int(land_id) > 0:
            break
        else:
            log.log_err(f"invalid value")
    while True:
        node_id = log.log_input("node_id: ")
        if node_id == "cancel":
            return
        if node_id.isdigit() and int(node_id) > 0:
            break
        else:
            log.log_err(f"invalid value")
    while True:
        protocol = log.log_input("protocolo(MQTT/COAP): ")
        if protocol == "cancel":
            return
        if protocol == "MQTT" or protocol == "COAP":
            break
        else:
            log.log_err(f"invalid value")
    assign_config(land_id, node_id, protocol)


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
    log.log_send(f"[{topic}] {json_msg}")
    mqtt_module.mqtt_publish(topic, json_msg)

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

    if (timer.isdigit() and int(timer) <= 0) or ((not timer.isdigit()) and len(timer) != 0):
        log.log_err(f"timer has to be a number > 0 [{timer}]")
        return
    elif len(timer) == 0:
        timer = 0

    msg = { 'cmd': 'timer_cmd', 'body': { 'sensor': sensor, 'timer': int(timer) } }
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_send(f"[{topic}] {json_msg}")
    mqtt_module.mqtt_publish(topic, json_msg)

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
    log.log_send(f"[{topic}] {json_msg}")
    mqtt_module.mqtt_publish(topic, json_msg)

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
    log.log_send(f"[{topic}] {json_msg}")
    mqtt_module.mqtt_publish(topic, json_msg)
