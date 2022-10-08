from persistence import get_mysql_db
import log 

#-----------------------------------

def print_lands(land_list):

    if not land_list:
        log.log_err(f"There are no lands")
        return
    log.log_console("-----------------------")
    log.log_console("      LAND LIST")
    for land in land_list:
        log.log_console("-----------------------")
        log.log_console(f"land_id:      {land[0]}")
        log.log_console(f"area:         {land[1]}")
        log.log_console(f"locality:     {land[2]}")
        log.log_console(f"name:         {land[3]}")
        log.log_console(f"crop:         {land[4]}")
        log.log_console(f"soil_type:    {land[5]}")
        log.log_console(f"mst_trashold: {land[6]}")
        log.log_console(f"min_ph:       {land[7]}")
        log.log_console(f"max_ph:       {land[8]}")
        log.log_console(f"min_tmp:      {land[9]}")
        log.log_console(f"max_tmo:      {land[10]}")
    log.log_console("-----------------------")

def view_lands():

    land_id = ""
    log.log_console("View lands ('cancel' to quit) ")
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
    log.log_console("-----------------------")
    log.log_console("  CONFIGURATION LIST")
    for config in config_list:
        log.log_console("-----------------------")
        log.log_console(f"land_id:         {config[0]}")
        log.log_console(f"node_id:         {config[1]}")
        log.log_console(f"protocol:        {config[2]}")
        log.log_console(f"status:          {config[4]}")
        log.log_console(f"timestamp:       {config[5]}")
        log.log_console(f"irr_enabled:     {config[6]}")
        log.log_console(f"irr_limit        {config[7]}")
        log.log_console(f"irr_duration:    {config[8]}")
        log.log_console(f"mst_timer:       {config[9]}")
        log.log_console(f"ph_timer:        {config[10]}")
        log.log_console(f"light_timer:     {config[11]}")
        log.log_console(f"tmp_timer:       {config[12]}")

    log.log_console("-----------------------")

def view_configurations():
    
    land_id = ""
    node_id = ""
    
    log.log_console("View configurations (type 'cancel' to quit)")
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
    log.log_console("-----------------------")
    log.log_console("   MEASUREMENT LIST")
    for measurement in measurement_list:
        log.log_console("-----------------------")
        log.log_console(f"land_id:     {measurement[0]}")
        log.log_console(f"node_id:     {measurement[1]}")
        log.log_console(f"timestamp:   {measurement[2]}")
        log.log_console(f"sensor:      {measurement[3]}")
        log.log_console(f"value:       {measurement[4]}")
    
    log.log_console("-----------------------")


def view_last_measurements():

    land_id = ""
    node_id = ""
    sensor = ""
    older_time = ""
    recent_time = ""

    log.log_console("View measurement events (Type 'cancel' to quit)")
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

    log.log_console("Insert the time period in days (both 0 for all)")
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
    log.log_console("-----------------------")
    log.log_console("    VIOLATION LIST")
    for violation in violation_list:
        log.log_console("-----------------------")
        log.log_console(f"land_id:     {violation[0]}")
        log.log_console(f"node_id:     {violation[1]}")
        log.log_console(f"timestamp:   {violation[2]}")
        log.log_console(f"sensor:      {violation[3]}")
        log.log_console(f"value:       {violation[4]}")
    
    log.log_console("-----------------------")

def view_last_violations():

    land_id = ""
    node_id = ""
    sensor = ""
    older_time = ""
    recent_time = ""

    log.log_console("View violation events (Type 'cancel' to quit)")
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

    log.log_console("Insert the time period in days (both 0 for all)")
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
    log.log_console("-----------------------")
    log.log_console("   IRRIGATION LIST")
    for irrigation in irrigation_list:
        log.log_console("-----------------------")
        log.log_console(f"land_id:     {irrigation[0]}")
        log.log_console(f"node_id:     {irrigation[1]}")
        log.log_console(f"timestamp:   {irrigation[2]}")
        log.log_console(f"irr_status:  {irrigation[3]}")
    
    log.log_console("-----------------------")

def view_last_irrigations():

    log.log_console("View irrigation events (Type 'cancel' to quit)")
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

    log.log_console("Insert the time period in days (both 0 for all)")
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

    
