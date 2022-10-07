import mysql.connector
import log 
#----------------------GET--------------------

def get_land(land_id, fetchone):
    mydb = ""
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "password",
            database = "iot_project_db"
        )
    except mysql.connector.Error as e:
        log.log_err("failed connection to mysql db")
        return
    mycursor = mydb.cursor(prepared=True)
    sql = "SELECT * FROM land WHERE (%s = 'all' OR id = %s OR %s = 0) ORDER BY id" 
    mycursor.execute(sql, (land_id, land_id, land_id))
    if fetchone:
        myresult = mycursor.fetchone()
    else:
        myresult = mycursor.fetchall()

    return myresult

#----------------------

def get_config(land_id, node_id, fetchone):

    mydb = ""
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "password",
            database = "iot_project_db"
        )
    except mysql.connector.Error as e:
        log.log_err("failed connection to mysql db")
        return
    mycursor = mydb.cursor(prepared=True)

    sql = "SELECT * FROM configuration WHERE (%s = 'all' OR land_id = %s) AND (%s = 'all' OR node_id = %s) ORDER BY land_id, node_id"
    mycursor.execute(sql, (land_id, land_id, node_id, node_id))
    if fetchone:
        myresult = mycursor.fetchone()
    else:
        myresult = mycursor.fetchall()

    return myresult

#-------------------------

def get_measurement(land_id, node_id, sensor, older_time, recent_time, limit):

    mydb = ""
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "password",
            database = "iot_project_db"
        )
    except mysql.connector.Error as e:
        log.log_err("failed connection to mysql db")
        return
    mycursor = mydb.cursor(prepared=True)

    if int(older_time) != 0 and int(recent_time) != 0:
        sql = "SELECT * FROM measurement WHERE \
            (%s = 'all' OR land_id = %s) \
            AND (%s = 'all' OR node_id = %s) \
            AND (sensor = %s OR %s = 'all') \
            AND (m_timestamp > date_sub(now(), interval %s day) and m_timestamp < date_sub(now(), interval %s day)) \
            ORDER BY m_timestamp DESC LIMIT %s"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor, older_time, recent_time, limit))
    else:
        sql = "SELECT * FROM measurement \
            WHERE (%s = 'all' OR land_id = %s) \
            AND (%s = 'all' OR node_id = %s) \
            AND (sensor = %s OR %s = 'all') \
            ORDER BY m_timestamp DESC LIMIT %s"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor, limit))

    myresult = mycursor.fetchall()

    return myresult

#---------------------

def get_measurement_one(land_id, node_id, timestamp):

    mydb = ""
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "password",
            database = "iot_project_db"
        )
    except mysql.connector.Error as e:
        log.log_err("failed connection to mysql db")
        return
    mycursor = mydb.cursor(prepared=True)

    sql = "SELECT * FROM measurement \
        WHERE land_id = %s \
        AND node_id = %s \
        AND m_timestamp = %s "
    mycursor.execute(sql, (land_id, node_id, timestamp))

    myresult = mycursor.fetchone()

    return myresult

#-------------------------

def get_violation(land_id, node_id, sensor, older_time, recent_time, limit):

    mydb = ""
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "password",
            database = "iot_project_db"
        )
    except mysql.connector.Error as e:
        log.log_err("failed connection to mysql db")
        return
    mycursor = mydb.cursor(prepared=True)

    if int(older_time) != 0 and int(recent_time) != 0:
        sql = "SELECT * FROM violation \
            WHERE (%s = 'all' OR land_id = %s) \
            AND (%s = 'all' OR node_id = %s) \
            AND (sensor = %s OR %s = 'all') \
            AND (v_timestamp > date_sub(now(), interval %s day) and v_timestamp < date_sub(now(), interval %s day)) \
            ORDER BY v_timestamp DESC LIMIT %s"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor, older_time, recent_time, limit))
    else:
        sql = "SELECT * FROM violation \
            WHERE (%s = 'all' OR land_id = %s) \
            AND (%s = 'all' OR node_id = %s) \
            AND (sensor = %s OR %s = 'all') \
            ORDER BY v_timestamp DESC LIMIT %s"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor, limit))

    myresult = mycursor.fetchall()

    return myresult

#------------------------

def get_violation_one(land_id, node_id, timestamp):

    mydb = ""
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "password",
            database = "iot_project_db"
        )
    except mysql.connector.Error as e:
        log.log_err("failed connection to mysql db")
        return
    mycursor = mydb.cursor(prepared=True)

    sql = "SELECT * FROM violation \
        WHERE land_id = %s \
        AND node_id = %s \
        AND v_timestamp = %s"
    mycursor.execute(sql, (land_id, node_id, timestamp))

    myresult = mycursor.fetchone()

    return myresult

#---------------------

def get_irrigation(land_id, node_id, older_time, recent_time, limit):

    mydb = ""
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "password",
            database = "iot_project_db"
        )
    except mysql.connector.Error as e:
        log.log_err("failed connection to mysql db")
        return
    mycursor = mydb.cursor(prepared=True)

    if int(older_time) != 0 and int(recent_time) != 0:
        sql = "SELECT * FROM irrigation \
            WHERE (%s = 'all' OR land_id = %s) \
            AND (%s = 'all' OR node_id = %s) \
            AND (i_timestamp > date_sub(now(), interval %s day) and i_timestamp < date_sub(now(), interval %s day)) \
            ORDER BY i_timestamp LIMIT %s"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, older_time, recent_time, limit))
    else:
        sql = "SELECT * FROM irrigation \
            WHERE (%s = 'all' OR land_id = %s) \
            AND (%s = 'all' OR node_id = %s) \
            ORDER BY i_timestamp LIMIT %s"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, limit))

    myresult = mycursor.fetchall()

    return myresult

#--------------------

def get_irrigation_one(land_id, node_id, timestamp):

    mydb = ""
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "password",
            database = "iot_project_db"
        )
    except mysql.connector.Error as e:
        log.log_err("failed connection to mysql db")
        return
    mycursor = mydb.cursor(prepared=True)

    sql = "SELECT * FROM irrigation \
        WHERE land_id = %s \
        AND node_id = %s \
        AND i_timestamp = %s"
    mycursor.execute(sql, (land_id, node_id, timestamp))

    myresult = mycursor.fetchone()

    return myresult

