import mysql.connector

#----------------------GET--------------------

def get_land(land_id, fetchone):
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)
    sql = "SELECT * FROM land WHERE (id = %s OR %s = 'all' OR %s = 0)" 
    mycursor.execute(sql, (land_id, land_id, land_id))
    if fetchone:
        myresult = mycursor.fetchone()
    else:
        myresult = mycursor.fetchall()

    return myresult

#----------------------

def get_config(land_id, node_id, fetchone):

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "SELECT * FROM configuration WHERE (land_id = %s OR %s = 'all') AND (node_id = %s OR %s = 'all')"
    mycursor.execute(sql, (land_id, land_id, node_id, node_id))
    if fetchone:
        myresult = mycursor.fetchone()
    else:
        myresult = mycursor.fetchall()

    return myresult

#-------------------------

def get_measurement(land_id, node_id, sensor, older_time, recent_time):

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    if int(older_time) != 0 and int(recent_time) != 0:
        sql = "SELECT * FROM measurement WHERE (land_id = %s OR %s = 'all') AND (node_id = %s OR %s = 'all') AND (sensor = %s OR %s = 'all') AND (m_timestamp BEETWEEN date_sub(now(), interval %s day) and date_sub(now(), interval %s day))"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor, older_time, recent_time))
    else:
        sql = "SELECT * FROM measurement WHERE (land_id = %s OR %s = 'all') AND (node_id = %s OR %s = 'all') AND (sensor = %s OR %s = 'all') "
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor))

    myresult = mycursor.fetchall()

    return myresult

#-------------------------

def get_violation(land_id, node_id, sensor, older_time, recent_time):

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    if int(older_time) != 0 and int(recent_time) != 0:
        sql = "SELECT * FROM violation WHERE (land_id = %s OR %s = 'all') AND (node_id = %s OR %s = 'all') AND (sensor = %s OR %s = 'all') AND (v_timestamp BEETWEEN date_sub(now(), interval %s day) and date_sub(now(), interval %s day))"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor, older_time, recent_time))
    else:
        sql = "SELECT * FROM violation WHERE (land_id = %s OR %s = 'all') AND (node_id = %s OR %s = 'all') AND (sensor = %s OR %s = 'all') "
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor))

    myresult = mycursor.fetchall()

    return myresult

#---------------------

def get_irrigation(land_id, node_id, older_time, recent_time):

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    if int(older_time) != 0 and int(recent_time) != 0:
        sql = "SELECT * FROM irrigation WHERE (land_id = %s OR %s = 'all') AND (node_id = %s OR %s = 'all') AND (i_timestamp BEETWEEN date_sub(now(), interval %s day) and date_sub(now(), interval %s day))"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, older_time, recent_time))
    else:
        sql = "SELECT * FROM irrigation WHERE (land_id = %s OR %s = 'all') AND (node_id = %s OR %s = 'all')"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id))

    myresult = mycursor.fetchall()

    return myresult


#--------------------ADD------------------------------

def add_configuration(land_id, node_id, status, irr_enabled, irr_limit, irr_duration, mst_timer, ph_timer, light_timer, tmp_timer):

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "INSERT INTO configuration ( \
        land_id, node_id, status, \
        irr_enabled, irr_limit, irr_duration, \
        mst_timer, ph_timer, light_timer, tmp_timer) \
        VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, (land_id, node_id, status, irr_enabled, irr_limit, irr_duration, mst_timer, ph_timer, light_timer, tmp_timer))
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

    sql = "INSERT INTO measurement (land_id, node_id, sensor, m_value) \
        VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, (land_id, node_id, sensor, value))
    mydb.commit()

    #check if the measure if out of range
    sql = "SELECT * FROM land WHERE id = %s" 
    mycursor.execute(sql, (land_id,))
    myresult = mycursor.fetchone()

    is_violation = False
    
    if sensor == 'moisture':
        mst_trashold = myresult[6]
        if value < mst_trashold:
            is_violation = True
    elif sensor == 'ph':
        ph_min = myresult[7]
        ph_max = myresult[8]
        if value < ph_min or value > ph_max:
            is_violation = True
    elif sensor == 'light':
        light_min = myresult[9]
        light_max = myresult[10]
        if value < light_min or value > light_max:
            is_violation = True
    elif sensor == 'tmp':
        tmp_min = myresult[11]
        tmp_max = myresult[12]
        if value < tmp_min or value > tmp_max:
            is_violation = True
 
    if is_violation:
        sql = "INSERT INTO violation (land_id, node_id, sensor, v_value) \
            VALUES(%s, %s, %s, %s)"
        mycursor.execute(sql, (land_id, node_id, sensor, value))
        mydb.commit()

#-----------------------UPDATE-------------------------

def update_configuration(land_id, node_id, irr_enabled, irr_limit, irr_duration, mst_timer, ph_timer, light_timer, tmp_timer):

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

#-----------------------------


def set_node_online(land_id, node_id):

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

#---------------------------

def set_all_node_offline():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "UPDATE configuration SET status = 'offline' WHERE node_id <> 0"
    mycursor.execute(sql)
    mydb.commit()

#------------------------------




    