import json
import random
import to_node
import log
from protocol import mqtt_module
from protocol import coap_module
from persistence import add_mysql_db
from persistence import update_mysql_db

#--------------

def config_request_sim():

    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    msg = { 'cmd': 'config_rqst', 'body': { 'land_id': land_id, 'node_id': node_id } }
    return msg

def config_request(protocol, address, doc):

    msg = doc
    if msg == "":
        msg = config_request_sim()

    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']

    if (protocol == "MQTT" and 
        (mqtt_module.check_node(land_id, node_id) or coap_module.check_node(land_id, node_id))
        ):

            topic = f"NODE/{land_id}/{node_id}"
            log.log_err(f"node ({land_id}, {node_id}) duplicated")
            msg = {'cmd': 'error_id'}
            mqtt_module.mqtt_publish(topic, json.dumps(msg))
            return
    else:
        if protocol == "MQTT":
            mqtt_module.add_node(land_id, node_id)
        to_node.assign_config(land_id, node_id, protocol, address, False)


#------------

def status_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    enable = ""
    if random.randint(1,2) == 1:
        enable = "true"
    else:
        enable = "false"
    irr_limit = random.randint(20,50)
    irr_duration = random.randint(5,20)
    mst_timer = random.randint(6,24) * 60
    ph_timer = random.randint(24,72) * 60
    light_timer = random.randint(1,4)*60
    tmp_timer = random.randint(1,4)*60
    msg = { 'cmd': 'status', 'body': { 'land_id': land_id, 'node_id': node_id, 'irr_config': { 'enabled': enable, 'irr_limit': irr_limit, 'irr_duration': irr_duration}, 'mst_timer': mst_timer, 'ph_timer': ph_timer, 'light_timer': light_timer, 'tmp_timer': tmp_timer } }
    return msg

def status(protocol, address, doc):

    msg = doc
    if msg == "":
        msg = status_sim()

    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']
    irr_enabled = msg['body']['irr_config']['enabled']
    irr_limit = msg['body']['irr_config']['irr_limit']
    irr_duration = msg['body']['irr_config']['irr_duration']
    mst_timer = msg['body']['mst_timer']
    ph_timer = msg['body']['ph_timer']
    light_timer = msg['body']['light_timer']
    tmp_timer = msg['body']['tmp_timer']

    if protocol == "MQTT":
        mqtt_module.add_node(land_id, node_id)
    update_mysql_db.update_configuration(land_id, node_id, protocol, address, irr_enabled, irr_limit, irr_duration, mst_timer, ph_timer, light_timer, tmp_timer)
    

#------------

def irrigation_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    status = ""
    if random.randint(1,2) == 1:
        status = "on"
    else:
        status = "off"
    msg = { 'cmd': 'irrigation', 'body': { 'land_id': land_id, 'node_id': node_id, "status": status } }
    return msg

def irrigation(doc):

    msg = doc
    if msg == "":
        msg = irrigation_sim()

    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']
    status = msg['body']['status'] 
    
    add_mysql_db.add_irrigation_event(land_id, node_id, status)

#-----------

def moisture_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    value = random.randint(10,50)
    msg = { 'cmd': 'moisture', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': 'moisture', 'value': value } }
    return msg

def moisture(doc):

    msg = doc
    if msg == "":
        msg = moisture_sim()

    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']
    sensor = "moisture"
    value = msg['body']['value'] 

    add_mysql_db.add_measurement_event(land_id, node_id, sensor, value)

#-----------

def ph_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    value = random.randint(5,8)
    msg = { 'cmd': 'ph', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': "ph", 'value': value } }
    return msg

def ph(doc):

    msg = doc
    if msg == "":
        msg = ph_sim()
    
    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']
    sensor = "ph"
    value = msg['body']['value'] 

    add_mysql_db.add_measurement_event(land_id, node_id, sensor, value)

#-----------

def light_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    value = random.randint(0, 1800)
    msg = { 'cmd': 'light', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': "light", 'value': value } }
    return msg

def light(doc):

    msg = doc
    if msg == "":
        msg = light_sim()
    
    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']
    sensor = "light"
    value = msg['body']['value'] 

    add_mysql_db.add_measurement_event(land_id, node_id, sensor, value)

#-----------

def tmp_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    value = random.randint(5, 35)
    msg = { 'cmd': 'tmp', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': "tmp", 'value': value } }
    return msg

def tmp(doc):

    msg = doc
    if msg == "":
        msg = tmp_sim()
    
    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']
    sensor = "tmp"
    value = msg['body']['value'] 

    add_mysql_db.add_measurement_event(land_id, node_id, sensor, value)

#-----------

def is_alive_ack_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    msg = { 'cmd': 'is_alive_ack', 'body': { 'land_id': land_id, 'node_id': node_id } }
    return msg

def is_alive_ack(doc, protocol):

    msg = doc
    if msg == "":
        protocol = "MQTT" if random.randint(0,1) == 0 else "COAP"
        msg = is_alive_ack_sim()
    
    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']

    if protocol == "MQTT":
        mqtt_module.add_node(land_id, node_id)
    update_mysql_db.set_node_online(land_id, node_id)