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

/*-------------------------------------------------------------------*/

PROCESS(mqtt_node, "Mqtt node");
AUTOSTART_PROCESSES(&mqtt_node);

PROCESS_THREAD(mqtt_node, ev, data){

    static struct etimer btn_timer;
    static struct etimer led_timer;
    static unsigned int btn_count;
    static bool led_status;

    PROCESS_BEGIN();

    /*------------INITIALIZATION---------------*/
    printf("initialization ...\n");
    
    etimer_set(&led_timer,0.5 * CLOCK_SECOND);
    btn_count = 0;
    led_status = false;
    leds_single_off(LEDS_RED);

    while(1){
        PROCESS_YIELD();

        if(ev == PROCESS_EVENT_TIMER){
            if(etimer_expired(&led_timer)){
                led_status = !led_status;
                leds_single_toggle(LEDS_RED);
                etimer_restart(&led_timer);
            }

            if(btn_count > 0 && etimer_expired(&btn_timer)){
                node_memory.configuration.land_id = btn_count;
                btn_count = 0;
                break;
            }
        }
        if(ev == serial_line_event_message){
            char * msg = (char*)data;
            printf("recevived '%s' by serial\n", msg);
            if(isNumber(msg)){
                node_memory.configuration.land_id = atoi(msg);
                break;
            }
            else    
                printf("[-] is not a number\n");
        }
        if(ev == button_hal_press_event){
            printf("button pressed\n");
            btn_count++;
            if(btn_count == 1)
                etimer_set(&btn_timer, 3 * CLOCK_SECOND);
            else    
                etimer_restart(&btn_timer);
        }

        
    }

    leds_single_off(LEDS_RED);
    led_status = false;


    printf("land %d selected\n", node_memory.configuration.land_id);

    printf("[!] intialization ended\n");
    /*-----------------------------------------*/

    PROCESS_END();
}
