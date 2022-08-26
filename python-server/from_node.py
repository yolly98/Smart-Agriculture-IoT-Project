import json
import command
import random
import mysql_module

#--------------

def config_request_sim():

    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    msg = { 'land_id': land_id, 'node_id': node_id}
    return json.dumps(msg)

def config_request():

    topic = "CONFIG_RQST"
    json_msg = config_request_sim()
    msg = json.loads(json_msg)

    print(" <  [", topic, "] ", msg)

    command.assign_config(msg['land_id'], msg['node_id'])


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
    msg = { 'land_id': land_id, 'node_id': node_id, 'irr_config': { 'enabled': enable, 'irr_limit': irr_limit, 'irr_duration': irr_duration}, 'mst_timer': mst_timer, 'ph_timer': ph_timer, 'light_timer': light_timer, 'tmp_timer': tmp_timer }
    return json.dumps(msg)

def status():

    topic = "STATUS"
    json_msg = status_sim()
    msg = json.loads(json_msg)

    print(" <  [", topic, "] ", msg)

    land_id = msg['land_id']
    node_id = msg['node_id']
    irr_enabled = msg['irr_config']['enabled']
    irr_limit = msg['irr_config']['irr_limit']
    irr_duration = msg['irr_config']['irr_duration']
    mst_timer = msg['mst_timer']
    ph_timer = msg['ph_timer']
    light_timer = msg['light_timer']
    tmp_timer = msg['tmp_timer']

    mysql_module.update_configuration(land_id, node_id, irr_enabled, irr_limit, irr_duration, mst_timer, ph_timer, light_timer, tmp_timer)
    

#------------

def irrigation_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    status = ""
    if random.randint(1,2) == 1:
        enable = "on"
    else:
        enable = "off"
    msg = { 'land_id': land_id, 'node_id': node_id, "status": status}
    return json.dumps(msg)

def irrigation():
    
    topic = "IRRIGATION"
    json_msg = irrigation_sim()
    msg = json.loads(json_msg)

    print(" < [", topic, "] ", msg)

    land_id = msg['land_id']
    node_id = msg['node_id']
    status = msg['status'] 
    
    mysql_module.add_irrigation_event(land_id, node_id, status)

#-----------

def moisture_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    value = random.randint(10,50)
    msg = { 'land_id': land_id, 'node_id': node_id, 'type': "moisture", 'value': value }
    return json.dumps(msg)

def moisture():

    topic = "MOISTURE"
    json_msg = moisture_sim()
    msg = json.loads(json_msg)
    
    print(" < [", topic, "] ", msg)

    land_id = msg['land_id']
    node_id = msg['node_id']
    sensor = msg['type']
    value = msg['value'] 

    mysql_module.add_measurement_event(land_id, node_id, sensor, value)

#-----------

def ph_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    value = random.randint(5,8)
    msg = { 'land_id': land_id, 'node_id': node_id, 'type': "ph", 'value': value }
    return json.dumps(msg)

def ph():

    topic = "PH"
    json_msg = ph_sim()
    msg = json.loads(json_msg)
    
    print(" < [", topic, "] ", msg)
    
    land_id = msg['land_id']
    node_id = msg['node_id']
    sensor = msg['type']
    value = msg['value'] 

    mysql_module.add_measurement_event(land_id, node_id, sensor, value)

#-----------

def light_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    value = random.randint(0, 1800)
    msg = { 'land_id': land_id, 'node_id': node_id, 'type': "light", 'value': value }
    return json.dumps(msg)

def light():

    topic = "LIGHT"
    json_msg = light_sim()
    msg = json.loads(json_msg)
    
    print(" < [", topic, "] ", msg)
    
    land_id = msg['land_id']
    node_id = msg['node_id']
    sensor = msg['type']
    value = msg['value'] 

    mysql_module.add_measurement_event(land_id, node_id, sensor, value)

#-----------

def tmp_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    value = random.randint(5, 35)
    msg = { 'land_id': land_id, 'node_id': node_id, 'type': "tmp", 'value': value }
    return json.dumps(msg)

def tmp():

    topic = "TMP"
    json_msg = tmp_sim()
    msg = json.loads(json_msg)
    
    print(" < [", topic, "] ", msg)
    
    land_id = msg['land_id']
    node_id = msg['node_id']
    sensor = msg['type']
    value = msg['value'] 

    mysql_module.add_measurement_event(land_id, node_id, sensor, value)

#-----------

def is_alive_ack_sim():
    land_id = random.randint(1,10)
    node_id = random.randint(1,10)
    msg = { 'land_id': land_id, 'node_id': node_id }
    return json.dumps(msg)

def is_alive_ack():

    topic = "IS_ALIVE_ACK"
    json_msg = is_alive_ack_sim()
    msg = json.loads(json_msg)
    
    print(" < [", topic, "] ", msg)
    
    land_id = msg['land_id']
    node_id = msg['node_id']

    mysql_module.set_node_online(land_id, node_id)