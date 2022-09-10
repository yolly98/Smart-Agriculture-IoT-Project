#include "mqtt_module.c"

/*------------------------UTILITY------------------------------------------*/


bool isNumber(char * text){

    int len = strlen(text);
    for(int i = 0; i < len; i++){
        if(text[i] > 47 && text[i] < 58)
            continue;
        else 
            return false;
    }

    return true;
}

/*--------*/

void print_config(){

    printf("[!] actual configuration: \n");
    printf("land_id: %d\n", node_memory.configuration.land_id);
    printf("node_id: %d\n", node_memory.configuration.node_id);
    printf("irr_config: { enabled: %s, irr_limit: %d, irr_duration: %d }\n",
        node_memory.configuration.irr_config.enabled?"true":"false",
        node_memory.configuration.irr_config.irr_limit,
        node_memory.configuration.irr_config.irr_duration);
    printf("mst_timer: %d\n", node_memory.configuration.mst_timer);
    printf("ph_timer: %d\n", node_memory.configuration.ph_timer);
    printf("light_timer: %d\n", node_memory.configuration.light_timer);
    printf("tmp_timer: %d\n", node_memory.configuration.tmp_timer);
    printf("-----------------------------\n");

}

/*--------*/

void parse_json(char json[], int n_arguments, char arguments[][100]){

    int value_parsed = 0;
    int len = 0;
    bool value_detected = false;

    for(int i = 0; json[i] != '\0' && value_parsed < n_arguments; i++){
        
        if(json[i] == ':'){
            i++; //there is the space after ':'
            value_detected = true;
            len = 0;
        }
        else if(value_detected && (json[i] == ',' || json[i] == ' ' || json[i] == '}')){
            value_detected = false;
            arguments[value_parsed][len] = '\0';
            value_parsed++;
        }
        else if(value_detected && json[i] == '{'){
            value_detected = false;
        }
        else if(value_detected){
            if(json[i] =='\'' || json[i] == '\"')
                continue;
            arguments[value_parsed][len] = json[i];
            len++;
        }

    }

    //for(int i = 0; i < n_arguments;i++)
    //    printf("[arg parsed #%d] %s \n", i, arguments[i]);        

}

/*-----------------COMMAND ELABORATOR----------------------------*/

bool elaborate_cmd(char msg[]){ 
    
    char cmd[1][100];
    parse_json(msg, 1, cmd);
    if(strcmp(cmd[0], IRR_CMD) == 0){
        printf("[!] IRR_CMD command elaboration ...\n");

        int n_arguments = 5;
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments);

        if(strcmp(arguments[1], "null") != 0)
            node_memory.configuration.irr_config.enabled = ((strcmp(arguments[1], "true") == 0)?true:false);
        if(strcmp(arguments[2], "null") != 0)
            node_memory.irr_status = ((strcmp(arguments[2], "on") == 0)?true:false);
        if(isNumber(arguments[3]) && atoi(arguments[3]) != 0)
            node_memory.configuration.irr_config.irr_limit = atoi(arguments[3]);
        if(isNumber(arguments[4]) && atoi(arguments[4]) != 0)
            node_memory.configuration.irr_config.irr_duration = atoi(arguments[4]);

        send_irrigation();
        printf("[+] IRR_CMD command elaborated with success\n");

    }
    else if(strcmp(cmd[0], GET_CONFIG) == 0){
        printf("[!] GET_CONFIG command elaboration ...\n");
        send_status();
        printf("[+] GET_CONFIG command elaborated with success\n");
    }
    else if(strcmp(cmd[0], TIMER_CMD) == 0){
        printf("[!] TIMER_CMD command elaboration ...\n");
        
        int n_arguments = 3;
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments);
        
        if(strcmp(arguments[1], "mst") == 0 && isNumber(arguments[2])){
            node_memory.configuration.mst_timer = atoi(arguments[2]);
            ctimer_set(&node_timers.mst_ctimer, node_memory.configuration.mst_timer * CLOCK_MINUTE, get_soil_moisture, NULL);
        }
        else if(strcmp(arguments[1], "ph") == 0 && isNumber(arguments[2])){
            node_memory.configuration.ph_timer = atoi(arguments[2]);
            ctimer_set(&node_timers.ph_ctimer, node_memory.configuration.ph_timer * CLOCK_MINUTE, get_ph_level, NULL);
        }
        else if(strcmp(arguments[1], "light") == 0 && isNumber(arguments[2])){
            node_memory.configuration.light_timer = atoi(arguments[2]);
            ctimer_set(&node_timers.light_ctimer, node_memory.configuration.light_timer * CLOCK_MINUTE, get_lihght_raw, NULL);
        }
        else if(strcmp(arguments[1], "tmp") == 0 && isNumber(arguments[2])){
            node_memory.configuration.tmp_timer = atoi(arguments[2]);
            ctimer_set(&node_timers.tmp_ctimer, node_memory.configuration.tmp_timer * CLOCK_MINUTE, get_soil_tmp, NULL);
        }

        send_status();
        printf("[+] TIMER_CMD command elaborated with success\n");
    }
    else if(strcmp(cmd[0], ASSIGN_CONFIG) == 0){
        printf("[!] ASSIGN_CONFIG command elaboration ...\n");
        mqtt_module.state = STATE_CONFIGURED;
        int n_arguments = 8; 
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments );

        node_memory.configuration.irr_config.enabled = (strcmp(arguments[1], "true") == 0)?true:false;
        node_memory.configuration.irr_config.irr_limit = atoi(arguments[2]);
        node_memory.configuration.irr_config.irr_duration = atoi(arguments[3]);
        node_memory.configuration.mst_timer = atoi(arguments[4]);
        node_memory.configuration.ph_timer = atoi(arguments[5]);
        node_memory.configuration.light_timer = atoi(arguments[6]);
        node_memory.configuration.tmp_timer = atoi(arguments[7]);

        send_status();
        printf("[+] ASSIGN_CONFIG command elaborated with success\n");
    }
    else if(strcmp(cmd[0], ASSIGN_I_CONFIG) == 0){
        printf("[!] ASSIGN_I_CONFIG command elaboration ...\n");
        int n_arguments = 4; 
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments );

        node_memory.configuration.irr_config.enabled = (strcmp(arguments[1], "true") == 0)?true:false;
        node_memory.configuration.irr_config.irr_limit = atoi(arguments[2]);
        node_memory.configuration.irr_config.irr_duration = atoi(arguments[3]);

        printf("[+] ASSIGN_I_CONFIG command elaborated with success\n");
    }
    else if(strcmp(cmd[0], ASSIGN_T_CONFIG) == 0){
        printf("[!] ASSIGN_T_CONFIG command elaboration ...\n");
        mqtt_module.state = STATE_CONFIGURED;
        int n_arguments = 5; 
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments );

        node_memory.configuration.mst_timer = atoi(arguments[1]);
        node_memory.configuration.ph_timer = atoi(arguments[2]);
        node_memory.configuration.light_timer = atoi(arguments[3]);
        node_memory.configuration.tmp_timer = atoi(arguments[4]);

        send_status();
        printf("[+] ASSIGN_T_CONFIG command elaborated with success\n");
    }
    else if(strcmp(cmd[0], ERROR_LAND) == 0){
        printf("[!] ERROR_LAND received, reset the node\n");
        process_exit(&mqtt_node);
    }
    else if(strcmp(cmd[0], ERROR_ID) == 0){
        printf("[!] ERROR_ID received, reset the node\n");
        process_exit(&mqtt_node);
    }
    else if(strcmp(cmd[0], GET_SENSOR) == 0){
        printf("[!] GET_SENSOR command elaboration ...\n");

        int n_arguments = 2;
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments);

        if(strcmp(arguments[1], "mst") == 0)
            get_soil_moisture();
        else if(strcmp(arguments[1], "ph") == 0)
            get_ph_level();
        else if(strcmp(arguments[1], "light") == 0)
            get_lihght_raw();
        else if(strcmp(arguments[1], "tmp") == 0)
            get_soil_tmp();

        printf("[+] GET_SENSOR command elaborated with success\n");
    }
    else if(strcmp(cmd[0], IS_ALIVE) == 0){
        printf("!] IS_ALIVE command elaboration ...\n");
        send_is_alive_ack();
        printf("[+] IS_ALIVE command elaborated with success\n");
    }
    else{
        printf("[-] command received not correct (%s)\n", cmd[0]);
        return false;
    }

    return true;

}

/*------------------------------------------*/

//used to test if the node can send

void is_alive_received_sim(char msg[]){

    sprintf(msg, "{ \"cmd\": \"%s\" }", IS_ALIVE);
}

/*------------------SENDING TO SERVER (SIMULATED)-----------------------------*/

void send_config_request(){

    char msg[MSG_SIZE];
    sprintf(msg, "{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d } }",
        CONFIG_RQST,
        node_memory.configuration.land_id,
        node_memory.configuration.node_id
        );
    printf(" >  %s \n", msg);
    mqtt_publish_service(msg, CONFIG_RQST);
}

/*--------*/

void send_status(){

    char msg[MSG_SIZE];
    sprintf(msg, "{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d, \"irr_config\": { \"enabled\": \"%s\", \"irr_limit\": %d, \"irr_duration\": %d }, \"mst_timer\": %d, \"ph_timer\": %d, \"light_timer\": %d, \"tmp_timer\": %d } } ",
        STATUS,
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        node_memory.configuration.irr_config.enabled?"true":"false",
        node_memory.configuration.irr_config.irr_limit,
        node_memory.configuration.irr_config.irr_duration,
        node_memory.configuration.mst_timer,
        node_memory.configuration.ph_timer,
        node_memory.configuration.light_timer,
        node_memory.configuration.tmp_timer
        );
    
    printf(" >  %s \n", msg);
    mqtt_publish_service(msg, STATUS);

}

/*-------*/

void send_irrigation(){

    char msg[MSG_SIZE];
    sprintf(msg, "{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d, \"status\": \"%s\" } }",
        IRRIGATION,
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        node_memory.irr_status?"on":"off"
        );
    printf(" >  %s \n", msg);
    mqtt_publish_service(msg, IRRIGATION);
}

/*-------*/

void send_is_alive_ack(){

    char msg[MSG_SIZE];
    sprintf(msg, "{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d } }",
        IS_ALIVE_ACK,
        node_memory.configuration.land_id,
        node_memory.configuration.node_id
        );
    
    printf(" >  %s \n", msg);
    mqtt_publish_service(msg, IS_ALIVE_ACK);
}

/*----------------- SENSORS READINGS (SIMULATED) AND SEND TO SERVER -------------------------------*/

void irr_stopping(){
    node_memory.irr_status = false;
    send_irrigation();
}

void get_soil_moisture(){
    
    if(node_timers.sensor_timer_are_setted)
        ctimer_restart(&node_timers.mst_ctimer);

    short moisture = (15 + random_rand()%50);
    node_memory.measurements.soil_moisture = moisture;
    printf("[+] soil moisture detected: %d\n", moisture);

    char msg[MSG_SIZE];
    sprintf(msg,"{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d, \"value\": %d } }",
        MOISTURE,
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        moisture);

    printf(" >  %s\n", msg);
    mqtt_publish_service(msg, MOISTURE);

    bool irr_enabled = node_memory.configuration.irr_config.enabled;
    int irr_limit = node_memory.configuration.irr_config.irr_limit;
    if( irr_enabled && moisture < irr_limit){
        node_memory.irr_status = true;
        int irr_duration = node_memory.configuration.irr_config.irr_duration;
        send_irrigation();
        if(!node_timers.irr_timer_is_setted){
            ctimer_set(&node_timers.irr_duration_ctimer, irr_duration * CLOCK_MINUTE, irr_stopping, NULL);
            node_timers.irr_timer_is_setted = true;
        }
        else
            ctimer_restart(&node_timers.irr_duration_ctimer);
    }

}

/*--------*/

void get_ph_level(){

    if(node_timers.sensor_timer_are_setted)
        ctimer_restart(&node_timers.ph_ctimer);

    short ph_level = (5 + random_rand()%5);
    node_memory.measurements.ph_level =  ph_level;
    printf("[+] ph level detected: %d\n", ph_level);

    char msg[MSG_SIZE];
    sprintf(msg,"{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d, \"value\": %d } }",
        PH, 
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        ph_level
        );
    
    printf(" >  %s\n", msg);
    mqtt_publish_service(msg, PH);

}

/*--------*/

void get_lihght_raw(){

    if(node_timers.sensor_timer_are_setted)
        ctimer_restart(&node_timers.light_ctimer);

    int light = random_rand()%28;
    node_memory.measurements.light_raw =  light;
    printf("[+] light raw detected: %d\n", light);

    char msg[MSG_SIZE];
    sprintf(msg,"{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d, \"value\": %d } }",
        LIGHT,
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        light
        );
    printf(" >  %s\n", msg);
    mqtt_publish_service(msg, LIGHT);
} 

/*--------*/

void get_soil_tmp(){

    if(node_timers.sensor_timer_are_setted)
        ctimer_restart(&node_timers.tmp_ctimer);

    int tmp = (5 + random_rand()%35);
    node_memory.measurements.soil_temperature =  tmp;
    printf("[+] soil temperature detected: %d\n", tmp);

    char msg[MSG_SIZE];
    sprintf(msg,"{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d, \"value\": %d } }",
        TMP,
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        tmp
        );
    printf(" >  %s\n", msg);
    mqtt_publish_service(msg, TMP);
}
/*-------------------------------------------------------------------*/

void receive_configuration_sim(){

    char msg[200];
    sprintf(msg, "{ \"cmd\": \"%s\", \"body\": { \"irr_config\": { \"enabled\": \"true\", \"irr_limit\": 38, \"irr_duration\": 20 }, \"mst_timer\": 720, \"ph_timer\": 720, \"light_timer\": 60, \"tmp_timer\": 60 } } ",
        ASSIGN_CONFIG
    );
    printf(" <  %s \n", msg);
    elaborate_cmd(msg);
}


//PROCESS(mqtt_node, "Mqtt node");
//AUTOSTART_PROCESSES(&mqtt_node);

PROCESS_THREAD(mqtt_node, ev, data){
    
    static unsigned int btn_count;
    static bool led_status;
    static bool land_id_setted;

    PROCESS_BEGIN();

    /*------------INITIALIZATION---------------*/
    printf("[!] initialization ...\n");

    printf("[!] manual land_id setting\n");

    etimer_set(&node_timers.led_etimer,0.5 * CLOCK_SECOND);
    btn_count = 0;
    led_status = false;
    leds_single_off(LEDS_RED);
    land_id_setted = false;

    while(1){
        PROCESS_YIELD();

        if(ev == PROCESS_EVENT_TIMER){
            if(etimer_expired(&node_timers.led_etimer)){
                led_status = !led_status;
                leds_single_toggle(LEDS_RED);
                etimer_restart(&node_timers.led_etimer);
            }

            if(btn_count > 0 && etimer_expired(&node_timers.btn_etimer)){
                if(!land_id_setted){
                    node_memory.configuration.land_id = btn_count;
                    land_id_setted = true;
                    leds_single_on(LEDS_RED);
                    led_status = true;
                    etimer_reset_with_new_interval(&node_timers.led_etimer, 2 * CLOCK_SECOND);
                    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&node_timers.led_etimer));
                    etimer_reset_with_new_interval(&node_timers.led_etimer, 0.5 * CLOCK_SECOND);
                    printf("[!] manual node_id setting\n");
                    btn_count = 0;
                }
                else{
                    node_memory.configuration.node_id = btn_count;
                    break;
                }
                
            }
        }
        if(ev == serial_line_event_message){
            char * msg = (char*)data;
            printf("[!] recevived '%s' by serial\n", msg);
            if(isNumber(msg) && atoi(msg) > 0){
               if(!land_id_setted){
                    node_memory.configuration.land_id = atoi(msg);
                    land_id_setted = true;
                    leds_single_on(LEDS_RED);
                    led_status = true;
                    etimer_reset_with_new_interval(&node_timers.led_etimer, 2 * CLOCK_SECOND);
                    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&node_timers.led_etimer));
                    etimer_reset_with_new_interval(&node_timers.led_etimer, 0.5 * CLOCK_SECOND);
                    printf("[!] manual node_id setting\n");
                    btn_count = 0;
                }
                else{
                    node_memory.configuration.node_id = atoi(msg);
                    break;
                }
            }
            else    
                printf("[-] is not a number\n");
        }
        if(ev == button_hal_press_event){
            printf("[!] button pressed\n");
            btn_count++;
            if(btn_count == 1 && !land_id_setted)
                etimer_set(&node_timers.btn_etimer, 3 * CLOCK_SECOND);
            else    
                etimer_restart(&node_timers.btn_etimer);
        }

        
    }

    leds_single_off(LEDS_RED);
    led_status = false;

    printf("[+] land %d selected \n", node_memory.configuration.land_id);
    printf("[+] id %d selected \n", node_memory.configuration.node_id);


    printf("[!] intialization ended\n");

    mqtt_init_service();

    while(true){
        PROCESS_YIELD();
        if(etimer_expired(&node_timers.mqtt_etimer)){
            mqtt_connection_service();
            if(mqtt_module.state == STATE_SUBSCRIBED)
                break;
        }
    }
    /*---------------CONFIGURATION-------------------*/
    
    printf("[!] configuration ... \n");

    send_config_request();
//    receive_configuration_sim();  //uncomment here to jump the configuration phase
//    print_config();

    while(true){
        PROCESS_YIELD();
        if(etimer_expired(&node_timers.mqtt_etimer))
            mqtt_connection_service();

        if(!(NETSTACK_ROUTING.node_is_reachable() && NETSTACK_ROUTING.get_root_ipaddr(&mqtt_module.dest_ipaddr))){
            printf("the border router is not reachable yet\n");
        }
          
        if(mqtt_module.state == STATE_CONFIGURED)
            break;
    }

    printf("[+] configuration ended\n");

    /*------------------FIRST MEASUREMENTS------------*/


    printf("[!] first sensor detection ...\n");

    node_timers.sensor_timer_are_setted = false;
    node_timers.irr_timer_is_setted = false;
    get_soil_moisture();
    get_ph_level();
    get_lihght_raw();
    get_soil_tmp();

    ctimer_set(&node_timers.mst_ctimer, node_memory.configuration.mst_timer * CLOCK_MINUTE, get_soil_moisture, NULL);
    ctimer_set(&node_timers.ph_ctimer, node_memory.configuration.ph_timer * CLOCK_MINUTE, get_ph_level, NULL);
    ctimer_set(&node_timers.light_ctimer, node_memory.configuration.light_timer * CLOCK_MINUTE, get_lihght_raw, NULL);
    ctimer_set(&node_timers.tmp_ctimer, node_memory.configuration.tmp_timer * CLOCK_MINUTE, get_soil_tmp, NULL);

    node_timers.sensor_timer_are_setted = true;

    /*---------------NORMAL WORKLOAD----------------*/

    while(true){

        PROCESS_YIELD();
        
        if(!(NETSTACK_ROUTING.node_is_reachable() && NETSTACK_ROUTING.get_root_ipaddr(&mqtt_module.dest_ipaddr))){
            printf("the border router is not reachable yet\n");
        }

        if(etimer_expired(&node_timers.mqtt_etimer) || ev == PROCESS_EVENT_POLL)
            mqtt_connection_service();

        //simulation of received command by server
        if(ev == serial_line_event_message){
            char * cmd = (char*)data;
            char msg[200];
        
            if(strcmp(cmd, "help") == 0){
                printf("[!] command list:\n");
                printf("    . is_alive\n");
                printf("    . mqtt_status\n");
                printf("---------------\n");
                continue;
            }
            else if(strcmp(cmd, "is_alive") == 0){
                is_alive_received_sim(msg);
            }
            else if(strcmp(cmd, "mqtt_status") == 0){
                print_mqtt_status();
                continue;
            }

            printf(" <  [%s] %s \n",cmd, msg);

            elaborate_cmd(msg);
    
        }
    }

    /*---------------------------------------------*/

    PROCESS_END();
}
