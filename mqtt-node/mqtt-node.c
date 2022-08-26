#include "mqtt-node.h"


/*----------------------------------------------------------------------*/


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

/*------------------------------------------------------------------*/

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

/*----------------------------------------------*/

void parse_json(char json[], int n_arguments, char arguments[][100]){

    int value_parsed = 0;
    int len = 0;
    bool value_detected = false;

    for(int i = 0; i< 500; i++){
        
        if(json[i] == ':'){
            i++; //there is the space after ':'
            value_detected = true;
            len = 0;
        }
        else if(value_detected && (json[i] == ',' || json[i] == ' ' || json[i] == '}')){
            value_detected = false;
            arguments[value_parsed][len + 1] = '\0';
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
        else if(json[i] == '\0')
            break;

    }

}

/*----------------------------------------------------------*/

void received_config_sim(char response[], char topic[]){ //is a simulation of a message received from server

    sprintf(response, "{ 'land_id': %d, 'node_id': %d, 'irr_config': { 'enabled': 'true', 'irr_limit': 22, 'irr_duration': 20 }, 'irr_timer': 720, 'ph_timer': 720, 'light_timer': 60, 'tmp_timer': 60 } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id
        );
    
    sprintf(topic, "ASSIGN_CONFIG");
}

bool get_config(){

    char response[500];
    char topic[100];
    received_config_sim(response, topic);
    printf(" <  [%s] %s \n", topic, response);


    if(strcmp(topic, "ASSIGN_CONFIG")!=0){
        printf("[-] topic received not correct (%s)\n", topic);
        return false;
    }

    int n_arguments = 9; 
    char arguments[n_arguments][100];

    parse_json(response, n_arguments, arguments );

    if(node_memory.configuration.land_id != atoi(arguments[0]) && node_memory.configuration.node_id != atoi(arguments[1])){
        printf("[-] this configuration is not for this board (%s, %s)\n", arguments[0], arguments[1]);
        return false;
    }

    node_memory.configuration.irr_config.enabled = arguments[2];
    node_memory.configuration.irr_config.irr_limit = atoi(arguments[3]);
    node_memory.configuration.irr_config.irr_duration = atoi(arguments[4]);

    node_memory.configuration.mst_timer = atoi(arguments[5]);
    node_memory.configuration.ph_timer = atoi(arguments[6]);
    node_memory.configuration.light_timer = atoi(arguments[7]);
    node_memory.configuration.tmp_timer = atoi(arguments[8]);

    return true;
}

/*-----------------COMMAND ELABORATOR----------------------------*/

//TODO parsing of the json received message
bool elaborate_cmd(char msg[], char topic[]){ 
    
    if(strcmp(topic, "IRR_CMD") == 0){
        printf("IRR_CMD command elaboration ...\n");

        int n_arguments = 6;
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments);
        if(node_memory.configuration.land_id != atoi(arguments[0]) && node_memory.configuration.node_id != atoi(arguments[1])){
            printf("[-] this configuration is not for this board (%s, %s)\n", arguments[0], arguments[1]);
            return false;
        }

        printf("------------\n");

    }
    else if(strcmp(topic, "GET_CONFIG") == 0){
        printf("GET_CONFIG command elaboration ...\n");
        
        int n_arguments = 2;
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments);
        if(node_memory.configuration.land_id != atoi(arguments[0]) && node_memory.configuration.node_id != atoi(arguments[1])){
            printf("[-] this configuration is not for this board (%s, %s)\n", arguments[0], arguments[1]);
            return false;
        }
        
        printf("------------\n");
    }
    else if(strcmp(topic, "TIMER_CMD") == 0){
        printf("TIMER_CMD command elaboration ...\n");
        
        int n_arguments = 4;
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments);
        if(node_memory.configuration.land_id != atoi(arguments[0]) && node_memory.configuration.node_id != atoi(arguments[1])){
            printf("[-] this configuration is not for this board (%s, %s)\n", arguments[0], arguments[1]);
            return false;
        }
        
        printf("------------\n");
    }
    else if(strcmp(topic, "ASSIGN_CONFIG") == 0){
        printf("ASSIGN_CONFIG command elaboration ...\n");
        
        int n_arguments = 9;
        char arguments[n_arguments][100];
        parse_json(msg, n_arguments, arguments);
        if(node_memory.configuration.land_id != atoi(arguments[0]) && node_memory.configuration.node_id != atoi(arguments[1])){
            printf("[-] this configuration is not for this board (%s, %s)\n", arguments[0], arguments[1]);
            return false;
        }
        
        printf("------------\n");
    }
    else{
        printf("[-] topic received not correct (%s)\n", topic);
        return false;
    }


    return true;

}

/*-----------------COMMAND SIMULATED-----------------------------*/

void irr_cmd_received_sim(char msg[], char topic[]){

    sprintf(topic, "IRR_CMD");
    sprintf(msg, "{ 'land_id': %d, 'node_id': %d, 'enable': '%s', 'status': '%s', 'limit': %d, 'irr_duration': %d } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        ((random_rand()%2)!=0)?(((random_rand()%2)!=0)?"true":"false"):"null",
        ((random_rand()%2)!=0)?(((random_rand()%2)!=0)?"on":"off"):"null",
        ((random_rand()%2)!=0)?(10 + random_rand()%30):0,
        ((random_rand()%2)!=0)?(5+ random_rand()%30):0
        );

}

void get_config_received_sim(char msg[], char topic[]){

    sprintf(topic, "GET_CONFIG");
    sprintf(msg, "{ 'land_id': %d, 'node_id': %d } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id);
}

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

    sprintf(topic, "TIMER_CMD");
    sprintf(msg, "{ 'land_id': %d, 'node_id': %d, 'sensor': '%s', 'timer': %d } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        sensor,
        20 + random_rand()%690
        );
}


/*-----------------SENSORS SIMULATED-------------------------------*/

void get_soil_moisture(){
    
    if(node_timers.areSetted)
        ctimer_restart(&node_timers.mst_ctimer);

    short moisture = (15 + random_rand()%70);
    node_memory.measurements.soil_moisture = moisture;
    printf("[+] soil moisture detected: %d\n", moisture);

    char msg[100];
    sprintf(msg,"[MOISTURE] { 'land_id': %d, 'node_id: %d, 'type': 'moisture', 'value': %d, 'timer': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        moisture,
        node_memory.configuration.mst_timer);
    printf(" >  %s\n", msg);

}

void get_ph_level(){

    if(node_timers.areSetted)
        ctimer_restart(&node_timers.ph_ctimer);

    short ph_level = (5 + random_rand()%5);
    node_memory.measurements.ph_level =  ph_level;
    printf("[+] ph level detected: %d\n", ph_level);

    char msg[100];
    sprintf(msg,"[PH] { 'land_id': %d, 'node_id: %d, 'type': 'ph', 'value': %d, 'timer': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        ph_level,
        node_memory.configuration.ph_timer);
    printf(" >  %s\n", msg);

}

void get_lihght_raw(){

    if(node_timers.areSetted)
        ctimer_restart(&node_timers.light_ctimer);

    int light = random_rand()%28;
    node_memory.measurements.light_raw =  light;
    printf("[+] light raw detected: %d\n", light);

    char msg[100];
    sprintf(msg,"[LIGHT] { 'land_id': %d, 'node_id: %d, 'type': 'light', 'value': %d, 'timer': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        light,
        node_memory.configuration.light_timer);
    printf(" >  %s\n", msg);
} 

void get_soil_tmp(){

    if(node_timers.areSetted)
        ctimer_restart(&node_timers.tmp_ctimer);

    int tmp = (5 + random_rand()%35);
    node_memory.measurements.soil_temperature =  tmp;
    printf("[+] soil temperature detected: %d\n", tmp);

    char msg[100];
    sprintf(msg,"[TMP] { 'land_id': %d, 'node_id: %d, 'type': 'tmp', 'value': %d, 'timer': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        tmp,
        node_memory.configuration.mst_timer);
    printf(" >  %s\n", msg);
}
/*-------------------------------------------------------------------*/

PROCESS(mqtt_node, "Mqtt node");
AUTOSTART_PROCESSES(&mqtt_node);

PROCESS_THREAD(mqtt_node, ev, data){

    static struct etimer cmd_sim_etimer;
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

    char request[100];
    sprintf(request, "[CONFIG_RQST] { 'land_id': %d, 'node_id': %d } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id
        );
    printf(" >  %s \n", request);

    get_config();
    print_config();

    printf("[+] configuration ended\n");

    /*------------------FIRST MEASUREMENTS------------*/


    printf("[!] first sensor detection ...\n");

    node_timers.areSetted = false;
    get_soil_moisture();
    get_ph_level();
    get_lihght_raw();
    get_soil_tmp();

    ctimer_set(&node_timers.mst_ctimer, node_memory.configuration.mst_timer * CLOCK_MINUTE, get_soil_moisture, NULL);
    ctimer_set(&node_timers.ph_ctimer, node_memory.configuration.ph_timer * CLOCK_MINUTE, get_ph_level, NULL);
    ctimer_set(&node_timers.light_ctimer, node_memory.configuration.light_timer * CLOCK_MINUTE, get_lihght_raw, NULL);
    ctimer_set(&node_timers.tmp_ctimer, node_memory.configuration.tmp_timer * CLOCK_MINUTE, get_soil_tmp, NULL);

    node_timers.areSetted = true;

    /*---------------NORMAL WORKLOAD----------------*/

    etimer_set(&cmd_sim_etimer, 5*CLOCK_SECOND);
    while(1){

        PROCESS_YIELD();

        //simulation of received command by server
        if(ev == PROCESS_EVENT_TIMER){
            if(etimer_expired(&cmd_sim_etimer)){
                char msg[200];
                char topic[50];
                
                int cmd = random_rand()%4;
                if(cmd == 0)
                    irr_cmd_received_sim(msg, topic);
                else if(cmd == 1)
                    get_config_received_sim(msg, topic);
                else if(cmd == 2)
                    timer_cmd_received_sim(msg, topic);
                else
                    received_config_sim(msg, topic);
            
                printf(" <  [%s] %s \n",topic, msg);

                elaborate_cmd(msg, topic);

                etimer_restart(&cmd_sim_etimer);
            }
        }
    }



    /*---------------------------------------------*/


    PROCESS_END();
}
