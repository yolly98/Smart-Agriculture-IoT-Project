import mysql_module

#-----------------------------------

def print_lands(land_list):

    if not land_list:
        print("[-] There are no lands")
        return
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

    land_id = input("[!] Type the land_id or 'all': ")
    
    if land_id.isdigit() or land_id == 'all':
        lands = mysql_module.get_land(land_id, False)
        print_lands(lands)
    else:
        print("[-] not valid command")

#----------------------------------

def print_configurations(config_list):

    if not config_list:
        print("[-] There are no configurations saved")
        return
    for config in config_list:
        print("-----------------")
        print("land_id:         ", config[0])
        print("node_id:         ", config[1])
        print("status:          ", config[2])
        print("timestamp:       ", config[3])
        print("irr_enabled:     ", config[4])
        print("irr_limit        ", config[5])
        print("irr_duration:    ", config[6])
        print("mst_timer:       ", config[7])
        print("ph_timer:        ", config[8])
        print("light_timer:     ", config[9])
        print("tmp_timer:       ", config[10])

    print("-----------------")

def view_configurations():
    
    cmd = input("[!] Type the land_id or 'all': ")
    if not cmd.isdigit() and cmd != 'all':
        print("[-] not value land_id")
        return
    land_id = cmd
    
    cmd = input("[!] Type the node_id or 'all': ")
    if not cmd.isdigit() and cmd != 'all':
        print("[-] not value node_id")
        return
    node_id = cmd

    configs = mysql_module.get_config(land_id, node_id, False)
    print_configurations(configs)


#---------------------------------------
def print_measurements(measurement_list):

    if not measurement_list:
        print("[-] There are no measurements")
        return
    for measurement in measurement_list:
        print("-----------------")
        print("land_id:     ", measurement[0])
        print("node_id:     ", measurement[1])
        print("timestamp:   ", measurement[2])
        print("sensor:      ", measurement[3])
        print("value:       ", measurement[4])
    
    print("-----------------")


def view_last_measurements():

    cmd = input("[!] Type the land_id or 'all': ")
    if not cmd.isdigit() and cmd != 'all':
        print("[-] not value land_id")
        return
    land_id = cmd
    
    cmd = input("[!] Type the node_id or 'all': ")
    if not cmd.isdigit() and cmd != 'all':
        print("[-] not value node_id")
        return
    node_id = cmd

    cmd = input("[!] Type the sensor (moisture, ph. light, tmp) or 'all': ")
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

    measurements = mysql_module.get_measurement(land_id, node_id, sensor, older, recent)
    print_measurements(measurements)

#-----------------------------------------

def print_violations(violation_list):

    if not violation_list:
        print("[-] There are no violations")
        return
    for violation in violation_list:
        print("-----------------")
        print("land_id:     ", violation[0])
        print("node_id:     ", violation[1])
        print("timestamp:   ", violation[2])
        print("sensor:      ", violation[3])
        print("value:       ", violation[4])
    
    print("-----------------")

def view_last_violations():

    cmd = input("[!] Type the land_id or 'all': ")
    if not cmd.isdigit() and cmd != 'all':
        print("[-] not value land_id")
        return
    land_id = cmd
    
    cmd = input("[!] Type the node_id or 'all': ")
    if not cmd.isdigit() and cmd != 'all':
        print("[-] not value node_id")
        return
    node_id = cmd

    cmd = input("[!] Type the sensor (moisture, ph. light, tmp) or 'all': ")
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

    violations = mysql_module.get_violation(land_id, node_id, sensor, older, recent)
    print_violations(violations)

#---------------------------------------
def print_irrigations(irrigation_list):

    if not irrigation_list:
        print("[-] There are no irrigations")
        return
    for irrigation in irrigation_list:
        print("-----------------")
        print("land_id:     ", irrigation[0])
        print("node_id:     ", irrigation[1])
        print("timestamp:   ", irrigation[2])
        print("irr_status:  ", irrigation[3])
    
    print("-----------------")

def view_last_irrigations():

    cmd = input("[!] Type the land_id or 'all': ")
    if not cmd.isdigit() and cmd != 'all':
        print("[-] not value land_id")
        return
    land_id = cmd
    
    cmd = input("[!] Type the node_id or 'all': ")
    if not cmd.isdigit() and cmd != 'all':
        print("[-] not value node_id")
        return
    node_id = cmd

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

    irrigations = mysql_module.get_irrigation(land_id, node_id, older, recent)
    print_irrigations(irrigations)

    
