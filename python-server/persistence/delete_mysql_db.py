import mysql.connector

#---------------------DELETE--------------

def delete_configuration(land_id, node_id):
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "DELETE from configuration WHERE (land_id = %s OR %s = 'all') AND (node_id = %s OR %s = 'all')"
    mycursor.execute(sql, (land_id, land_id, node_id, node_id))
    mydb.commit()

#---------

def delete_land(land_id):
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "DELETE from land WHERE (land_id = %s OR %s = 'all')"
    mycursor.execute(sql, (land_id, land_id))
    mydb.commit()

#--------


def delete_measurement_many(land_id, node_id, sensor, older_time, recent_time):

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    if int(older_time) != 0 and int(recent_time) != 0:
        sql = "DELETE FROM measurement \
            WHERE (land_id = %s OR %s = 'all') \
            AND (node_id = %s OR %s = 'all') \
            AND (sensor = %s OR %s = 'all') \
            AND (m_timestamp BEETWEEN date_sub(now(), interval %s day) and date_sub(now(), interval %s day))"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor, older_time, recent_time))
    else:
        sql = "DELETE FROM measurement \
            WHERE (land_id = %s OR %s = 'all') \
            AND (node_id = %s OR %s = 'all') \
            AND (sensor = %s OR %s = 'all') "
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor))

    mydb.commit()

#--------

def delete_measurement_one(land_id, node_id, timestamp):

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    
    sql = "DELETE FROM measurement \
        WHERE land_id = %s \
        AND node_id = %s  \
        AND m_timestamp = %s"
    mycursor.execute(sql, (land_id, node_id, timestamp))
    

    mydb.commit()

#-------------------------

def delete_violation_many(land_id, node_id, sensor, older_time, recent_time):

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    if int(older_time) != 0 and int(recent_time) != 0:
        sql = "DELETE FROM violation \
            WHERE (land_id = %s OR %s = 'all') \
            AND (node_id = %s OR %s = 'all') \
            AND (sensor = %s OR %s = 'all') \
            AND (v_timestamp BEETWEEN date_sub(now(), interval %s day) and date_sub(now(), interval %s day))"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor, older_time, recent_time))
    else:
        sql = "DELETE FROM violation \
            WHERE (land_id = %s OR %s = 'all') \
            AND (node_id = %s OR %s = 'all') \
            AND (sensor = %s OR %s = 'all') "
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor))

    mydb.commit()

#--------------

def delete_violation_one(land_id, node_id, timestamp):

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)
    
    sql = "DELETE FROM violation \
        WHERE land_id \
        AND node_id = %s \
        AND v_timestamp = %s"
    mycursor.execute(sql, (land_id, node_id, timestamp))

    mydb.commit()

#---------------------

def delete_irrigation_many(land_id, node_id, older_time, recent_time):

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    if int(older_time) != 0 and int(recent_time) != 0:
        sql = "DELETE FROM irrigation \
            WHERE (land_id = %s OR %s = 'all') \
            AND (node_id = %s OR %s = 'all') \
            AND (i_timestamp BEETWEEN date_sub(now(), interval %s day) and date_sub(now(), interval %s day))"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, older_time, recent_time))
    else:
        sql = "DELETE FROM irrigation \
            WHERE (land_id = %s OR %s = 'all') \
            AND (node_id = %s OR %s = 'all')"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id))

    mydb.commit()

#---------------

def delete_irrigation_one(land_id, node_id, timestamp):

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)


    sql = "DELETE FROM irrigation \
        WHERE land_id = %s \
        AND (node_id = %s \
        AND i_timestamp = %s"
    mycursor.execute(sql, (land_id,  node_id, timestamp))

    mydb.commit()
