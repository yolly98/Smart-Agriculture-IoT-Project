import mysql.connector
import log 

#--------------------ADD------------------------------

def add_configuration(land_id, node_id, protocol, address, status, irr_enabled, irr_limit, irr_duration, mst_timer, ph_timer, light_timer, tmp_timer):

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "INSERT INTO configuration ( \
        land_id, node_id, protocol, address, status, \
        irr_enabled, irr_limit, irr_duration, \
        mst_timer, ph_timer, light_timer, tmp_timer) \
        VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, (land_id, node_id, protocol, address, status, irr_enabled, irr_limit, irr_duration, mst_timer, ph_timer, light_timer, tmp_timer))
    mydb.commit()
   

#---------------------------

def add_land(id, area, locality, name, crop, soil_type, mst_trashold, min_ph, max_ph, min_tmp, max_tmp):
    
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "INSERT INTO land ( \
        id, area, locality, \
        name, crop, soil_type, \
        mst_trashold, min_ph, max_ph, \
        min_tmp, max_tmp) \
        VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, (id, area, locality, name, crop, soil_type, mst_trashold, min_ph, max_ph, min_tmp, max_tmp))
    mydb.commit()

#----------------------------

def add_irrigation_event(land_id, node_id, status):

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "SELECT * FROM irrigation \
        WHERE land_id = %s and node_id = %s \
        and i_timestamp = CURRENT_TIMESTAMP \
        LIMIT 1"
    mycursor.execute(sql, (land_id, node_id))
    last_value = mycursor.fetchone()
    if last_value:
        log.log_err(f"duplicated value from ({land_id}, {node_id}, irrigation)")
        return

    sql = "INSERT INTO irrigation (land_id, node_id, irr_status) \
        VALUES (%s, %s, %s)"
    mycursor.execute(sql, (land_id, node_id, status))
    mydb.commit()

#----------------------------------

def add_measurement_event(land_id, node_id, sensor, value):

    #add the measure to db
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "SELECT * FROM measurement \
        WHERE land_id = %s and node_id = %s \
        and sensor = %s and m_timestamp = CURRENT_TIMESTAMP \
        LIMIT 1"
    mycursor.execute(sql, (land_id, node_id, sensor))
    last_value = mycursor.fetchone()
    if last_value:
        log.log_err(f"duplicated value from ({land_id}, {node_id}, {sensor})")
        return
    
    sql = "INSERT INTO measurement (land_id, node_id, sensor, m_value) \
        VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, (land_id, node_id, sensor, value))
    mydb.commit()

    #check if the measure if out of range
    if sensor == 'light':
        return

    sql = "SELECT * FROM land WHERE id = %s" 
    mycursor.execute(sql, (land_id,))
    land = mycursor.fetchone()

    if not land:
        log.log_err(f"the land {land_id} doesn't exist")
        return

    is_violation = False
    
    if sensor == 'moisture':
        mst_trashold = land[6]
        if int(value) < int(mst_trashold):
            is_violation = True
    elif sensor == 'ph':
        ph_min = land[7]
        ph_max = land[8]
        if int(value) < int(ph_min) or int(value) > int(ph_max):
            is_violation = True
    elif sensor == 'tmp':
        tmp_min = land[9]
        tmp_max = land[10]
        if int(value) < int(tmp_min) or int(value) > int(tmp_max):
            is_violation = True
    else:
        log.log_err(f"Unknown error")
 
    if is_violation:
        log.log_err(f"Violation detected")
        sql = "INSERT INTO violation (land_id, node_id, sensor, v_value) \
            VALUES(%s, %s, %s, %s)"
        mycursor.execute(sql, (land_id, node_id, sensor, value))
        mydb.commit()
