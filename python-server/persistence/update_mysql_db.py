import mysql.connector
import log 
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

def update_land(id, area, locality, name, crop, soil_type, mst_trashold, min_ph, max_ph, min_tmp, max_tmp):
    
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "UPDATE land  \
        SET area = %s, locality = %s, \
        name = %s, crop = %s, soil_type = %s, \
        mst_trashold = %s, min_ph = %s, max_ph = %s, \
        min_tmp = %s, max_tmp = %s \
        WHERE id = %s"
    mycursor.execute(sql, (area, locality, name, crop, soil_type, mst_trashold, min_ph, max_ph, min_tmp, max_tmp, id))
    mydb.commit()

#----------------------------

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
