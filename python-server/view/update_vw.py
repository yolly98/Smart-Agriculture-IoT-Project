from persistence import update_mysql_db
from persistence import get_mysql_db
import log 

#-------------------------------

def update_configuration_vw():

    land_id = ""
    node_id = ""
    protocol = ""
    status = ""
    irr_enabled = ""
    irr_limit = ""
    irr_duration = ""
    mst_timer = ""
    ph_timer = ""
    tmp_timer = ""

    log.log_info("Update Configuration (type 'cancel' to quit)")
    while True:
        land_id = log.log_input("land_id: ")
        if land_id == "cancel":
            return
        if land_id.isdigit() and int(land_id) > 0:
            break
        else:
            log.log_err(f"invalid value")
    while True:
        node_id = log.log_input("node_id: ")
        if node_id == "cancel":
            return
        if node_id.isdigit() and int(node_id) > 0:
            break
        else:
            log.log_err(f"invalid value")

    old_configuration = get_mysql_db.get_config(land_id, node_id, True)
    if not old_configuration:
        log.log_err(f"not exists the configuration ({land_id}, {node_id})")
        return

    log.log_err(f"Note: type 'x' to not update the attribute")
    while True:
        protocol = log.log_input("protocol: ")
        if protocol == "cancel":
            return
        if protocol == 'x':
            protocol = old_configuration[2]
            break
        if protocol == 'COAP' or protocol == 'MQTT':
            break
        else:
            log.log_err(f"invalid value")
    while True:
        status = log.log_input("status: ")
        if status == "cancel":
            return
        if status == 'x':
            status = old_configuration[3]
            break
        if status == 'online' or status == 'offline' or status == 'null':
            break
        else:
            log.log_err(f"invalid value")
    while True:
        irr_enabled = log.log_input("irr_enabled: ")
        if irr_enabled == "cancel":
            return
        if irr_enabled == 'x':
            irr_enabled = old_configuration[5]
            break
        if irr_enabled == 'true' or irr_enabled == 'false':
            break
        else:
            log.log_err(f"invalid value")
    while True:
        irr_limit = log.log_input("irr_limit: ")
        if irr_limit == "cancel":
            return
        if irr_limit == 'x':
            irr_limit = old_configuration[6]
            break
        if irr_limit.isdigit():
            break
        else:
            log.log_err(f"invalid value")
    while True:
        irr_duration = log.log_input("irr_duration: ")
        if irr_duration == "cancel":
            return
        if irr_duration == 'x':
            irr_duration = old_configuration[7]
            break
        if irr_duration.isdigit():
            break
        else:
            log.log_err(f"invalid value")
    while True:
        mst_timer = log.log_input("mst_timer: ")
        if mst_timer == "cancel":
            return
        if mst_timer == 'x':
            mst_timer = old_configuration[8]
            break
        if mst_timer.isdigit():
            break
        else:
            log.log_err(f"invalid value")
    while True:
        ph_timer = log.log_input("ph_timer: ")
        if ph_timer == "cancel":
            return
        if ph_timer == 'x':
            ph_timer = old_configuration[9]
            break
        if ph_timer.isdigit():
            break
        else:
            log.log_err(f"invalid value")
    while True:
        light_timer = log.log_input("light_timer: ")
        if light_timer == "cancel":
            return
        if light_timer == 'x':
            light_timer = old_configuration[10]
            break
        if light_timer.isdigit():
            break
        else:
            log.log_err(f"invalid value")
    while True:
        tmp_timer = log.log_input("tmp_timer: ")
        if tmp_timer == "cancel":
            return
        if tmp_timer == 'x':
            tmp_timer = old_configuration[11]
            break
        if tmp_timer.isdigit():
            break
        else:
            log.log_err(f"invalid value")

    update_mysql_db.update_configuration(land_id, node_id, protocol, irr_enabled, irr_limit, irr_duration, mst_timer, ph_timer, light_timer, tmp_timer)
    new_config = get_mysql_db.get_config(land_id, node_id, True)
    if new_config:
        log.log_success(f"updated configuration: {new_config}")
    else:
        log.log_err(f"update configuration failed")

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

    log.log_info("Update land (type 'cancel' to quit)")
    while True:
        land_id = log.log_input("land_id: ")
        if land_id == "cancel":
            return
        if land_id.isdigit() and int(land_id) > 0:
            break
        else:
            log.log_err(f"invalid value")


    old_land = get_mysql_db.get_land(land_id, True)
    if not old_land:
        log.log_err(f"not exists the land {land_id}")
        return
    
    log.log_info("Type 'x' to not update the attribute")
    while True:
        area = log.log_input("area: ")
        if area == "cancel":
            return
        if area == 'x':
            area = old_land[1]
            break
        if area.isdigit() and float(area) > 0:
            break
        else:
            log.log_err(f"invalid value")
    while True:
        locality = log.log_input("locality: ")
        if locality == "cancel":
            return
        if locality == 'x':
            locality = old_land[2]
            break
        if not locality.isdigit():
            break
        else:
            log.log_err(f"invalid value")
    while True:
        name = log.log_input("name: ")
        if name == "cancel":
            return
        if name == 'x':
            name = old_land[3]
            break
        if not name.isdigit():
            break
        else:
            log.log_err(f"invalid value")
    while True:
        crop = log.log_input("crop: ")
        if crop == "cancel":
            return
        if crop == 'x':
            crop = old_land[4]
            break
        if not crop.isdigit():
            break
        else:
            log.log_err(f"invalid value")
    while True:
        soil_type = log.log_input("soil_type: ")
        if soil_type == "cancel":
            return
        if soil_type == 'x':
            soil_type = old_land[5]
            break
        if not soil_type.isdigit():
            break
        else:
            log.log_err(f"invalid value")
    while True:
        mst_trashold = log.log_input("mst_trashold: ")
        if mst_trashold == "cancel":
            return
        if mst_trashold == 'x':
            mst_trashold = old_land[6]
            break
        if mst_trashold.isdigit():
            break
        else:
            log.log_err(f"invalid value")
    while True:
        min_ph = log.log_input("min_ph: ")
        if min_ph == "cancel":
            return
        max_ph = log.log_input("max_ph: ")
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
                log.log_err(f"invalid values")
            
    while True:
        min_tmp = log.log_input("min_tmp: ")
        if min_tmp == "cancel":
            return
        max_tmp = log.log_input("max_tmp: ")
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
                log.log_err(f"invalid values")

    update_mysql_db.update_land(land_id, area, locality, name, crop, soil_type, mst_trashold, min_ph, max_ph, min_tmp, max_tmp)
    new_land = get_mysql_db.get_land(land_id, True)
    if new_land:
        log.log_success(f"updated land: {new_land}")
    else:
        log.log_err(f"update land failed")

#-------------

def set_node_online_vw():

    land_id = ""
    node_id = ""

    log.log_info("Set a node 'online' (type 'cancel' to quit)")
    while True:
        land_id = log.log_input("land_id: ")
        if land_id == "cancel":
            return
        if land_id.isdigit() and int(land_id) > 0:
            break
        else:
            log.log_err(f"invalid value")
    while True:
        node_id = log.log_input("node_id: ")
        if node_id == "cancel":
            return
        if node_id.isdigit() and int(node_id) > 0:
            break
        else:
            log.log_err(f"invalid value")

    update_mysql_db.set_node_online(land_id, node_id)
    node = get_mysql_db.get_config(land_id, node_id, True)

    if node:
        log.log_success(f"node: {node}")
    else:
        log.log_err(f"set node online failed")

#---------------------

def set_all_node_offline_vw():
    update_mysql_db.set_all_node_offline()
    log.log_success("set all node offline completed")
    
