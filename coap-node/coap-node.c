#include "coap_module.c"

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

/*------------------------------------------------*/

void send_config_request(){

    char msg[MSG_SIZE];
    sprintf(msg, "{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d } }",
        CONFIG_RQST,
        node_memory.configuration.land_id,
        node_memory.configuration.node_id
        );
    printf(" >  %s \n", msg);
    coap_send(msg);
}

/*---------------*/

void irr_stopping(){
    node_memory.irr_status = false;
    irr_rsc.trigger();
}

/*-------------------------------------------------------*/

PROCESS_THREAD(coap_node, ev, data){
    
    static unsigned int btn_count;
    static bool led_status;
    static bool land_id_setted;

    PROCESS_BEGIN();

    /*------------INITIALIZATION---------------*/
    printf("[!] initialization ...\n");

    //set land_id and node_id

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

    coap_activate_resource(&config_rsc);
    coap_activate_resource(&irr_rsc);
    coap_activate_resource(&isalive_rsc);
    coap_activate_resource(&mst_rsc);
    coap_activate_resource(&ph_rsc);
    coap_activate_resource(&light_rsc);
    coap_activate_resource(&tmp_rsc);
    
    coap_init();
    /*---------------CONFIGURATION-------------------*/
    
    printf("[!] configuration ... \n");

    send_config_request();

    printf("[+] configuration ended\n");

    /*------------------FIRST MEASUREMENTS------------*/


    printf("[!] first sensor detection ...\n");

    node_timers.sensor_timer_are_setted = false;
    node_timers.irr_timer_is_setted = false;
    mst_rsc.trigger();
    ph_rsc.trigger();
    light_rsc.trigger();
    tmp_rsc.trigger();

    ctimer_set(&node_timers.mst_ctimer, node_memory.configuration.mst_timer * CLOCK_MINUTE, get_soil_moisture, NULL);
    ctimer_set(&node_timers.ph_ctimer, node_memory.configuration.ph_timer * CLOCK_MINUTE, get_ph_level, NULL);
    ctimer_set(&node_timers.light_ctimer, node_memory.configuration.light_timer * CLOCK_MINUTE, get_lihght_raw, NULL);
    ctimer_set(&node_timers.tmp_ctimer, node_memory.configuration.tmp_timer * CLOCK_MINUTE, get_soil_tmp, NULL);

    node_timers.sensor_timer_are_setted = true;


    while(true){

        PROCESS_YIELD();
        
        //if(!(NETSTACK_ROUTING.node_is_reachable() && NETSTACK_ROUTING.get_root_ipaddr(&mqtt_module.dest_ipaddr))){
        //    printf("the border router is not reachable yet\n");
        //}
    }

    PROCESS_END();
}
