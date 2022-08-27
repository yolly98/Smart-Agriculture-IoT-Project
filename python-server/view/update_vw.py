from persistence import update_mysql_db
from persistence import get_mysql_db

#-------------------------------

def update_configuration_vw():

    land_id = ""
    node_id = ""
    status = ""
    irr_enabled = ""
    irr_limit = ""
    irr_duration = ""
    mst_timer = ""
    ph_timer = ""
    tmp_timer = ""

    print("[!] Update Configuration (type 'cancel' to quit)")
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

    old_configuration = get_mysql_db.get_config(land_id, node_id, True)
    if not old_configuration:
        print("[-] not exists the configuration (", land_id, ", ", node_id, ")")
        return

    print("[-] Note: type 'x' to not update the attribute")
    while True:
        status = input("status: ")
        if status == "cancel":
            return
        if status == 'x':
            status = old_configuration[2]
            break
        if status == 'online' or status == 'offline' or status == 'null':
            break
        else:
            print("[-] invalid value")
    while True:
        irr_enabled = input("irr_enabled: ")
        if irr_enabled == "cancel":
            return
        if irr_enabled == 'x':
            irr_enabled = old_configuration[4]
            break
        if irr_enabled == 'true' or irr_enabled == 'false':
            break
        else:
            print("[-] invalid value")
    while True:
        irr_limit = input("irr_limit: ")
        if irr_limit == "cancel":
            return
        if irr_limit == 'x':
            irr_limit = old_configuration[5]
            break
        if irr_limit.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        irr_duration = input("irr_duration: ")
        if irr_duration == "cancel":
            return
        if irr_duration == 'x':
            irr_duration = old_configuration[6]
            break
        if irr_duration.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        mst_timer = input("mst_timer: ")
        if mst_timer == "cancel":
            return
        if mst_timer == 'x':
            mst_timer = old_configuration[7]
            break
        if mst_timer.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        ph_timer = input("ph_timer: ")
        if ph_timer == "cancel":
            return
        if ph_timer == 'x':
            ph_timer = old_configuration[8]
            break
        if ph_timer.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        light_timer = input("light_timer: ")
        if light_timer == "cancel":
            return
        if light_timer == 'x':
            light_timer = old_configuration[9]
            break
        if light_timer.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        tmp_timer = input("tmp_timer: ")
        if tmp_timer == "cancel":
            return
        if tmp_timer == 'x':
            tmp_timer = old_configuration[10]
            break
        if tmp_timer.isdigit():
            break
        else:
            print("[-] invalid value")

    update_mysql_db.update_configuration(land_id, node_id, irr_enabled, irr_limit, irr_duration, mst_timer, ph_timer, light_timer, tmp_timer)
    new_config = get_mysql_db.get_config(land_id, node_id, True)
    if new_config:
        print("[+] ", new_config)
    else:
        print("[-] add configuration failed")

#----------------

def update_land_vw():


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

    print("[!] Update land (type 'cancel' to quit")
    while True:
        land_id = input("land_id: ")
        if land_id == "cancel":
            return
        if land_id.isdigit() and int(land_id) > 0:
            break
        else:
            print("[-] invalid value")


    old_land = get_mysql_db.get_land(land_id, True)
    if not old_land:
        print("[-] not exists the land ", land_id)
        return
    
    print("[!] Type 'x' to not update the attribute")
    while True:
        area = input("area: ")
        if area == "cancel":
            return
        if area == 'x':
            area = old_land[1]
            break
        if area.isdigit() and float(area) > 0:
            break
        else:
            print("[-] invalid value")
    while True:
        locality = input("locality: ")
        if locality == "cancel":
            return
        if locality == 'x':
            locality = old_land[2]
            break
        if not locality.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        name = input("name: ")
        if name == "cancel":
            return
        if name == 'x':
            name = old_land[3]
            break
        if not name.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        crop = input("crop: ")
        if crop == "cancel":
            return
        if crop == 'x':
            crop = old_land[4]
            break
        if not crop.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        soil_type = input("soil_type: ")
        if soil_type == "cancel":
            return
        if soil_type == 'x':
            soil_type = old_land[5]
            break
        if not soil_type.isdigit():
            break
        else:
            print("[-] invalid value")
    while True:
        mst_trashold = input("mst_trashold: ")
        if mst_trashold == "cancel":
            return
        if mst_trashold == 'x':
            mst_trashold = old_land[6]
            break
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
            if min_ph == 'x':
                min_ph = old_land[7]
            if max_ph == 'x':
                max_ph = old_land[8]
            if int(min_ph) <= int(max_ph):
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
            if min_tmp == 'x':
                min_tmp = old_land[9]
            if max_tmp == 'x':
                max_tmp = old_land[10]
            if int(min_tmp) <= int(max_tmp):
                break
            else:
                print("[-] invalid values")

    update_mysql_db.update_land(land_id, area, locality, name, crop, soil_type, mst_trashold, min_ph, max_ph, min_tmp, max_tmp)
    new_land = get_mysql_db.get_land(land_id, True)
    if new_land:
        print("[+] ", new_land)
    else:
        print("[-] add land failed")

#-------------

def set_node_online_vw():

    land_id = ""
    node_id = ""

    print("[!] Set a node 'online' (type 'cancel' to quit)")
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

    update_mysql_db.set_node_online(land_id, node_id)
    node = get_mysql_db.get_config(land_id, node_id, True)

    if node:
        print("[+] ", node)
    else:
        print("[-] set node online failed")

#---------------------

def set_all_node_offline_vw():
    update_mysql_db.set_all_node_offline()
    print("[+] set all node offline completed")
    
