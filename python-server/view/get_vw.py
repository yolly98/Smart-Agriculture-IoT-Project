from persistence import get_mysql_db
import log 

#-----------------------------------

def print_lands(land_list):

    if not land_list:
        log.log_err(f"There are no lands")
        return
    log.log_info("LAND LIST")
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
        print("min_tmp:      ", land[9])
        print("max_tmo:      ", land[10])
    print("-----------------")

def view_lands():

    land_id = ""
    log.log_info("View lands ('cancel' to quit) ")
    while True:
        land_id = log.log_input("land_id (number or 'all'): ")
        if land_id == "cancel":
            return
        if land_id.isdigit() or land_id == 'all':
            break
        else:
            log.log_err(f"invalid value")

    lands = get_mysql_db.get_land(land_id, False)
    print_lands(lands)

#----------------------------------

def print_configurations(config_list):

    if not config_list:
        log.log_err(f"There are no configurations saved")
        return
    log.log_info("CONFIGURATION LIST")
    for config in config_list:
        print("-----------------")
        print("land_id:         ", config[0])
        print("node_id:         ", config[1])
        print("protocol:        ", config[2])
        print("status:          ", config[3])
        print("timestamp:       ", config[4])
        print("irr_enabled:     ", config[5])
        print("irr_limit        ", config[6])
        print("irr_duration:    ", config[7])
        print("mst_timer:       ", config[8])
        print("ph_timer:        ", config[9])
        print("light_timer:     ", config[10])
        print("tmp_timer:       ", config[11])

    print("-----------------")

def view_configurations():
    
    land_id = ""
    node_id = ""
    
    log.log_info("View configurations (type 'cancel' to quit)")
    while True:
        land_id = log.log_input("land_id (number or 'all'): ")
        if land_id == "cancel":
            return
        if land_id.isdigit() or land_id == 'all':
            break
        else:
            log.log_err(f"invalid value")
    while True:
        node_id = log.log_input("node_id (number or 'all'): ")
        if node_id == "cancel":
            return
        if node_id.isdigit() or node_id == 'all':
            break
        else:
            log.log_err(f"invalid value")

    configs = get_mysql_db.get_config(land_id, node_id, False)
    print_configurations(configs)


#---------------------------------------
def print_measurements(measurement_list):

    if not measurement_list:
        log.log_err(f"There are no measurements")
        return
    log.log_info("MEASUREMENT LIST")
    for measurement in measurement_list:
        print("-----------------")
        print("land_id:     ", measurement[0])
        print("node_id:     ", measurement[1])
        print("timestamp:   ", measurement[2])
        print("sensor:      ", measurement[3])
        print("value:       ", measurement[4])
    
    print("-----------------")


def view_last_measurements():

    land_id = ""
    node_id = ""
    sensor = ""
    older_time = ""
    recent_time = ""

    log.log_info("View measurement events (Type 'cancel' to quit)")
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
        if ((land_id.isdigit() or land_id == "all")
            and (node_id.isdigit() or node_id == "all")
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

    measurements = get_mysql_db.get_measurement(land_id, node_id, sensor, older_time, recent_time, 10)
    print_measurements(measurements)

#-----------------------------------------

def print_violations(violation_list):

    if not violation_list:
        log.log_err(f"There are no violations")
        return
    log.log_info("VIOLATION LIST")
    for violation in violation_list:
        print("-----------------")
        print("land_id:     ", violation[0])
        print("node_id:     ", violation[1])
        print("timestamp:   ", violation[2])
        print("sensor:      ", violation[3])
        print("value:       ", violation[4])
    
    print("-----------------")

def view_last_violations():

    land_id = ""
    node_id = ""
    sensor = ""
    older_time = ""
    recent_time = ""

    log.log_info("View violation events (Type 'cancel' to quit)")
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
        if ((land_id.isdigit() or land_id == "all")
            and (node_id.isdigit() or node_id == "all")
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

    violations = get_mysql_db.get_violation(land_id, node_id, sensor, older_time, recent_time, 10)
    print_violations(violations)

#---------------------------------------
def print_irrigations(irrigation_list):

    if not irrigation_list:
        log.log_err(f"There are no irrigations")
        return
    log.log_info("IRRIGATION LIST")
    for irrigation in irrigation_list:
        print("-----------------")
        print("land_id:     ", irrigation[0])
        print("node_id:     ", irrigation[1])
        print("timestamp:   ", irrigation[2])
        print("irr_status:  ", irrigation[3])
    
    print("-----------------")

def view_last_irrigations():

    log.log_info("View irrigation events (Type 'cancel' to quit)")
    while True:
        land_id = log.log_input("land_id (number or 'all'): ")
        if land_id == "cancel":
            return
        node_id = log.log_input("node_id (number or 'all'): ")
        if node_id == "cancel":
            return
        if ((land_id.isdigit() or land_id == 'all')
            and (node_id.isdigit() or node_id == 'all')
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

    irrigations = get_mysql_db.get_irrigation(land_id, node_id, older_time, recent_time, 10)
    print_irrigations(irrigations)

    
