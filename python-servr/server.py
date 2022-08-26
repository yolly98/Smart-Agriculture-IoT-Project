import command

# ------------MAIN-----------

while True:

    cmd = input("$ Type a command: ")
    if cmd == "help":
        print("[!] command list:")
        print(". irr_cmd")
        print(". get_config")
        print(". assign_config")
        print(". timer_cmd")
        print(". get_sensor")
        print(". is_alive")
        continue

    if cmd == "irr_cmd":
        command.irr_cmd()
    elif cmd == "get_config":
        command.get_config()
    elif cmd == "assign_config":
        command.assign_config(0, 0)
    elif cmd == "timer_cmd":
        command.timer_cmd()
    elif cmd == "get_sensor":
        command.get_sensor()
    elif cmd == "is_alive":
        command.is_alive()
    else:
        print("[-] command not valid!")