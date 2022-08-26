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

void get_config_sim(){

    
    char response[500];
    sprintf(response, "[ASSIGN_CONFIG] { 'land_id': %d, 'node_id': %d, 'irr_config': { 'enabled': 'true', 'irr_limit': 22, 'irr_duration': 20 }, 'irr_timer': 720, 'ph_timer': 720, 'light_timer': 60, 'tmp_timer': 60 } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id
        );

    printf(" <  %s \n", response);

    //TODO parsing json received

    node_memory.configuration.irr_config.enabled = true;
    node_memory.configuration.irr_config.irr_limit = 22;
    node_memory.configuration.irr_config.irr_duration = 10;

    node_memory.configuration.mst_timer = 720;
    node_memory.configuration.ph_timer = 720;
    node_memory.configuration.light_timer = 60;
    node_memory.configuration.tmp_timer = 60;
}

/*-----------------COMMAND ELABORATOR----------------------------*/

//TODO parsing of the json received message
void elaborate_IRR_CMD(){ printf("[+] IRR_CMD elaborated\n");}

void elaborate_GET_CONFIG(){ printf("[+] GET_CONFIG elaborated\n");}

void elaborate_TIMER_CMD(){ printf("[+] TIMER_CMD elaborated\n");}

/*-----------------COMMAND SIMULATED-----------------------------*/

void irr_cmd_received_sim(char *msg){

    char buffer[200];
    sprintf(buffer, "[IRR_CMD] { 'land_id': %d, 'node_id': %d, 'enable': '%s', 'status': '%s', 'limit': %d, 'irr_duration': %d } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        ((random_rand()%2)!=0)?(((random_rand()%2)!=0)?"true":"false"):"null",
        ((random_rand()%2)!=0)?(((random_rand()%2)!=0)?"on":"off"):"null",
        ((random_rand()%2)!=0)?(10 + random_rand()%30):0,
        ((random_rand()%2)!=0)?(5+ random_rand()%30):0
        );

    strcpy(msg, buffer);

}

void get_config_received_sim(char *msg){

    char buffer[200];
    sprintf(buffer, "[GET_CONFIG] { 'land_id': %d, 'node_id': %d } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id);

    strcpy(msg, buffer);

}

void timer_cmd_received_sim(char *msg){

    char buffer[200];
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

    sprintf(buffer, "[TIMER_CMD] { 'land_id': %d, 'node_id': %d, 'sensor': '%s', 'timer': %d } ",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        sensor,
        20 + random_rand()%690
        );

    strcpy(msg, buffer);

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

    printf("[!] manual led_id setting\n");

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

    get_config_sim();
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
                char* msg = malloc(200);
                
                int cmd = random_rand()%3;
                if(cmd == 0)
                    irr_cmd_received_sim(msg);
                else if(cmd == 1)
                    get_config_received_sim(msg);
                else if(cmd == 2)
                    timer_cmd_received_sim(msg);
            
                printf(" <  %s \n",msg);

                char topic[50];
                for(int i = 1; i < 200 - 1 ; i++){
                    if(msg[i] == ']'){
                        topic[i-1] = '\0';
                        break;
                    }
                    topic[i - 1] = msg[i];
                }
                if(strcmp(topic, "IRR_CMD") == 0)
                    elaborate_IRR_CMD();
                else if(strcmp(topic, "GET_CONFIG") == 0)
                    elaborate_GET_CONFIG();
                else if(strcmp(topic, "TIMER_CMD") == 0)
                    elaborate_TIMER_CMD();
                else
                    printf("[-] invalid topic received (%s)\n", topic);

                etimer_restart(&cmd_sim_etimer);
            }
        }
    }



    /*---------------------------------------------*/


    PROCESS_END();
}
