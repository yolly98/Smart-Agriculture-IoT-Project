from persistence import delete_mysql_db
from persistence import get_mysql_db
import log 

#---------------------

def delete_configuration_vw():

    land_id = ""
    node_id = ""

    log.log_info("Delete configuration (type 'cancel' to quit)")
    while True:
        land_id = log.log_input("land_id (number or 'all'): ")
        if land_id == "cancel":
            return
        if land_id == 'all' or (land_id.isdigit() and int(land_id) > 0):
            break
        else:
            log.log_err(f"invalid value")
    while True:
        node_id = log.log_input("node_id (number or 'all'): ")
        if node_id == "cancel":
            return
        if node_id == 'all' or (node_id.isdigit() and int(node_id) > 0):
            break
        else:
            log.log_err(f"invalid value")

    delete_mysql_db.delete_configuration(land_id, node_id)
    config = get_mysql_db.get_config(land_id, node_id, True)

    if not config:
        log.log_success("configuration eliminated")
    else:
        log.log_err(f"delete configuratino failed")

#--------------------------

def delete_land_vw():

    land_id = ""

    log.log_info("Delete land (type 'cancel' to quit)")
    while True:
        land_id = log.log_input("land_id (number or 'all'): ")
        if land_id == "cancel":
            return
        if land_id == 'all' or (land_id.isdigit() and int(land_id)) > 0:
            break
        else:
            log.log_err(f"invalid value")

    delete_mysql_db.delete_land(land_id)
    land = get_mysql_db.get_land(land_id, True)

    if not land:
        log.log_success("land eliminated")
    else:
        log.log_err(f"delete land failed")    

#----------------------

def delete_measurement_many_vw():

    land_id = ""
    node_id = ""
    sensor = ""
    older_time = ""
    recent_time = ""

    log.log_info("Delete measurement events (Type 'cancel' to quit)")
    while True:
        land_id = log.log_input("land_id (number or 'all'): ")
        if land_id == "cancel":
            return
        node_id = log.log_input("node_id (number or 'all'): ")
        if node_id == "cancel":
            return
        sensor = log.log_input("sensor (moisture/ph/light/tmp/all): ")
        if sensor == "cancel":
            return
        if ( (land_id == 'all' or (land_id.isdigit() and int(land_id) > 0))
            and (node_id == 'all' or (node_id.isdigit() and int(node_id) > 0))
            and (sensor == "moisture" or sensor == "ph" or sensor == "light" or sensor == "tmp" or sensor == "all")
        ):
            break
        else:
            log.log_err(f"invalid values")

    log.log_info("Insert the time period in days (both 0 for all)")
    while True:
        older_time = log.log_input("older value: ")
        if older_time == "cancel":
            return
        recent_time = log.log_input("recent value: ")
        if recent_time == "cancel":
            return
        if older_time.isdigit() and recent_time.isdigit() and int(older_time) >= int(recent_time):
            break
        else:
            log.log_err(f"values are not correct")

    delete_mysql_db.delete_measurement_many(land_id, node_id, sensor, older_time, recent_time)
    measurements = get_mysql_db.get_measurement(land_id, node_id, sensor, older_time, recent_time,1)
    if not measurements:
         log.log_success("measurements eliminated")
    else:
        log.log_err(f"delete measurements failed")

#---------------

def delete_measurement_one_vw():

    land_id = ""
    node_id = ""
    timestamp = ""

    log.log_info("Delete measurement event (Type 'cancel' to quit)")
    while True:
        land_id = log.log_input("land_id: ")
        if land_id == "cancel":
            return
        node_id = log.log_input("node_id: ")
        if node_id == "cancel":
            return
        timestamp = log.log_input("timestamp: ")
        if timestamp == "cancel":
            return
        if (land_id.isdigit() and int(land_id) > 0
            and node_id.isdigit() and int(node_id) > 0
            and not timestamp.isdigit()
        ):
            break
        else:
            log.log_err(f"invalid values")


    delete_mysql_db.delete_measurement_one(land_id, node_id, timestamp)
    measurement = get_mysql_db.get_measurement_one(land_id, node_id, timestamp)
    if not measurement:
         log.log_success("measurement eliminated")
    else:
        log.log_err(f"delete measurement failed")

#----------------------

def delete_violation_many_vw():

    land_id = ""
    node_id = ""
    sensor = ""
    older_time = ""
    recent_time = ""

    log.log_info("Delete violation events (Type 'cancel' to quit)")
    while True:
        land_id = log.log_input("land_id (number or 'all'): ")
        if land_id == "cancel":
            return
        node_id = log.log_input("node_id (number or 'all'): ")
        if node_id == "cancel":
            return
        sensor = log.log_input("sensor (moisture/ph/light/tmp/all): ")
        if sensor == "cancel":
            return
        if ((land_id == 'all' or (land_id.isdigit() and int(land_id) > 0))
            and (node_id == 'all' or (node_id.isdigit() and int(node_id) > 0))
            and (sensor == "moisture" or sensor == "ph" or sensor == "light" or sensor == "tmp" or sensor == "all")
        ):
            break
        else:
            log.log_err(f"invalid values")

    log.log_info("Insert the time period in days (both 0 for all)")
    while True:
        older_time = log.log_input("older value: ")
        if older_time == "cancel":
            return
        recent_time = log.log_input("recent value: ")
        if recent_time == "cancel":
            return
        if older_time.isdigit() and recent_time.isdigit() and int(older_time) >= int(recent_time):
            break
        else:
            log.log_err(f"values are not correct")

    delete_mysql_db.delete_violation_many(land_id, node_id, sensor, older_time, recent_time)
    violations = get_mysql_db.get_violation(land_id, node_id, sensor, older_time, recent_time, 1)
    if not violations:
         log.log_success("violations eliminated")
    else:
        log.log_err(f"delete violations failed")

#---------------

def delete_violation_one_vw():

    land_id = ""
    node_id = ""
    timestamp = ""

    log.log_info("Delete violation event (Type 'cancel' to quit)")
    while True:
        land_id = log.log_input("land_id: ")
        if land_id == "cancel":
            return
        node_id = log.log_input("node_id: ")
        if node_id == "cancel":
            return
        timestamp = log.log_input("timestamp: ")
        if timestamp == "cancel":
            return
        if (land_id.isdigit() and int(land_id) > 0
            and node_id.isdigit() and int(node_id) > 0
            and not timestamp.isdigit()
        ):
            break
        else:
            log.log_err(f"invalid values")


    delete_mysql_db.delete_violation_one(land_id, node_id, timestamp)
    violation = get_mysql_db.get_violation_one(land_id, node_id, timestamp)
    if not violation:
         log.log_success("violation eliminated")
    else:
        log.log_err(f"delete violation failed")

#----------------------

def delete_irrigation_many_vw():

    land_id = ""
    node_id = ""
    older_time = ""
    recent_time = ""

    log.log_info("Delete irrigation events (Type 'cancel' to quit)")
    while True:
        land_id = log.log_input("land_id (number or 'all'): ")
        if land_id == "cancel":
            return
        node_id = log.log_input("node_id (number or 'all'): ")
        if node_id == "cancel":
            return
        if ((land_id == 'all' or (land_id.isdigit() and int(land_id) > 0))
            and (node_id == 'all' or (node_id.isdigit() and int(node_id) > 0))
        ):
            break
        else:
            log.log_err(f"invalid values")

    log.log_info("Insert the time period in days (both 0 for all)")
    while True:
        older_time = log.log_input("older value: ")
        if older_time == "cancel":
            return
        recent_time = log.log_input("recent value: ")
        if recent_time == "cancel":
            return
        if older_time.isdigit() and recent_time.isdigit() and int(older_time) >= int(recent_time):
            break
        else:
            log.log_err(f"values are not correct")

    delete_mysql_db.delete_irrigation_many(land_id, node_id, older_time, recent_time)
    irrigations = get_mysql_db.get_irrigation(land_id, node_id, older_time, recent_time, 1)
    if not irrigations:
         log.log_success("irrigations eliminated")
    else:
        log.log_err(f"delete irrigations failed")

#---------------

def delete_irrigation_one_vw():

    land_id = ""
    node_id = ""
    timestamp = ""

    log.log_info("Delete irrigation event (Type 'cancel' to quit)")
    while True:
        land_id = log.log_input("land_id: ")
        if land_id == "cancel":
            return
        node_id = log.log_input("node_id: ")
        if node_id == "cancel":
            return
        timestamp = log.log_input("timestamp: ")
        if timestamp == "cancel":
            return
        if (land_id.isdigit() and int(land_id) > 0
            and node_id.isdigit() and int(node_id) > 0
            and not timestamp.isdigit()
        ):
            break
        else:
            log.log_err(f"invalid values")


    delete_mysql_db.delete_irrigation_one(land_id, node_id, timestamp)
    irrigation = get_mysql_db.get_irrigation_one(land_id, node_id, timestamp)
    if not irrigation:
         log.log_success("irrigation eliminated")
    else:
        log.log_err(f"delete irrigation failed")
