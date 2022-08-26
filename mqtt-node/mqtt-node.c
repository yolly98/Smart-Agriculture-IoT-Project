#include "mqtt-node.h"


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

    for(int i = 0; json[i] != '\0'; i++){
        
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
            if(json[i] =='\'')
                continue;
            arguments[value_parsed][len] = json[i];
            len++;
        }

    }

    //for(int i = 0; i < n_arguments;i++)
    //    printf("[arg parsed #%d] %s \n", i, arguments[i]);
            

}

/*-----------------COMMAND ELABORATOR----------------------------*/

bool elaborate_cmd(char msg[], char topic[]){ 
    
    if(strcmp(topic, IRR_CMD) == 0){
        printf("[!] IRR_CMD command elaboration ...\n");

        int n_arguments = 6;
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments);
        
        int land_id = node_memory.configuration.land_id;
        int node_id = node_memory.configuration.node_id;
        int dest_land_id = atoi(arguments[0]);
        int dest_node_id = atoi(arguments[1]);
        if( (dest_land_id != 0 && dest_land_id != land_id) || ( dest_node_id != 0 && dest_node_id != node_id)){
            printf("[-] this message is not for this board (%s, %s)\n", arguments[0], arguments[1]);
            return false;
        }

        if(strcmp(arguments[2], "null") != 0)
            node_memory.configuration.irr_config.enabled = ((strcmp(arguments[2], "true") == 0)?true:false);
        if(strcmp(arguments[3], "null") != 0)
            node_memory.irr_status = ((strcmp(arguments[3], "true") == 0)?true:false);
        if(strcmp(arguments[4], "null") != 0 && isNumber(arguments[4]))
            node_memory.configuration.irr_config.irr_limit = atoi(arguments[4]);
        if(strcmp(arguments[5], "null") != 0 && isNumber(arguments[5]))
            node_memory.configuration.irr_config.irr_duration = atoi(arguments[5]);

        irrigation_sim();
        printf("[+] IRR_CMD command elaborated with success\n");

    }
    else if(strcmp(topic, GET_CONFIG) == 0){
        printf("[!] GET_CONFIG command elaboration ...\n");
        
        int n_arguments = 2;
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments);
        
        int land_id = node_memory.configuration.land_id;
        int node_id = node_memory.configuration.node_id;
        int dest_land_id = atoi(arguments[0]);
        int dest_node_id = atoi(arguments[1]);
        if( (dest_land_id != 0 && dest_land_id != land_id) || ( dest_node_id != 0 && dest_node_id != node_id)){
            printf("[-] this message is not for this board (%s, %s)\n", arguments[0], arguments[1]);
            return false;
        }

        status_sim();
        printf("[+] GET_CONFIG command elaborated with success\n");
    }
    else if(strcmp(topic, TIMER_CMD) == 0){
        printf("[!] TIMER_CMD command elaboration ...\n");
        
        int n_arguments = 4;
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments);
        
        int land_id = node_memory.configuration.land_id;
        int node_id = node_memory.configuration.node_id;
        int dest_land_id = atoi(arguments[0]);
        int dest_node_id = atoi(arguments[1]);
        if( (dest_land_id != 0 && dest_land_id != land_id) || ( dest_node_id != 0 && dest_node_id != node_id)){
            printf("[-] this message is not for this board (%s, %s)\n", arguments[0], arguments[1]);
            return false;
        }

        if(strcmp(arguments[2], "moisture") == 0 && isNumber(arguments[3]))
            node_memory.configuration.mst_timer = atoi(arguments[3]);
        else if(strcmp(arguments[2], "ph") == 0 && isNumber(arguments[3]))
            node_memory.configuration.ph_timer = atoi(arguments[3]);
        else if(strcmp(arguments[2], "light") == 0 && isNumber(arguments[3]))
            node_memory.configuration.light_timer = atoi(arguments[3]);
        else if(strcmp(arguments[2], "tmp") == 0 && isNumber(arguments[3]))
            node_memory.configuration.tmp_timer = atoi(arguments[3]);

        status_sim();
        printf("[+] TIMER_CMD command elaborated with success\n");
    }
    else if(strcmp(topic, ASSIGN_CONFIG) == 0){
        printf("[!] ASSIGN_CONFIG command elaboration ...\n");
        
        int n_arguments = 9; 
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments );

        int land_id = node_memory.configuration.land_id;
        int node_id = node_memory.configuration.node_id;
        int dest_land_id = atoi(arguments[0]);
        int dest_node_id = atoi(arguments[1]);
        if( (dest_land_id != 0 && dest_land_id != land_id) || ( dest_node_id != 0 && dest_node_id != node_id)){
            printf("[-] this message is not for this board (%s, %s)\n", arguments[0], arguments[1]);
            return false;
        }

        node_memory.configuration.irr_config.enabled = arguments[2];
        node_memory.configuration.irr_config.irr_limit = atoi(arguments[3]);
        node_memory.configuration.irr_config.irr_duration = atoi(arguments[4]);

        node_memory.configuration.mst_timer = atoi(arguments[5]);
        node_memory.configuration.ph_timer = atoi(arguments[6]);
        node_memory.configuration.light_timer = atoi(arguments[7]);
        node_memory.configuration.tmp_timer = atoi(arguments[8]);

        status_sim();
        printf("[+] ASSIGN_CONFIG command elaborated with success\n");
    }
    else if(strcmp(topic, GET_SENSOR) == 0){
        printf("[!] GET_SENSOR command elaboration ...\n");

        int n_arguments = 3;
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments);

        int land_id = node_memory.configuration.land_id;
        int node_id = node_memory.configuration.node_id;
        int dest_land_id = atoi(arguments[0]);
        int dest_node_id = atoi(arguments[1]);
        if( (dest_land_id != 0 && dest_land_id != land_id) || ( dest_node_id != 0 && dest_node_id != node_id)){
            printf("[-] this message is not for this board (%s, %s)\n", arguments[0], arguments[1]);
            return false;
        }

        if(strcmp(arguments[2], "moisture") == 0)
            get_soil_moisture();
        else if(strcmp(arguments[2], "ph") == 0)
            get_ph_level();
        else if(strcmp(arguments[2], "light") == 0)
            get_lihght_raw();
        else if(strcmp(arguments[2], "tmp") == 0)
            get_soil_tmp();

        printf("[+] GET_SENSOR command elaborated with success\n");
    }
    else if(strcmp(topic, IS_ALIVE) == 0){
        printf("!] IS_ALIVE command elaboration ...\n");

        int n_arguments = 2;
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments);

        int land_id = node_memory.configuration.land_id;
        int node_id = node_memory.configuration.node_id;
        int dest_land_id = atoi(arguments[0]);
        int dest_node_id = atoi(arguments[1]);
        if( (dest_land_id != 0 && dest_land_id != land_id) || ( dest_node_id != 0 && dest_node_id != node_id)){
            printf("[-] this message is not for this board (%s, %s)\n", arguments[0], arguments[1]);
            return false;
        }

        is_alive_ack_sim();
        printf("[+] IS_ALIVE command elaborated with success\n");
    }
    else{
        printf("[-] topic received not correct (%s)\n", topic);
        return false;
    }


    return true;

}

/*-----------------COMMAND RECEIVED (SIMULATED)-----------------------------*/

void irr_cmd_received_sim(char msg[], char topic[]){

    sprintf(topic, "%s", IRR_CMD);
    sprintf(msg, "{ 'land_id': %d, 'node_id': %d, 'enable': '%s', 'status': '%s', 'limit': %d, 'irr_duration': %d } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        ((random_rand()%2)!=0)?(((random_rand()%2)!=0)?"true":"false"):"null",
        ((random_rand()%2)!=0)?(((random_rand()%2)!=0)?"on":"off"):"null",
        ((random_rand()%2)!=0)?(10 + random_rand()%30):0,
        ((random_rand()%2)!=0)?(5+ random_rand()%30):0
        );

}

/*--------*/

void get_config_received_sim(char msg[], char topic[]){

    sprintf(topic, "%s", GET_CONFIG);
    sprintf(msg, "{ 'land_id': %d, 'node_id': %d } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id);
}

/*--------*/

void assign_config_received_sim(char msg[], char topic[]){ //is a simulation of a message received from server

    sprintf(msg, "{ 'land_id': %d, 'node_id': %d, 'irr_config': { 'enabled': 'true', 'irr_limit': 22, 'irr_duration': 20 }, 'irr_timer': 720, 'ph_timer': 720, 'light_timer': 60, 'tmp_timer': 60 } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id
        );
    
    sprintf(topic, ASSIGN_CONFIG);
}

/*--------*/

void timer_cmd_received_sim(char msg[], char topic[]){

    char sensor[10];
    int rand = random_rand()%3;
    if(rand == 0)
        sprintf(sensor, "moisture");
    else if(rand == 1)
        sprintf(sensor, "ph");
    else if(rand == 2)
        sprintf(sensor, "light");
    else
        sprintf(sensor, "tmp");

    sprintf(topic, "%s", TIMER_CMD);
    sprintf(msg, "{ 'land_id': %d, 'node_id': %d, 'sensor': '%s', 'timer': %d } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        sensor,
        20 + random_rand()%690
        );
}

/*--------*/

void get_sensor_received_sim(char msg[], char topic[]){

    char sensor[10];
    int rand = random_rand()%3;
    if(rand == 0)
        sprintf(sensor, "%s", "moisture");
    else if(rand == 1)
        sprintf(sensor, "%s", "ph");
    else if(rand == 2)
        sprintf(sensor, "%s", "light");
    else
        sprintf(sensor, "%s", "tmp");

    sprintf(topic, "%s", GET_SENSOR);
    sprintf(msg, "{ 'land_id': %d, 'node_id': %d, 'tyoe': '%s' } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        sensor
        );
}

/*--------*/

void is_alive_received_sim(char msg[], char topic[]){

    sprintf(topic, "%s", IS_ALIVE);
    sprintf(msg, "{ 'land_id': %d, 'node_id': %d }", 
        node_memory.configuration.land_id,
        node_memory.configuration.node_id
        );
}

/*------------------SENDING TO SERVER (SIMULATED)-----------------------------*/

void config_request_sim(){

    char msg[100];
    char topic[50];

    sprintf(msg, "{ 'land_id': %d, 'node_id': %d } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id
        );
    sprintf(topic, CONFIG_RQST);
    printf(" >  [%s] %s \n", topic, msg);
}

/*--------*/

void status_sim(){

    char msg[200];
    char topic[50];

    sprintf(msg, "{ 'land_id': %d, 'node_id': %d, 'irr_config': { 'enabled': '%s', 'irr_limit': %d, 'irr_duration': %d }, 'irr_timer': %d, 'ph_timer': %d, 'light_timer': %d, 'tmp_timer': %d } ",
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
    
    sprintf(topic, STATUS);
    printf(" >  [%s] %s \n", topic, msg);

}

/*-------*/

void irrigation_sim(){

    char msg[100];
    char topic[50];

    sprintf(msg, "{ 'land_id': %d, 'node_id': %d, 'enabled': '%s', 'status': '%s', 'irr_limit': %d, 'irr_duration': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        node_memory.configuration.irr_config.enabled?"true":"false",
        node_memory.irr_status?"on":"off",
        node_memory.configuration.irr_config.irr_limit,
        node_memory.configuration.irr_config.irr_duration
        );
    sprintf(topic, IRRIGATION);
    printf(" >  [%s] %s \n", topic, msg);
}

/*-------*/

void is_alive_ack_sim(){

    char msg[50];
    char topic[50];
    sprintf(msg, "{ 'land_id': %d, 'node_id': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id
        );
    sprintf(topic, IS_ALIVE_ACK);
    printf(" >  [%s] %s \n", topic, msg);
}

/*-----------------SENSORS READINGS (SIMULATED)-------------------------------*/

void irr_stopping(){
    node_memory.irr_status = false;
    irrigation_sim();
}

void get_soil_moisture(){
    
    if(node_timers.sensor_timer_are_setted)
        ctimer_restart(&node_timers.mst_ctimer);

    short moisture = (15 + random_rand()%70);
    node_memory.measurements.soil_moisture = moisture;
    printf("[+] soil moisture detected: %d\n", moisture);

    char msg[100];
    char topic[50];
    sprintf(msg,"{ 'land_id': %d, 'node_id: %d, 'type': 'moisture', 'value': %d, 'timer': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        moisture,
        node_memory.configuration.mst_timer);
    sprintf(topic, MOISTURE);

    printf(" >  [%s] %s\n", topic, msg);

    if(moisture < node_memory.configuration.irr_config.irr_limit){
        node_memory.irr_status = true;
        int irr_duration = node_memory.configuration.irr_config.irr_duration;
        irrigation_sim();
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

    char msg[100];
    char topic[50];
    sprintf(msg,"{ 'land_id': %d, 'node_id: %d, 'type': 'ph', 'value': %d, 'timer': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        ph_level,
        node_memory.configuration.ph_timer);
    sprintf(topic, PH);
    printf(" >  [%s] %s\n", topic, msg);

}

/*--------*/

void get_lihght_raw(){

    if(node_timers.sensor_timer_are_setted)
        ctimer_restart(&node_timers.light_ctimer);

    int light = random_rand()%28;
    node_memory.measurements.light_raw =  light;
    printf("[+] light raw detected: %d\n", light);

    char msg[100];
    char topic[50];
    sprintf(msg,"{ 'land_id': %d, 'node_id: %d, 'type': 'light', 'value': %d, 'timer': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        light,
        node_memory.configuration.light_timer);
    sprintf(topic, LIGHT);
    printf(" >  [%s] %s\n", topic, msg);
} 

/*--------*/

void get_soil_tmp(){

    if(node_timers.sensor_timer_are_setted)
        ctimer_restart(&node_timers.tmp_ctimer);

    int tmp = (5 + random_rand()%35);
    node_memory.measurements.soil_temperature =  tmp;
    printf("[+] soil temperature detected: %d\n", tmp);

    char msg[100];
    char topic[50];
    sprintf(msg,"{ 'land_id': %d, 'node_id: %d, 'type': 'tmp', 'value': %d, 'timer': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        tmp,
        node_memory.configuration.mst_timer);
    sprintf(topic, TMP);
    printf(" >  [%s] %s\n", topic, msg);
}
/*-------------------------------------------------------------------*/

void receive_configuration(){

    char response[200];
    char topic[50];
    assign_config_received_sim(response, topic);
    printf(" <  [%s] %s \n", topic, response);
    elaborate_cmd(response, topic);
}


PROCESS(mqtt_node, "Mqtt node");
AUTOSTART_PROCESSES(&mqtt_node);

PROCESS_THREAD(mqtt_node, ev, data){
    
    static unsigned int btn_count;
    static bool led_status;
    static bool land_id_setted;

    PROCESS_BEGIN();

    /*------------INITIALIZATION---------------*/
    printf("[!] initialization ...\n");
    

    //set land_id

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

    printf("[+] land %d selected: \n", node_memory.configuration.land_id);
    printf("[+] id %d selected: \n", node_memory.configuration.node_id);


    printf("[!] intialization ended\n");

    /*---------------CONFIGURATION-------------------*/
    
    printf("[!] configuration ... \n");

    config_request_sim();
    receive_configuration();
    print_config();

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

    while(1){

        PROCESS_YIELD();

        //simulation of received command by server
        if(ev == serial_line_event_message){
            char * cmd = (char*)data;
            char msg[200];
            char topic[50];

            if(strcmp(cmd, "help") == 0){
                printf("[!] command list:\n");
                printf("    . irr_cmd\n");
                printf("    . get_config\n");
                printf("    . timer_cmd\n");
                printf("    . assign_config\n");
                printf("    . get_sensor\n");
                printf("    . is_alive\n");
                printf("---------------\n");
                continue;
            }
            else if(strcmp(cmd, "irr_cmd") == 0){
                irr_cmd_received_sim(msg, topic);
            }
            else if(strcmp(cmd, "get_config") == 0){
                get_config_received_sim(msg, topic);
            }
            else if(strcmp(cmd, "timer_cmd") == 0){
                timer_cmd_received_sim(msg, topic);
            }
            else if(strcmp(cmd, "assign_config") == 0){
                assign_config_received_sim(msg, topic);
            }
            else if(strcmp(cmd, "get_sensor") == 0){
                get_sensor_received_sim(msg, topic);
            }
            else if(strcmp(cmd, "is_alive") == 0){
                is_alive_received_sim(msg, topic);
            }

            printf(" <  [%s] %s \n",topic, msg);

            elaborate_cmd(msg, topic);

            
        }
    }



    /*---------------------------------------------*/


    PROCESS_END();
}
