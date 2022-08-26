

def view_lands():

    cmd = input("[!] Select a land or type 'all': ")
    if cmd.isdigit():
        land_id = cmd
        #TODO get land and print
        print("land ", land_id)
    elif cmd == "all":
        #TODO: get lands form mysql db and print
        print("lands all")
    else:
        print("[-] not valid command")

#-------

def view_configurations():
    
    cmd = input("[!] Select the land_id: ")
    if not cmd.isdigit():
        print("[-] not value land_id")
        return
    land_id = cmd
    
    cmd = input("[!] Select the node_id: ")
    if not cmd.isdigit():
        print("[-] not value node_id")
        return
    node_id = cmd

    #TODO get configurations from mysql db and print


#-------

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

    cmd = input("[!] Select the sensor: ")
    if cmd != 'moisture' and cmd != 'ph' and cmd != 'light' and cmd != 'tmp' and cmd != 'all':
        print("[-] sensor not valid")
        return
    sensor = cmd

    print("[!] Insert the time period in minutes")
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

    if older <= recent:
        print("[-] older value has to be greater then the recent one")
        return

    #TODO get events from mysql in the period [older, recent] and print

#-------

def view_last_violations():

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

    cmd = input("[!] Select the sensor: ")
    if cmd != 'moisture' and cmd != 'ph' and cmd != 'light' and cmd != 'tmp' and cmd != 'all':
        print("[-] sensor not valid")
        return
    sensor = cmd

    print("[!] Insert the time period in minutes")
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

    if older <= recent:
        print("[-] older value has to be greater then the recent one")
        return

    #TODO get violations from mysql in the period [older, recent] and print

#-------

def view_last_irrigations():

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

    print("[!] Insert the time period in minutes")
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

    if older <= recent:
        print("[-] older value has to be greater then the recent one")
        return

    #TODO get events from mysql in the period [older, recent] and print

    
