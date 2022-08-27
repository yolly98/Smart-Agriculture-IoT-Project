from persistence import add_mysql_db
from persistence import get_mysql_db

def add_configuration_vw():

    land_id = ""
    node_id = ""
    status = ""
    irr_enabled = ""
    irr_limit = ""
    irr_duration = ""
    mst_timer = ""
    ph_timer = ""
    tmp_timer = ""

    print("[!] New Configuration (type 'cancel' to quit)")
    while True:
        land_id = input("land_id: ")
        if land_id == "cancel":
            return
        if land_id.isdigit() and int(land_id) > 0:
            break
        else:
            print("[-] invalid value")
    while True:
        node_id = input("node_id: ")
        if node_id == "cancel":
            return
        if node_id.isdigit() and int(node_id) > 0:
            break
        else:
            print("[-] invalid value")
    while True:
        status = input("status: ")
        if status == "cancel":
            return
        if status == 'online' or status == 'offline' or status == 'null':
            break
        else:
            print("[-] invalid value")
    while True:
        irr_enabled = input("irr_enabled: ")
        if irr_enabled == "cancel":
            return
        if irr_enabled == 'true' or irr_enabled == 'false':
            break
        else:
            print("[-] invalid value")
    while True:
        irr_limit = input("irr_limit: ")
        if irr_limit == "cancel":
            return
        if irr_limit.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        irr_duration = input("irr_duration: ")
        if irr_duration == "cancel":
            return
        if irr_duration.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        mst_timer = input("mst_timer: ")
        if mst_timer == "cancel":
            return
        if mst_timer.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        ph_timer = input("ph_timer: ")
        if ph_timer == "cancel":
            return
        if ph_timer.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        light_timer = input("light_timer: ")
        if light_timer == "cancel":
            return
        if light_timer.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        tmp_timer = input("tmp_timer: ")
        if tmp_timer == "cancel":
            return
        if tmp_timer.isdigit():
            break
        else:
            print("[-] invalid value")

    add_mysql_db.add_configuration(land_id, node_id, status, irr_enabled, irr_limit, irr_duration, mst_timer, ph_timer, light_timer, tmp_timer)
    new_config = get_mysql_db.get_config(land_id, node_id, True)
    if new_config:
        print("[+] ", new_config)
    else:
        print("[-] add configuration failed")

#-----------------------

def add_land_vw():

    land_id = ""
    area = ""
    locality = ""
    name = ""
    crop = ""
    soil_type = ""
    mst_trashold = ""
    min_ph = ""
    max_ph = ""
    min_tmp = ""
    max_tmp = ""

    print("[!] New land (type 'cancel' to quit)")
    while True:
        land_id = input("land_id: ")
        if land_id == "cancel":
            return
        if land_id.isdigit() and int(land_id) > 0:
            break
        else:
            print("[-] invalid value")
    while True:
        area = input("area: ")
        if area == "cancel":
            return
        if area.isdigit() and float(area) > 0:
            break
        else:
            print("[-] invalid value")
    while True:
        locality = input("locality: ")
        if locality == "cancel":
            return
        if not locality.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        name = input("name: ")
        if name == "cancel":
            return
        if not name.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        crop = input("crop: ")
        if crop == "cancel":
            return
        if not crop.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        soil_type = input("soil_type: ")
        if soil_type == "cancel":
            return
        if not soil_type.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        mst_trashold = input("mst_trashold: ")
        if mst_trashold == "cancel":
            return
        if mst_trashold.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        min_ph = input("min_ph: ")
        if min_ph == "cancel":
            return
        max_ph = input("max_ph: ")
        if max_ph == "cancel":
            return
        if min_ph.isdigit() and max_ph.isdigit() and int(min_ph) <= int(max_ph):
            break
        else:
            print("[-] invalid values")
    while True:
        min_tmp = input("min_tmp: ")
        if min_tmp == "cancel":
            return
        max_tmp = input("max_tmp: ")
        if max_tmp == "cancel":
            return
        if min_tmp.isdigit() and max_tmp.isdigit() and int(min_tmp) <= int(max_tmp):
            break
        else:
            print("[-] invalid values")

    add_mysql_db.add_land(land_id, area, locality, name, crop, soil_type, mst_trashold, min_ph, max_ph, min_tmp, max_tmp)
    new_land = get_mysql_db.get_land(land_id, True)
    if new_land:
        print("[+] ", new_land)
    else:
        print("[-] add land failed")

#-----------------------

def add_irrigation_event_vw():

    land_id = ""
    node_id = ""
    status = ""

    print("[!] New irrigation event (Type 'cancel' to quit)")
    while True:
        land_id = input("land_id: ")
        if land_id == "cancel":
            return
        node_id = input("node_id: ")
        if node_id == "cancel":
            return
        status = input("status (on/off): ")
        if status == "cancel":
            return
        if land_id.isdigit() and int(land_id) > 0 and node_id.isdigit() and int(node_id) > 0 and (status == "on" or status == "off"):
            break
        else:
            print("[-] invalid values")

    add_mysql_db.add_irrigation_event(land_id, node_id, status)
    new_irrigation =get_mysql_db.get_irrigation(land_id, node_id, 1, 0, 1)
    if new_irrigation:
        print("[+] ", new_irrigation[0])
    else:
        print("[-] add irrigation event failed")

#---------------------------

def add_measurement_event_vw():

    land_id = ""
    node_id = ""
    sensor = ""
    value = ""

    print("[!] New measurement event (Type 'cancel' to quit)")
    while True:
        land_id = input("land_id: ")
        if land_id == "cancel":
            return
        node_id = input("node_id: ")
        if node_id == "cancel":
            return
        sensor = input("sensor (moisture/ph/light/tmp): ")
        if sensor == "cancel":
            return
        value = input("value: ")
        if value == "cancel":
            return
        if (land_id.isdigit() and int(land_id) > 0
            and node_id.isdigit() and int(node_id) > 0
            and (sensor == "moisture" or sensor == "ph" or sensor == "light" or sensor == "tmp")
            and value.isdigit()
        ):
            break
        else:
            print("[-] invalid values")

    add_mysql_db.add_measurement_event(land_id, node_id, sensor, value)
    new_measurement = get_mysql_db.get_measurement(land_id, node_id, sensor, 1, 0, 1)
    if new_measurement:
        print("[+] ", new_measurement[0])
    else:
        print("[-] add new measurement event failed")
