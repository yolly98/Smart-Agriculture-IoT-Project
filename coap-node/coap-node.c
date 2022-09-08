#include "coap-node.h"

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

    unsigned int *land_id = NULL;
    unsigned int *node_id = NULL;
    bool *enabled = NULL;
    unsigned int *irr_limit = NULL;
    unsigned int *irr_duration = NULL;
    bool *status = NULL;
    unsigned int *mst_timer = NULL;
    unsigned int *ph_timer = NULL;
    unsigned int *light_timer = NULL;
    unsigned int *tmp_timer = NULL;

    get_config(land_id, node_id);
    get_irr_config(enabled, irr_limit, irr_duration, status);
    get_mst_timer(mst_timer);
    get_ph_timer(ph_timer);
    get_light_timer(light_timer);
    get_tmp_timer(tmp_timer);
    printf("[!] actual configuration: \n");
    printf("land_id: %d\n", *land_id);
    printf("node_id: %d\n", *node_id);
    printf("irr_config: { enabled: %s, irr_limit: %d, irr_duration: %d }\n",
        *enabled?"true":"false",
        *irr_limit,
        *irr_duration);
    printf("mst_timer: %d\n", *mst_timer);
    printf("ph_timer: %d\n", *ph_timer);
    printf("light_timer: %d\n", *light_timer);
    printf("tmp_timer: %d\n", *tmp_timer);
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

void send_config_request(char msg[]){

    unsigned int* land_id = NULL;
    unsigned int* node_id = NULL;
    get_config(land_id, node_id);
    sprintf(msg, "{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d } }",
        "config_rqst",
        *land_id,
        *node_id
        );
    printf(" >  %s \n", msg);
}

/*---------------------------------------*/

void coap_init(){

    coap_endpoint_parse(SERVER_EP, strlen(SERVER_EP), &coap_module.server_ep);
    coap_activate_resource(&config_rsc, "/configuration");
    coap_activate_resource(&irr_rsc, "/irrigation");
    coap_activate_resource(&is_alive_rsc, "/is_alive");
    coap_activate_resource(&mst_rsc, "/sensor/mst");
    coap_activate_resource(&ph_rsc, "/sensor/ph");
    coap_activate_resource(&light_rsc, "/sensor/light");
    coap_activate_resource(&tmp_rsc, "/sensor/tmp");
    STATE = STATE_INITIALIZED;
}

/*-----------------------------------------*/

void client_chunk_handler(coap_message_t *response){

    const uint8_t *chunk;

    if(response == NULL) {
        puts("Request timed out");
        return;
    }

    int len = coap_get_payload(response, &chunk);
    char msg[MSG_SIZE];
    sprintf(msg,"%s",chunk);
    
    printf("[!] ASSIGN_CONFIG command elaboration ...\n");
    STATE = STATE_CONFIGURED;
    int n_arguments = 9; 
    char arguments[n_arguments][100];
    parse_json(msg, n_arguments, arguments );

    bool enabled = (strcmp(arguments[2], "true") == 0)?true:false;
    int irr_limit = atoi(arguments[3]);
    int irr_duration = atoi(arguments[4]);
    int mst_timer = atoi(arguments[5]);
    int ph_timer = atoi(arguments[6]);
    int light_timer = atoi(arguments[7]);
    int tmp_timer = atoi(arguments[8]);

    save_irr_config(enabled, irr_limit, irr_duration, false);
    save_mst_timer(mst_timer);
    save_ph_timer(ph_timer);
    save_light_timer(light_timer);
    save_tmp_timer(tmp_timer);

    printf("[+] ASSIGN_CONFIG command elaborated with success\n");

    config_rsc.trigger();
    printf(" <  %.*s", len, (char *)chunk);
}

/*-------------------------------------------------------*/

PROCESS_THREAD(coap_node, ev, data){
    
    static unsigned int btn_count;
    static bool led_status;
    static bool land_id_setted;
    static int land_id;
    static int node_id;

    PROCESS_BEGIN();

    /*------------INITIALIZATION---------------*/
    printf("[!] initialization ...\n");

    //set land_id and node_id

    printf("[!] manual land_id setting\n");

    etimer_set(&led_etimer,0.5 * CLOCK_SECOND);
    btn_count = 0;
    led_status = false;
    leds_single_off(LEDS_RED);
    land_id_setted = false;
    land_id = 0;
    node_id = 0;

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
                    land_id = btn_count;
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
                    node_id = btn_count;
                    break;
                }
                
            }
        }
        if(ev == serial_line_event_message){
            char * msg = (char*)data;
            printf("[!] recevived '%s' by serial\n", msg);
            if(isNumber(msg) && atoi(msg) > 0){
               if(!land_id_setted){
                    land_id = atoi(msg);
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
                    node_id = atoi(msg);
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

    printf("[+] land %d selected: \n", land_id);
    printf("[+] id %d selected: \n", node_id);

    save_config(0, node_id); //TODO mettere land_id al posto dello 0
    
    printf("[!] intialization ended\n");
    coap_init();
    /*---------------CONFIGURATION-------------------*/
    
    printf("[!] configuration ... \n");

    char msg[MSG_SIZE];
    coap_init_message(coap_module.request, COAP_TYPE_CON, COAP_POST, 0);
    coap_set_header_uri_path(coap_module.request, "/new_config");
    coap_set_payload(coap_module.request, (uint8_t *)msg, strlen(msg) - 1);

    while(true){
        
        COAP_BLOCKING_REQUEST(&coap_module.server_ep, coap_module.request, client_chunk_handler);
        if(STATE == STATE_CONFIGURED)
            break;
    }
    print_config();
    printf("[+] configuration ended\n");

    /*------------------FIRST MEASUREMENTS------------*/


    printf("[!] first sensor detection ...\n");

    mst_rsc.trigger();
    ph_rsc.trigger();
    light_rsc.trigger();
    tmp_rsc.trigger();

    set_mst_timer();
    set_ph_timer();
    set_light_timer();
    set_tmp_timer();

    while(true){

        PROCESS_YIELD();
        
        //if(!(NETSTACK_ROUTING.node_is_reachable() && NETSTACK_ROUTING.get_root_ipaddr(&mqtt_module.dest_ipaddr))){
        //    printf("the border router is not reachable yet\n");
        //}
        if(check_mst_timer_expired()){
            mst_rsc.trigger();
            set_mst_timer();
            int moisture = get_mst_value(); //TODO
            irr_starting(moisture);
        }

        if(check_ph_timer_expired()){
            ph_rsc.trigger();
            set_ph_timer();
        }

        if(check_light_timer_expired()){
            light_rsc.trigger();
            set_light_timer();
        }

        if(check_tmp_timer_expired()){
            tmp_rsc.trigger();
            set_tmp_timer();
        }

        if(check_irr_timer_expired())
            irr_stopping();
    }

    PROCESS_END();
}
