import mysql.connector

#-----------------------------------

def print_lands(land_list):
    for land in land_list:
        print("-----------------")
        print("land_id:      ", land[0])
        print("area:         ", land[1])
        print("locality:     ", land[2])
        print("name:         ", land[3])
        print("crop:         ", land[4])
        print("soil_type:    ", land[5])
        print("mst_trashold: ", land[6])
        print("min_ph:       ", land[7])
        print("max_ph:       ", land[8])
        print("min_light:    ", land[9])
        print("max_light:    ", land[10])
        print("min_tmp:      ", land[11])
        print("max_tmo:      ", land[12])
    print("-----------------")

def view_lands():

    land_id = input("[!] Select a land or type 'all': ")
    
    if land_id.isdigit() or land_id == 'all':
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "password",
            database = "iot_project_db"
        )
        mycursor = mydb.cursor(prepared=True)
        sql = "SELECT * FROM land WHERE (id = %s OR %s = 'all' OR %s = 0)" 
        mycursor.execute(sql, (land_id, land_id, land_id))
        myresult = mycursor.fetchall()
        print_lands(myresult)
    else:
        print("[-] not valid command")

#----------------------------------

def print_configurations(config_list):

    for config in config_list:
        print("-----------------")
        print("land_id:         ", config[0])
        print("node_id:         ", config[1])
        print("status:          ", config[2])
        print("timestamp:       ", config[3])
        print("irr_enabled:     ", config[4])
        print("irr_duration:    ", config[5])
        print("mst_timer:       ", config[6])
        print("ph_timer:        ", config[7])
        print("light_timer:     ", config[8])
        print("tmp_timer:       ", config[9])

    print("-----------------")

def view_configurations():
    
    cmd = input("[!] Select the land_id (type 0 for all): ")
    if not cmd.isdigit():
        print("[-] not value land_id")
        return
    land_id = cmd
    
    cmd = input("[!] Select the node_id (type 0 for all): ")
    if not cmd.isdigit():
        print("[-] not value node_id")
        return
    node_id = cmd

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    sql = "SELECT * FROM configuration WHERE (land_id = %s OR %s = 0) AND (node_id = %s OR %s = 0)"
    mycursor.execute(sql, (land_id, land_id, node_id, node_id))
    myresult = mycursor.fetchall()
    print_configurations(myresult)


#---------------------------------------
def print_measurements(measurement_list):

    for measurement in measurement_list:
        print("-----------------")
        print("land_id:     ", measure[0])
        print("node_id:     ", measure[1])
        print("timestamp:   ", measure[2])
        print("sensor:      ", measure[3])
        print("value:       ", measure[4])
    
    print("-----------------")


def view_last_measurements():

    cmd = input("[!] Select the land_id (type 0 for all): ")
    if not cmd.isdigit():
        print("[-] not value land_id")
        return
    land_id = cmd
    
    cmd = input("[!] Select the node_id (type 0 for all): ")
    if not cmd.isdigit():
        print("[-] not value node_id")
        return
    node_id = cmd

    cmd = input("[!] Select the sensor (moisture, ph. light, tmp) or 'all': ")
    if cmd != 'moisture' and cmd != 'ph' and cmd != 'light' and cmd != 'tmp' and cmd != 'all':
        print("[-] sensor not valid")
        return
    sensor = cmd

    print("[!] Insert the time period in days (both 0 for all)")
    cmd = input("older value: ")
    if not cmd.isdigit:
        print("[-] older value is not correct")
        return
    older = cmd

    cmd = input("more recent value: ")
    if not cmd.isdigit:
        print("[-] recent value is not correct")
        return
    recent = cmd

    if int(older) < int(recent):
        print("[-] older value has to be greater then the recent one")
        return

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    if int(older) != 0 and int(recent) != 0:
        sql = "SELECT * FROM measurement WHERE (land_id = %s OR %s = 0) AND (node_id = %s OR %s = 0) AND (sensor = %s OR %s = 'all') AND (m_timestamp BEETWEEN date_sub(now(), interval %s day) and date_add(now(), interval %s day))"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor, older, recent))
    else:
        sql = "SELECT * FROM measurement WHERE (land_id = %s OR %s = 0) AND (node_id = %s OR %s = 0) AND (sensor = %s OR %s = 'all') "
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor))

    myresult = mycursor.fetchall()
    print_measurements(myresult)

#-----------------------------------------

def print_violations(violation_list):

    for violation in violation_list:
        print("-----------------")
        print("land_id:     ", violation[0])
        print("node_id:     ", violation[1])
        print("timestamp:   ", violation[2])
        print("sensor:      ", violation[3])
        print("value:       ", violation[4])
    
    print("-----------------")

def view_last_violations():

    cmd = input("[!] Select the land_id (type 0 for all): ")
    if not cmd.isdigit():
        print("[-] not value land_id")
        return
    land_id = int(cmd)
    
    cmd = input("[!] Select the node_id (type 0 for all): ")
    if not cmd.isdigit():
        print("[-] not value node_id")
        return
    node_id = int(cmd)

    cmd = input("[!] Select the sensor (moisture, ph. light, tmp) or 'all': ")
    if cmd != 'moisture' and cmd != 'ph' and cmd != 'light' and cmd != 'tmp' and cmd != 'all':
        print("[-] sensor not valid")
        return
    sensor = cmd

    print("[!] Insert the time period in days (both 0 for all)")
    cmd = input("older value: ")
    if not cmd.isdigit:
        print("[-] older value is not correct")
        return
    older = int(cmd)

    cmd = input("more recent value: ")
    if not cmd.isdigit:
        print("[-] recent value is not correct")
        return
    recent = int(cmd)

    if int(older) < int(recent):
        print("[-] older value has to be greater then the recent one")
        return

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    if int(older) != 0 and int(recent) != 0:
        sql = "SELECT * FROM violation WHERE (land_id = %s OR %s = 0) AND (node_id = %s OR %s = 0) AND (sensor = %s OR %s = 'all') AND (v_timestamp BEETWEEN date_sub(now(), interval %s day) and date_add(now(), interval %s day))"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor, older, recent))
    else:
        sql = "SELECT * FROM violation WHERE (land_id = %s OR %s = 0) AND (node_id = %s OR %s = 0) AND (sensor = %s OR %s = 'all') "
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, sensor, sensor))

    myresult = mycursor.fetchall()
    print_violations(myresult)

#---------------------------------------
def print_irrigations(irrigation_list):

    for irrigation in irrigation_list:
        print("-----------------")
        print("land_id:     ", irrigation[0])
        print("node_id:     ", irrigation[1])
        print("timestamp:   ", irrigation[2])
        print("irr_status:  ", irrigation[3])
    
    print("-----------------")

def view_last_irrigations():

    cmd = input("[!] Select the land_id (type 0 for all): ")
    if not cmd.isdigit():
        print("[-] not value land_id")
        return
    land_id = int(cmd)
    
    cmd = input("[!] Select the node_id (type 0 for all): ")
    if not cmd.isdigit():
        print("[-] not value node_id")
        return
    node_id = int(cmd)

    print("[!] Insert the time period in days (both 0 for all)")
    cmd = input("older value: ")
    if not cmd.isdigit:
        print("[-] older value is not correct")
        return
    older = int(cmd)

    cmd = input("more recent value: ")
    if not cmd.isdigit:
        print("[-] recent value is not correct")
        return
    recent = int(cmd)

    if int(older) < int(recent):
        print("[-] older value has to be greater then the recent one")
        return

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "iot_project_db"
    )
    mycursor = mydb.cursor(prepared=True)

    if int(older) != 0 and int(recent) != 0:
        sql = "SELECT * FROM irrigation WHERE (land_id = %s OR %s = 0) AND (node_id = %s OR %s = 0) AND (i_timestamp BEETWEEN date_sub(now(), interval %s day) and date_add(now(), interval %s day))"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id, older, recent))
    else:
        sql = "SELECT * FROM irrigation WHERE (land_id = %s OR %s = 0) AND (node_id = %s OR %s = 0)"
        mycursor.execute(sql, (land_id, land_id, node_id, node_id))

    myresult = mycursor.fetchall()
    print_irrigations(myresult)

    
