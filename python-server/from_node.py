import json
import command
import random
import mysql.connector

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
    irr_enabled = msg['irr_config']['irr_enabled']
    irr_limit = msg['irr_config']['irr_limit']
    irr_duration = msg['irr_config']['irr_duration']
    mst_timer = msg['mst_timer']
    ph_timer = msg['ph_timer']
    light_timer = msg['light_timer']
    tmp_timer = msg['tmp_timer']


    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "UPDATE configuration \
        SET status = 'online', irr_enabled = %s, \
        irr_limit = %s, irr_duration = %s, \
        mst_timer = %s, ph_timer = %s, \
        light_timer = %s, tmp_timer = %s \
        WHERE land_id = %s AND node_id = %s "
    mycursor.execute(sql, (irr_enabled, irr_limit, irr_duration, mst_timer, ph_timer, light_timer, tmp_timer, land_id, node_id))
    mydb.commit()

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
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "INSERT INTO irrigation (land_id, node_id, irr_status) \
        VALUES (%s, %s, %s)"
    mycursor.execute(sql, (land_id, node_id, status))
    mydb.commit()

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

    #save the measuremt
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "INSERT INTO measurement (land_id, node_id, sensor, m_value) \
        VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, (land_id, node_id, sensor, value))
    mydb.commit()

    #check if the measure is out of range
    sql = "SELECT * FROM land WHERE id = %s" 
    mycursor.execute(sql, (land_id,))
    myresult = mycursor.fetchone()

    mst_trashold = myresult[6]
    if value < mst_trashold:
        sql = "INSERT INTO violation (land_id, node_id, sensor, v_value) \
            VALUES(%s, %s, %s, %s)"
        mycursor.execute(sql, (land_id, node_id, sensor, value))
        mydb.commit()

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

    #save the measuremt
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "INSERT INTO measurement (land_id, node_id, sensor, m_value) \
        VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, (land_id, node_id, sensor, value))
    mydb.commit()

    #check if the measure is out of range
    sql = "SELECT * FROM land WHERE id = %s" 
    mycursor.execute(sql, (land_id,))
    myresult = mycursor.fetchone()

    ph_min = myresult[7]
    ph_max = myresult[8]
    if value < ph_min or value > ph_max:
        sql = "INSERT INTO violation (land_id, node_id, sensor, v_value) \
            VALUES(%s, %s, %s, %s)"
        mycursor.execute(sql, (land_id, node_id, sensor, value))
        mydb.commit()

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

    #save the measuremt
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "INSERT INTO measurement (land_id, node_id, sensor, m_value) \
        VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, (land_id, node_id, sensor, value))
    mydb.commit()

    #check if the measure is out of range
    sql = "SELECT * FROM land WHERE id = %s" 
    mycursor.execute(sql, (land_id,))
    myresult = mycursor.fetchone()

    light_min = myresult[9]
    light_max = myresult[10]
    if value < light_min or value > light_max:
        sql = "INSERT INTO violation (land_id, node_id, sensor, v_value) \
            VALUES(%s, %s, %s, %s)"
        mycursor.execute(sql, (land_id, node_id, sensor, value))
        mydb.commit()

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

    #save the measuremt
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "INSERT INTO measurement (land_id, node_id, sensor, m_value) \
        VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, (land_id, node_id, sensor, value))
    mydb.commit()

    #check if the measure is out of range
    sql = "SELECT * FROM land WHERE id = %s" 
    mycursor.execute(sql, (land_id,))
    myresult = mycursor.fetchone()

    tmp_min = myresult[11]
    tmp_max = myresult[12]
    if value < tmp_min or value > tmp_max:
        sql = "INSERT INTO violation (land_id, node_id, sensor, v_value) \
            VALUES(%s, %s, %s, %s)"
        mycursor.execute(sql, (land_id, node_id, sensor, value))
        mydb.commit()

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

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "UPDATE configuration \
        SET status = 'online' \
        WHERE land_id = %s AND node_id = %s "
    mycursor.execute(sql, (land_id, node_id))
    mydb.commit()