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

/*-------------------------------------------------------------------*/

PROCESS(mqtt_node, "Mqtt node");
AUTOSTART_PROCESSES(&mqtt_node);

PROCESS_THREAD(mqtt_node, ev, data){

    static struct etimer btn_timer;
    static struct etimer led_timer;
    static unsigned int btn_count;
    static bool led_status;
    static bool land_id_setted;

    PROCESS_BEGIN();

    /*------------INITIALIZATION---------------*/
    printf("[!] initialization ...\n");
    

    //set land_id

    printf("[!] manual led_id setting\n");

    etimer_set(&led_timer,0.5 * CLOCK_SECOND);
    btn_count = 0;
    led_status = false;
    leds_single_off(LEDS_RED);
    land_id_setted = false;

    while(1){
        PROCESS_YIELD();

        if(ev == PROCESS_EVENT_TIMER){
            if(etimer_expired(&led_timer)){
                led_status = !led_status;
                leds_single_toggle(LEDS_RED);
                etimer_restart(&led_timer);
            }

            if(btn_count > 0 && etimer_expired(&btn_timer)){
                if(!land_id_setted){
                    node_memory.configuration.land_id = btn_count;
                    land_id_setted = true;
                    leds_single_on(LEDS_RED);
                    led_status = true;
                    etimer_reset_with_new_interval(&led_timer, 2 * CLOCK_SECOND);
                    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&led_timer));
                    etimer_reset_with_new_interval(&led_timer, 0.5 * CLOCK_SECOND);
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
                    etimer_reset_with_new_interval(&led_timer, 2 * CLOCK_SECOND);
                    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&led_timer));
                    etimer_reset_with_new_interval(&led_timer, 0.5 * CLOCK_SECOND);
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
                etimer_set(&btn_timer, 3 * CLOCK_SECOND);
            else    
                etimer_restart(&btn_timer);
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

    printf("[+] configuration ended");
    PROCESS_END();
}
