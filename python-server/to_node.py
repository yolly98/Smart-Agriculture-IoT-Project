import json
import log
from persistence import get_mysql_db
from persistence import add_mysql_db
from protocol import mqtt_module
from protocol import coap_module

#--------------------COMMAND TO NODE--------------

def irr_cmd():
    log.log_info("irr_cmd command selected")
    land_id = ""
    node_id = ""
    enabled = ""
    status = ""
    limit = ""
    irr_duration = ""
    protocol = ""
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
    while True:
        protocol = log.log_input("protocolo(MQTT/COAP): ")
        if protocol == "cancel":
            return
        if protocol == "MQTT" or protocol == "COAP":
            break
        else:
            log.log_err(f"invalid value")

    msg = ""
    if protocol == "MQTT":
        msg = { 'cmd': 'irr_cmd', 'body': { 'enable': enabled, 'status': status, 'limit': int(limit), 'irr_duration': int(irr_duration) } }
    elif protocol == "COAP":
        msg = { 'enable': enabled, 'status': status, 'limit': int(limit), 'irr_duration': int(irr_duration) }
    
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_send(f"[{topic}] {json_msg}")
    
    if protocol == "MQTT":
        mqtt_module.mqtt_publish(topic, json_msg)
    elif protocol == "COAP":
        coap_module.send_msg(land_id, node_id, "irrigation", "PUT", json_msg)


#---------

def get_config(broadcast):

    log.log_info("get_config command selected")
    
    msg = { 'cmd': 'get_config' }
    json_msg = json.dumps(msg)

    if( not broadcast):
        log.log_info("Type the arguments or 'cancel'")
        
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
            protocol = log.log_input("protocolo(MQTT/COAP): ")
            if protocol == "cancel":
                return
            if protocol == "MQTT" or protocol == "COAP":
                break
            else:
                log.log_err(f"invalid value")

        topic = f"NODE/{land_id}/{node_id}"
        log.log_send(f"[{topic}] {json_msg}")
        if protocol == "MQTT":
            mqtt_module.mqtt_publish(topic, json_msg)
        elif protocol == "COAP":
            coap_module.send_msg(land_id, node_id, "configuration", "GET", "status")
            coap_module.send_msg(land_id, node_id, "irrigation", "GET", "status")
            coap_module.send_msg(land_id, node_id, "sensor/mst", "GET", "status")
            coap_module.send_msg(land_id, node_id, "sensor/ph", "GET", "status")
            coap_module.send_msg(land_id, node_id, "sensor/light", "GET", "status")
            coap_module.send_msg(land_id, node_id, "sensor/tmp", "GET", "status")
        else:
            log.log_err("protocol not recognized")
            return

    else:
        configs = get_mysql_db.get_config('all', 'all', False)
        if not configs:
            log.log_info("There are no configutations")
            return
        
        for config in configs:
            land_id = config[0]
            node_id = config[1]
            protocol = config[2]
            address = config[3]

            if node_id == 0:
                continue
            topic = f"NODE/{land_id}/{node_id}"
            log.log_send(f"[{topic}] {json_msg}")
            if protocol == "MQTT":
                mqtt_module.mqtt_publish(topic, json_msg)
            elif protocol == "COAP":
                coap_module.add_nodes(land_id, node_id, address)
                coap_module.send_msg(land_id, node_id, "configuration", "GET", "status")
                coap_module.send_msg(land_id, node_id, "irrigation", "GET", "status")
                coap_module.send_msg(land_id, node_id, "sensor/mst", "GET", "status")
                coap_module.send_msg(land_id, node_id, "sensor/ph", "GET", "status")
                coap_module.send_msg(land_id, node_id, "sensor/light", "GET", "status")
                coap_module.send_msg(land_id, node_id, "sensor/tmp", "GET", "status")
            else:
                log.log_err("protocol not recognized")
                return
        
    

#---------

def assign_config_cmd():

    land_id = ""
    node_id = ""
    protocol = ""
    address = ""
    log.log_info("Type the arguments or 'cancel'")
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
    while True:
        address = log.log_input("address(fd00::20?:?:?:?): ")
        if address == "cancel":
            return
        if not address.isdigit():
            break
        else:
            log.log_err(f"invalid value")
    assign_config(land_id, node_id, protocol, address)


def assign_config(land_id, node_id, protocol, address):

    log.log_info("assign_config command")
    config = get_mysql_db.get_config(land_id, node_id, True)
    msg = {}
    
    #if is a new node, send the default configuration
    if not config:
        log.log_info(f"({land_id}, {node_id}) is a new node")
        config = get_mysql_db.get_config(land_id, 0, True)
        if not config:
            log.log_err(f"mysqldb: the land {land_id} doesn't exist or return too many results")
            msg = { 'cmd': 'error_land'}
        else:
            #save the new config
            add_mysql_db.add_configuration(land_id, node_id, protocol, address, "online", config[6], config[7], config[8], config[9], config[10], config[11], config[12])
            msg = { 'cmd': 'assign_config', 'body': { 'irr_config': { 'enabled': config[6], 'irr_limit':  config[7], 'irr_duration': config[8]}, 'mst_timer': config[9], 'ph_timer': config[10], 'light_timer': config[11], 'tmp_timer': config[12] } }
    else:
        if config[3] != address:
            update_mysql_db.update_configuration(land_id, node_id, protocol, address, config[6], config[7], config[8], config[9], config[10], config[11], config[12])
        msg = { 'cmd': 'assign_config', 'body': { 'irr_config': { 'enabled': config[6], 'irr_limit':  config[7], 'irr_duration': config[8]}, 'mst_timer': config[9], 'ph_timer': config[10], 'light_timer': config[11], 'tmp_timer': config[12] } }
    
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_send(f"[{topic}] {json_msg}")
    
    if protocol == "MQTT":
        mqtt_module.mqtt_publish(topic, json_msg)
    elif protocol == "COAP":
        return json_msg
    else:
        log.log_err("protocol not recognized")
        

#--------

def timer_cmd():

    log.log_info("timer_cmd command selected")
    log.log_info("Type the arguments or 'cancel'...")
    land_id = ""
    node_id = ""
    sensor = ""
    timer = ""
    path = ""
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
        sensor = log.log_input("sensor (mst/ph/light/tmp): ")
        if sensor == "cancel":
            return
        if sensor == "moisture" or sensor == "ph" or sensor == 'light' or sensor == "tmp":
            break
        else:
            log.log_err(f"invalid value")

    while True:
        timer = log.log_input("timer: ")
        if timer == "cancel":
            return
        if (timer.isdigit() and int(timer) > 0) or len(timer) == 0:
            break
        else:
            log.log_err(f"invalid value")

    if len(timer) == 0:
        timer = 0

    while True:
        protocol = log.log_input("protocolo(MQTT/COAP): ")
        if protocol == "cancel":
            return
        if protocol == "MQTT" or protocol == "COAP":
            break
        else:
            log.log_err(f"invalid value")

    msg = ""
    if protocol == "MQTT":
        msg = { 'cmd': 'timer_cmd', 'body': { 'sensor': sensor, 'timer': int(timer) } }
    elif protocol == "COAP":
        if sensor == "moisture":
            path = "sensor/mst"
        elif sensor == "ph":
            path = "sensor/ph"
        elif sensor == "light":
            path = "sensor/light"
        elif sensor == "tmp":
            path = "sensor/tmp"
        msg = { 'timer': int(timer)}

    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_send(f"[{topic}] {json_msg}")

    if protocol == "MQTT":
        mqtt_module.mqtt_publish(topic, json_msg)
    elif protocol == "COAP":
        coap_module.send_msg(land_id, node_id, path, "PUT", json_msg)

#-------

def get_sensor():

    log.log_info("get_sensor command selected")
    log.log_info("Type the arguments ...")
    land_id = ""
    node_id = ""
    sensor = ""
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
        sensor = log.log_input("sensor (mst/ph/light/tmp): ")
        if sensor == "cancel":
            return
        if sensor == "moisture" or sensor == "ph" or sensor == 'light' or sensor == "tmp":
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

    msg = { 'cmd': 'get_sensor', 'type': sensor }
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_send(f"[{topic}] {json_msg}")

    if protocol == "MQTT":
        mqtt_module.mqtt_publish(topic, json_msg)
    elif protocol == "COAP":
        path = ""
        if sensor == "moisture":
            path = "sensor/mst"
        elif sensor == "ph":
            path = "sensor/ph"
        elif sensor == "light":
            path = "sensor/light"
        elif sensor == "tmp":
            path = "sensor/tmp"
        coap_module.send_msg(land_id, node_id, path, "GET", "")
    else:
        log.log_err("protocol not recognized")
        return

#-------

def is_alive(broadcast, protocol):

    log.log_info("is_alive command selected")
    msg = { 'cmd': 'is_alive' }
    json_msg = json.dumps(msg)

    if(not broadcast):
        log.log_info("Type the arguments or 'cancel'...")
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
            protocol = log.log_input("protocolo(MQTT/COAP): ")
            if protocol == "cancel":
                return
            if protocol == "MQTT" or protocol == "COAP":
                break
            else:
                log.log_err(f"invalid value")

        topic = f"NODE/{land_id}/{node_id}"
        log.log_send(f"[{topic}] {json_msg}")
        if protocol == "MQTT":
            mqtt_module.mqtt_publish(topic, json_msg)
        elif protocol == "COAP":
            coap_module.send_msg(land_id, node_id, "is_alive", "GET", "")
        else:
            log.log_err("protocol not recognized")
            return
    else:
        configs = get_mysql_db.get_config('all', 'all', False)
        if not configs:
            log.log_info("There are no configutations")
            return
        
        for config in configs:
            land_id = config[0]
            node_id = config[1]
            if node_id == 0:
                continue
            topic = f"NODE/{land_id}/{node_id}"
            log.log_send(f"[{topic}] {json_msg}")
            if protocol == "MQTT":
                mqtt_module.mqtt_publish(topic, json_msg)
            elif protocol == "COAP":
                coap_module.send_msg(land_id, node_id, "is_alive", "GET", "")
            else:
                log.log_err("protocol not recognized")
                return

