import json
import log
from persistence import get_mysql_db
from persistence import add_mysql_db
from persistence import update_mysql_db
from protocol import mqtt_module
from protocol import coap_module

#--------------------COMMAND TO NODE--------------

def irr_cmd():
    log.log_info("irr_cmd process starting ...")
    land_id = ""
    node_id = ""
    enabled = ""
    status = ""
    limit = ""
    irr_duration = ""
    protocol = ""
    log.log_console("Type the arguments or 'cancel'")
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

    if coap_module.check_node(land_id, node_id):
        protocol = "COAP"
    elif mqtt_module.check_node(land_id, node_id):
        protocol = "MQTT"
    else:
        log.log_err(f"node ({land_id}, {node_id}) there isn't in the network")
        return

    msg = ""
    if protocol == "MQTT":
        msg = { 'cmd': 'irr_cmd', 'body': { 'enable': enabled, 'status': status, 'limit': int(limit), 'irr_duration': int(irr_duration) } }
    elif protocol == "COAP":
        msg = { 'enable': enabled, 'status': status, 'limit': int(limit), 'irr_duration': int(irr_duration) }
    
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_send(json_msg, land_id, node_id)
    
    if protocol == "MQTT":
        mqtt_module.mqtt_publish(topic, json_msg)
    elif protocol == "COAP":
        coap_module.send_msg(land_id, node_id, "irrigation", "PUT", json_msg)

    log.log_success("irr_cmd ended")

#---------

def get_config(broadcast):

    log.log_info("get_config process starting ...")
    
    msg = { 'cmd': 'get_config' }
    json_msg = json.dumps(msg)

    if(not broadcast):
        log.log_console("Type the arguments or 'cancel'")
        
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

        #if coap_module.check_node(land_id, node_id):
        #    protocol = "COAP"
        #elif mqtt_module.check_node(land_id, node_id):
        #    protocol = "MQTT"
        #else:
        #    log.log_err(f"node ({land_id}, {node_id}) there isn't in the network")
        #    return

        if coap_module.check_node(land_id, node_id):
            protocol = "COAP"
        else:
            protocol = "MQTT"
        #-----------------

        topic = f"NODE/{land_id}/{node_id}"
        log.log_send(json_msg, land_id, node_id)
        if protocol == "MQTT":
            mqtt_module.mqtt_publish(topic, json_msg)
        elif protocol == "COAP":
            coap_module.coap_reset_config(land_id, node_id)
            result = coap_module.send_msg(land_id, node_id, "configuration", "GET", "")
            if not result:
                return
            coap_module.send_msg(land_id, node_id, "irrigation", "PUT", "status")
            coap_module.send_msg(land_id, node_id, "sensor/mst", "PUT", "status")
            coap_module.send_msg(land_id, node_id, "sensor/ph", "PUT", "status")
            coap_module.send_msg(land_id, node_id, "sensor/light", "PUT", "status")
            coap_module.send_msg(land_id, node_id, "sensor/tmp", "PUT", "status")
        else:
            log.log_info(f"protocol not recognized for node ({land_id}, {node_id}")
            return

    else:
        configs = get_mysql_db.get_config('all', 'all', False)
        if not configs:
            log.log_err("There are no configutations")
            return
        
        for config in configs:
            land_id = config[0]
            node_id = config[1]
            protocol = config[2]
            address = config[3]

            if protocol == "null":
                continue
            topic = f"NODE/{land_id}/{node_id}"
            log.log_send(json_msg, land_id, node_id)
            if protocol == "MQTT":
                if mqtt_module.check_node(land_id, node_id):
                    continue
                mqtt_module.mqtt_publish(topic, json_msg)
            elif protocol == "COAP":
                if coap_module.check_node(land_id, node_id):
                    continue
                if (not coap_module.add_nodes(land_id, node_id, address)) or mqtt_module.check_node(land_id, node_id):
                    log.log_err(f"nodes ({land_id}, {node_id}) duplicated")
                    continue
                result = coap_module.send_msg(land_id, node_id, "configuration", "GET", "")
                if not result:
                    coap_module.delete_node(land_id, node_id)
                    continue
                coap_module.send_msg(land_id, node_id, "irrigation", "PUT", "status")
                coap_module.send_msg(land_id, node_id, "sensor/mst", "PUT", "status")
                coap_module.send_msg(land_id, node_id, "sensor/ph", "PUT", "status")
                coap_module.send_msg(land_id, node_id, "sensor/light", "PUT", "status")
                coap_module.send_msg(land_id, node_id, "sensor/tmp", "PUT", "status")
            else:
                log.log_info(f"protocol not recognized for node ({land_id}, {node_id}")
                continue
        
    log.log_success("get_config ended")
    

#---------

def assign_config_cmd():

    land_id = ""
    node_id = ""
    protocol = ""
    address = ""

    log.log_console("Type the arguments or 'cancel'")
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

    if coap_module.check_node(land_id, node_id):
        protocol = "COAP"
        address = coap_module.get_node_addr(land_id, node_id)
    elif mqtt_module.check_node(land_id, node_id):
        protocol = "MQTT"
        address = ""
    else:
        log.log_err(f"node ({land_id}, {node_id}) there isn't in the network")
        return

    assign_config(land_id, node_id, protocol, address, True)


def assign_config(land_id, node_id, protocol, address, cmd):

    log.log_info("assign_config process starting ...")
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
            add_mysql_db.add_configuration(land_id, node_id, protocol, address, "online", "true", config[7], config[8], config[9], config[10], config[11], config[12])
            msg = { 'cmd': 'assign_config', 'body': { 'irr_config': { 'enabled': 'true', 'irr_limit':  config[7], 'irr_duration': config[8]}, 'mst_timer': config[9], 'ph_timer': config[10], 'light_timer': config[11], 'tmp_timer': config[12] } }
    else:
        if config[2] != protocol or config[3] != address:
            if (protocol == "COAP" and 
                ((not coap_module.add_nodes(land_id, node_id, address)) or mqtt_module.check_node(land_id, node_id))):
                log.log_err(f"nodes ({land_id}, {node_id}) duplicated")
                msg = {'cmd': 'error_id'}
            else:
                update_mysql_db.update_address_in_configuration(land_id, node_id, protocol, address)
                msg = { 'cmd': 'assign_config', 'body': { 'irr_config': { 'enabled': config[6], 'irr_limit':  config[7], 'irr_duration': config[8]}, 'mst_timer': config[9], 'ph_timer': config[10], 'light_timer': config[11], 'tmp_timer': config[12] } }
        else:
            msg = { 'cmd': 'assign_config', 'body': { 'irr_config': { 'enabled': config[6], 'irr_limit':  config[7], 'irr_duration': config[8]}, 'mst_timer': config[9], 'ph_timer': config[10], 'light_timer': config[11], 'tmp_timer': config[12] } }
    
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_send(json_msg, land_id, node_id)
        
    if protocol == "MQTT":
        if msg['cmd'] != 'error_land':
            msg1 = { 'cmd': 'assign_i_config', 'body': {'enabled': msg['body']['irr_config']['enabled'], 'irr_limit':  msg['body']['irr_config']['irr_limit'], 'irr_duration': msg['body']['irr_config']['irr_duration'] } }
            msg2 = { 'cmd': 'assign_t_config', 'body': {'mst_timer': msg['body']['mst_timer'], 'ph_timer':msg['body']['ph_timer'], 'light_timer': msg['body']['light_timer'], 'tmp_timer': msg['body']['tmp_timer'] } }
            mqtt_module.mqtt_publish(topic, json.dumps(msg1))
            mqtt_module.mqtt_publish(topic, json.dumps(msg2))
        else:
            mqtt_module.mqtt_reset_config(land_id, node_id)
            mqtt_module.mqtt_publish(topic, json_msg)
    elif protocol == "COAP":
        if cmd == False:
            if msg['cmd'] == 'error_land':
                json_msg = 'error_land'
            elif msg['cmd'] == 'error_id':
                json_msg = 'error_id'
            return json_msg
        else:
            if msg['cmd'] == 'error_land' or msg['cmd'] == 'error_id':
                return
            coap_module.coap_reset_config(land_id, node_id)
            result = coap_module.send_msg(land_id, node_id, "irrigation", "PUT", json.dumps(msg['body']['irr_config']))
            if not result:
                coap_module.delete_node(land_id, node_id)
                return
            coap_module.send_msg(land_id, node_id, "sensor/mst", "PUT", str(msg['body']['mst_timer']))
            coap_module.send_msg(land_id, node_id, "sensor/ph", "PUT", str(msg['body']['ph_timer']))
            coap_module.send_msg(land_id, node_id, "sensor/light", "PUT", str(msg['body']['light_timer']))
            coap_module.send_msg(land_id, node_id, "sensor/tmp", "PUT", str(msg['body']['tmp_timer']))
    else:
        log.log_info(f"protocol not recognized for node ({land_id}, {node_id}")

    log.log_success("assign_config process ended")
        

#--------

def timer_cmd():

    log.log_info("timer_cmd process starting ...")
    log.log_console("Type the arguments or 'cancel'...")
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
        if sensor == "mst" or sensor == "ph" or sensor == 'light' or sensor == "tmp":
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

    if coap_module.check_node(land_id, node_id):
        protocol = "COAP"
    elif mqtt_module.check_node(land_id, node_id):
        protocol = "MQTT"
    else:
        log.log_err(f"node ({land_id}, {node_id}) there isn't in the network")
        return

    msg = ""
    if protocol == "MQTT":
        msg = { 'cmd': 'timer_cmd', 'body': { 'sensor': sensor, 'timer': int(timer) } }
    elif protocol == "COAP":
        if sensor == "mst":
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
    log.log_send(json_msg, land_id, node_id)

    if protocol == "MQTT":
        mqtt_module.mqtt_publish(topic, json_msg)
    elif protocol == "COAP":
        coap_module.send_msg(land_id, node_id, path, "PUT", timer)

    log.log_success("timer_cmd ended")

#-------

def get_sensor():

    log.log_info("get_sensor process starting ...")
    log.log_console("Type the arguments ...")
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
        if sensor == "mst" or sensor == "ph" or sensor == 'light' or sensor == "tmp":
            break
        else:
            log.log_err(f"invalid value")

    if coap_module.check_node(land_id, node_id):
        protocol = "COAP"
    elif mqtt_module.check_node(land_id, node_id):
        protocol = "MQTT"
    else:
        log.log_err(f"node ({land_id}, {node_id}) there isn't in the network")
        return

    msg = { 'cmd': 'get_sensor', 'type': sensor }
    json_msg = json.dumps(msg)
    topic = f"NODE/{land_id}/{node_id}"
    log.log_send(json_msg, land_id, node_id)

    if protocol == "MQTT":
        mqtt_module.mqtt_publish(topic, json_msg)
    elif protocol == "COAP":
        path = ""
        if sensor == "mst":
            path = "sensor/mst"
        elif sensor == "ph":
            path = "sensor/ph"
        elif sensor == "light":
            path = "sensor/light"
        elif sensor == "tmp":
            path = "sensor/tmp"
        coap_module.send_msg(land_id, node_id, path, "GET", "")
    else:
        log.log_info(f"protocol not recognized for node ({land_id}, {node_id}")
        return

    log.log_success("get_sensor ended")

#-------

def is_alive(broadcast):

    log.log_info("is_alive process starting ...")
    msg = { 'cmd': 'is_alive' }
    json_msg = json.dumps(msg)

    if(not broadcast):
        log.log_console("Type the arguments or 'cancel'...")
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

        #if coap_module.check_node(land_id, node_id):
        #    protocol = "COAP"
        #elif mqtt_module.check_node(land_id, node_id):
        #    protocol = "MQTT"
        #else:
        #    log.log_err(f"node ({land_id}, {node_id}) there isn't in the network")
        #    return

        if coap_module.check_node(land_id, node_id):
            protocol = "COAP"
        else:
            protocol = "MQTT"

        topic = f"NODE/{land_id}/{node_id}"
        log.log_send(json_msg, land_id, node_id)
        if protocol == "MQTT":
            mqtt_module.mqtt_publish(topic, json_msg)
        elif protocol == "COAP":
            coap_module.send_msg(land_id, node_id, "is_alive", "GET", "")
        else:
            log.log_info(f"protocol not recognized for node ({land_id}, {node_id}")
            return
    else:
        update_mysql_db.set_all_node_offline()
        mqtt_module.set_all_node_offline()
        coap_module.set_all_node_offline()
        
        #configs = get_mysql_db.get_config('all', 'all', False)
        #if not configs:
        #    log.log_info("There are no configutations")
        #    return
        
        list_of_nodes = coap_module.get_nodes() + mqtt_module.get_nodes()

        #for config in configs:
        #    land_id = config[0]
        #    node_id = config[1]
        #    protocol = config[2]
        #    address = config[3]

        for node in list_of_nodes:
            land_id = node['land_id']
            node_id = node['node_id']
            protocol = node['protocol']
            address = node['addr']

            if node_id == 0:
                continue
            topic = f"NODE/{land_id}/{node_id}"
            log.log_send(json_msg, land_id, node_id)
            
            if protocol == "MQTT":
                mqtt_module.mqtt_publish(topic, json_msg)
                mqtt_module.delete_node(land_id, node_id)
            elif protocol == "COAP":
                if (not coap_module.add_nodes(land_id, node_id, address)) or mqtt_module.check_node(land_id, node_id):
                    log.log_err(f"nodes ({land_id}, {node_id}) duplicated")
                    continue
                result = coap_module.send_msg(land_id, node_id, "is_alive", "GET", "")
                if not result:
                    coap_module.delete_node(land_id, node_id)
            else:
                log.log_info(f"protocol not recognized for node ({land_id}, {node_id}")
                continue

    log.log_success("is_alive ended")

