import json
import random
import to_node
import log
from persistence import add_mysql_db
from persistence import update_mysql_db

#--------------

def config_request_sim():

    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    msg = { 'cmd': 'config_rqst', 'body': { 'land_id': land_id, 'node_id': node_id } }
    return json.dumps(msg)

def config_request(protocol):

    cmd = "config_rqst"
    json_msg = config_request_sim()
    msg = json.loads(json_msg)

    log.log_receive(f"[{cmd}] {msg}")

    to_node.assign_config(msg['body']['land_id'], msg['body']['node_id'], protocol)


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
    return json.dumps(msg)

def status(protocol):

    cmd = "status"
    json_msg = status_sim()
    msg = json.loads(json_msg)

    log.log_receive(f"[{cmd}] {msg}")

    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']
    irr_enabled = msg['body']['irr_config']['enabled']
    irr_limit = msg['body']['irr_config']['irr_limit']
    irr_duration = msg['body']['irr_config']['irr_duration']
    mst_timer = msg['body']['mst_timer']
    ph_timer = msg['body']['ph_timer']
    light_timer = msg['body']['light_timer']
    tmp_timer = msg['body']['tmp_timer']

    update_mysql_db.update_configuration(land_id, node_id, protocol, irr_enabled, irr_limit, irr_duration, mst_timer, ph_timer, light_timer, tmp_timer)
    

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
    return json.dumps(msg)

def irrigation():
    
    cmd = "irrigation"
    json_msg = irrigation_sim()
    msg = json.loads(json_msg)

    log.log_receive(f"[{cmd}] {msg}")

    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']
    status = msg['body']['status'] 
    
    add_mysql_db.add_irrigation_event(land_id, node_id, status)

#-----------

def moisture_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    value = random.randint(10,50)
    msg = { 'cmd': 'moisture', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': "moisture", 'value': value } }
    return json.dumps(msg)

def moisture():

    cmd = "moisture"
    json_msg = moisture_sim()
    msg = json.loads(json_msg)
    
    log.log_receive(f"[{cmd}] {msg}")

    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']
    sensor = msg['body']['type']
    value = msg['body']['value'] 

    add_mysql_db.add_measurement_event(land_id, node_id, sensor, value)

#-----------

def ph_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    value = random.randint(5,8)
    msg = { 'cmd': 'ph', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': "ph", 'value': value } }
    return json.dumps(msg)

def ph():

    cmd = "ph"
    json_msg = ph_sim()
    msg = json.loads(json_msg)
    
    log.log_receive(f"[{cmd}] {msg}")
    
    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']
    sensor = msg['body']['type']
    value = msg['body']['value'] 

    add_mysql_db.add_measurement_event(land_id, node_id, sensor, value)

#-----------

def light_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    value = random.randint(0, 1800)
    msg = { 'cmd': 'light', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': "light", 'value': value } }
    return json.dumps(msg)

def light():

    cmd = "light"
    json_msg = light_sim()
    msg = json.loads(json_msg)
    
    log.log_receive(f"[{cmd}] {msg}")
    
    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']
    sensor = msg['body']['type']
    value = msg['body']['value'] 

    add_mysql_db.add_measurement_event(land_id, node_id, sensor, value)

#-----------

def tmp_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    value = random.randint(5, 35)
    msg = { 'cmd': 'tmp', 'body': { 'land_id': land_id, 'node_id': node_id, 'type': "tmp", 'value': value } }
    return json.dumps(msg)

def tmp():

    cmd = "tmp"
    json_msg = tmp_sim()
    msg = json.loads(json_msg)
    
    log.log_receive(f"[{cmd}] {msg}")
    
    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']
    sensor = msg['body']['type']
    value = msg['body']['value'] 

    add_mysql_db.add_measurement_event(land_id, node_id, sensor, value)

#-----------

def is_alive_ack_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    msg = { 'cmd': 'is_alive_ack', 'body': { 'land_id': land_id, 'node_id': node_id } }
    return json.dumps(msg)

def is_alive_ack():

    cmd = "is_alive_ack"
    json_msg = is_alive_ack_sim()
    msg = json.loads(json_msg)
    
    log.log_receive(f"[{cmd}] {msg}")
    
    land_id = msg['body']['land_id']
    node_id = msg['body']['node_id']

    update_mysql_db.set_node_online(land_id, node_id)