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

void get_config(){

    node_memory.configuration.irr_config.enabled = true;
    node_memory.configuration.irr_config.irr_limit = 22;
    node_memory.configuration.irr_config.irr_duration = 10;

    node_memory.configuration.mst_timer = 720;
    node_memory.configuration.ph_timer = 720;
    node_memory.configuration.light_timer = 60;
    node_memory.configuration.tmp_timer = 60;

}

/*-----------------SENSORS SIMULATED-------------------------------*/

void get_soil_moisture(){

    short moisture = (15 + random_rand()%70);
    node_memory.measurements.soil_moisture = moisture;
    printf("[+] soil moisture detected: %d\n", moisture);

    char msg[100];
    sprintf(msg,"{ 'land_id': %d, 'node_id: %d, 'type': 'moisture', 'value': %d, 'timer': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        moisture,
        node_memory.configuration.mst_timer);
    printf("[!] sending on topic = MOISTURE ...\n");
    printf("[+] > %s\n", msg);
}

void get_ph_level(){

    short ph_level = (5 + random_rand()%5);
    node_memory.measurements.ph_level =  ph_level;
    printf("[+] ph level detected: %d\n", ph_level);

    char msg[100];
    sprintf(msg,"{ 'land_id': %d, 'node_id: %d, 'type': 'ph', 'value': %d, 'timer': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        ph_level,
        node_memory.configuration.ph_timer);
    printf("[!] sending on topic = PH ...\n");
    printf("[+] > %s\n", msg);
}

void get_lihght_raw(){

    int light = random_rand()%28;
    node_memory.measurements.light_raw =  light;
    printf("[+] light raw detected: %d\n", light);

    char msg[100];
    sprintf(msg,"{ 'land_id': %d, 'node_id: %d, 'type': 'light', 'value': %d, 'timer': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        light,
        node_memory.configuration.light_timer);
    printf("[!] sending on topic = LIGHT ...\n");
    printf("[+] > %s\n", msg);
} 

void get_soil_tmp(){

    int tmp = (5 + random_rand()%35);
    node_memory.measurements.soil_temperature =  tmp;
    printf("[+] soil temperature detected: %d\n", tmp);

    char msg[100];
    sprintf(msg,"{ 'land_id': %d, 'node_id: %d, 'type': 'tmp', 'value': %d, 'timer': %d }",
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        tmp,
        node_memory.configuration.mst_timer);
    printf("[!] sending on topic = TMP ...\n");
    printf("[+] > %s\n", msg);
}
/*-------------------------------------------------------------------*/

PROCESS(mqtt_node, "Mqtt node");
AUTOSTART_PROCESSES(&mqtt_node);

PROCESS_THREAD(mqtt_node, ev, data){

    static struct etimer btn_etimer;
    static struct etimer led_etimer;
    static struct ctimer mst_ctimer;
    static struct ctimer ph_ctimer;
    static struct ctimer light_ctimer;
    static struct ctimer tmp_ctimer;
    static unsigned int btn_count;
    static bool led_status;
    static bool land_id_setted;

    PROCESS_BEGIN();

    /*------------INITIALIZATION---------------*/
    printf("[!] initialization ...\n");
    

    //set land_id

    printf("[!] manual led_id setting\n");

    etimer_set(&led_etimer,0.5 * CLOCK_SECOND);
    btn_count = 0;
    led_status = false;
    leds_single_off(LEDS_RED);
    land_id_setted = false;

    while(1){
        PROCESS_YIELD();

        if(ev == PROCESS_EVENT_TIMER){
            if(etimer_expired(&led_etimer)){
                led_status = !led_status;
                leds_single_toggle(LEDS_RED);
                etimer_restart(&led_etimer);
            }

            if(btn_count > 0 && etimer_expired(&btn_etimer)){
                if(!land_id_setted){
                    node_memory.configuration.land_id = btn_count;
                    land_id_setted = true;
                    leds_single_on(LEDS_RED);
                    led_status = true;
                    etimer_reset_with_new_interval(&led_etimer, 2 * CLOCK_SECOND);
                    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&led_etimer));
                    etimer_reset_with_new_interval(&led_etimer, 0.5 * CLOCK_SECOND);
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
                    etimer_reset_with_new_interval(&led_etimer, 2 * CLOCK_SECOND);
                    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&led_etimer));
                    etimer_reset_with_new_interval(&led_etimer, 0.5 * CLOCK_SECOND);
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
                etimer_set(&btn_etimer, 3 * CLOCK_SECOND);
            else    
                etimer_restart(&btn_etimer);
        }

        
    }

    leds_single_off(LEDS_RED);
    led_status = false;

    printf("[+] land %d selected: \n", node_memory.configuration.land_id);
    printf("[+] id %d selected: \n", node_memory.configuration.node_id);


    printf("[!] intialization ended\n");

    /*---------------CONFIGURATION-------------------*/
    
    printf("[!] configuration ... ");

    get_config();
    print_config();

    printf("[+] configuration ended\n");

    /*------------------FIRST MEASUREMENTS------------*/


    printf("[!] first sensor detection ...\n");
    get_soil_moisture();
    get_ph_level();
    get_lihght_raw();
    get_soil_tmp();

    ctimer_set(&mst_ctimer, node_memory.configuration.mst_timer * CLOCK_MINUTE, get_soil_moisture, NULL);
    ctimer_set(&ph_ctimer, node_memory.configuration.ph_timer * CLOCK_MINUTE, get_ph_level, NULL);
    ctimer_set(&light_ctimer, node_memory.configuration.light_timer * CLOCK_MINUTE, get_lihght_raw, NULL);
    ctimer_set(&tmp_ctimer, node_memory.configuration.tmp_timer * CLOCK_MINUTE, get_soil_tmp, NULL);


    /*---------------NORMAL WORKLOAD----------------*/

    while(1){

        PROCESS_YIELD();
        if(ev == serial_line_event_message){
            char * msg = (char*)data;
            printf("[!] recevived '%s' by serial\n", msg);
        }
    }



    /*---------------------------------------------*/


    PROCESS_END();
}
