from persistence import delete_mysql_db
from persistence import get_mysql_db

#---------------------

def delete_configuration_vw():

    land_id = ""
    node_id = ""

    print("[!] Delete configuration (type 'cancel' to quit)")
    while True:
        land_id = input("land_id: ")
        if land_id == "cancel":
            return
        if land_id.isdigit() and land_id > 0:
            break
        else:
            print("[-] invalid value")
    while True:
        node_id = input("node_id: ")
        if node_id == "cancel":
            return
        if node_id.isdigit() and node_id > 0:
            break
        else:
            print("[-] invalid value")

    delete_mysql_db.delete_configuration(land_id, node_id)
    config = get_mysql_db.get_config(land_id, node_id, True)

    if not config:
        print("[+] configuration eliminated")
    else:
        print("[-] delete configuratino failed")

#--------------------------

def delete_land_vw():

    land_id = ""

    print("[!] Delete land (type cancel to quit)")
    while True:
        land_id = input("land_id: ")
        if land_id == "cancel":
            return
        if land_id.isdigit() and land_id > 0:
            break
        else:
            print("[-] invalid value")

    delete_mysql_db.delete_land(land_id)
    land = get_mysql_db.get_land(land_id, True)

    if not land:
        print("[+] land eliminated")
    else:
        print("[-] delete land failed")    

#----------------------

def delete_measurement_many_vw():

    land_id = ""
    node_id = ""
    sensor = ""
    older_time = ""
    recent_time = ""

    print("[!] Delete measurement events (Type 'cancel' to quit)")
    while True:
        land_id = input("land_id: ")
        if land_id == "cancel":
            return
        node_id = input("node_id: ")
        if node_id == "cancel":
            return
        sensor = input("sensor (moisture/ph/light/tmp/all): ")
        if sensor == "cancel":
            return
        if (land_id.isdigit() and land_id > 0
            and node_id.isdigit() and node_id > 0
            and (sensor == "moisture" or sensor == "ph" or sensor == "light" or sensor == "tmp" or sensor == "all")
        ):
            break
        else:
            print("[-] invalid values")

    print("[!] Insert the time period in days (both 0 for all)")
    while True:
        older_time = input("older value: ")
        if older_time == "cancel":
            return
        recent_time = input("recent value: ")
        if recent_time == "cancel":
            return
        if older_time.isdigit() and recent_time.isdigit() and int(older_time) >= int(recent_time):
            break
        else:
            print("[-] values are not correct")

    delete_mysql_db.delete_measurement_many(land_id, node_id, sensor, older_time, recent_time)
    measurements = get_mysql_db.get_measurement(land_id, node_id, sensor, older_time, recent_time)
    if not measurements:
         print("[+] measurements eliminated")
    else:
        print("[-] delete measurements failed")

#---------------

def delete_measurement_one_vw():

    land_id = ""
    node_id = ""
    timestamp = ""

    print("[!] Delete measurement event (Type 'cancel' to quit)")
    while True:
        land_id = input("land_id: ")
        if land_id == "cancel":
            return
        node_id = input("node_id: ")
        if node_id == "cancel":
            return
        timestamp = input("timestamp: ")
        if timestamp == "cancel":
            return
        if land_id.isdigit() and land_id > 0
            and node_id.isdigit() and node_id > 0
            and not timestamp.isdigit():
            break
        else:
            print("[-] invalid values")


    delete_mysql_db.delete_measurement_one(land_id, node_id, timestamp)
    measurement = get_mysql_db.get_measurement_one(land_id, node_id, timestamp)
    if not measurement:
         print("[+] measurement eliminated")
    else:
        print("[-] delete measurement failed")

#----------------------

def delete_violation_many_vw():

    land_id = ""
    node_id = ""
    sensor = ""
    older_time = ""
    recent_time = ""

    print("[!] Delete violation events (Type 'cancel' to quit)")
    while True:
        land_id = input("land_id: ")
        if land_id == "cancel":
            return
        node_id = input("node_id: ")
        if node_id == "cancel":
            return
        sensor = input("sensor (moisture/ph/light/tmp/all): ")
        if sensor == "cancel":
            return
        if land_id.isdigit() and land_id > 0
            and node_id.isdigit() and node_id > 0
            and (sensor == "moisture" or sensor == "ph" or sensor == "light" or sensor == "tmp" or sensor == "all"):
            break
        else:
            print("[-] invalid values")

    print("[!] Insert the time period in days (both 0 for all)")
    while True:
        older_time = input("older value: ")
        if older_time == "cancel":
            return
        recent_time = input("recent value: ")
        if recent_time == "cancel":
            return
        if older_time.isdigit() and recent_time.isdigit() and int(older_time) >= int(recent_time):
            break
        else:
            print("[-] values are not correct")

    delete_mysql_db.delete_violation_many(land_id, node_id, sensor, older_time, recent_time)
    violations = get_mysql_db.get_violation(land_id, node_id, sensor, older_time, recent_time)
    if not violations:
         print("[+] violations eliminated")
    else:
        print("[-] delete violations failed")

#---------------

def delete_violation_one_vw():

    land_id = ""
    node_id = ""
    timestamp = ""

    print("[!] Delete violation event (Type 'cancel' to quit)")
    while True:
        land_id = input("land_id: ")
        if land_id == "cancel":
            return
        node_id = input("node_id: ")
        if node_id == "cancel":
            return
        timestamp = input("timestamp: ")
        if timestamp == "cancel":
            return
        if land_id.isdigit() and land_id > 0
            and node_id.isdigit() and node_id > 0
            and not timestamp.isdigit():
            break
        else:
            print("[-] invalid values")


    delete_mysql_db.delete_violation_one(land_id, node_id, timestamp)
    violation = get_mysql_db.get_violation_one(land_id, node_id, timestamp)
    if not violation:
         print("[+] violation eliminated")
    else:
        print("[-] delete violation failed")

#----------------------

def delete_irrigation_many_vw():

    land_id = ""
    node_id = ""
    older_time = ""
    recent_time = ""

    print("[!] Delete irrigation events (Type 'cancel' to quit)")
    while True:
        land_id = input("land_id: ")
        if land_id == "cancel":
            return
        node_id = input("node_id: ")
        if node_id == "cancel":
            return
        if land_id.isdigit() and land_id > 0
            and node_id.isdigit() and node_id > 0:
            break
        else:
            print("[-] invalid values")

    print("[!] Insert the time period in days (both 0 for all)")
    while True:
        older_time = input("older value: ")
        if older_time == "cancel":
            return
        recent_time = input("recent value: ")
        if recent_time == "cancel":
            return
        if older_time.isdigit() and recent_time.isdigit() and int(older_time) >= int(recent_time):
            break
        else:
            print("[-] values are not correct")

    delete_mysql_db.delete_irrigation_many(land_id, node_id, older_time, recent_time)
    irrigations = get_mysql_db.get_irrigation(land_id, node_id, older_time, recent_time)
    if not irrigations:
         print("[+] irrigations eliminated")
    else:
        print("[-] delete irrigations failed")

#---------------

def delete_irrigation_one_vw():

    land_id = ""
    node_id = ""
    timestamp = ""

    print("[!] Delete irrigation event (Type 'cancel' to quit)")
    while True:
        land_id = input("land_id: ")
        if land_id == "cancel":
            return
        node_id = input("node_id: ")
        if node_id == "cancel":
            return
        timestamp = input("timestamp: ")
        if timestamp == "cancel":
            return
        if land_id.isdigit() and land_id > 0
            and node_id.isdigit() and node_id > 0
            and not timestamp.isdigit():
            break
        else:
            print("[-] invalid values")


    delete_mysql_db.delete_irrigation_one(land_id, node_id, timestamp)
    irrigation = get_mysql_db.get_irrigation_one(land_id, node_id, timestamp)
    if not irrigation:
         print("[+] irrigation eliminated")
    else:
        print("[-] delete irrigation failed")
