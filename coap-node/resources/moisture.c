#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "coap-engine.h"

static void mst_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);

static void mst_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);

static void mst_event_handler(void);

/*--------------------------------------------*/

EVENT_RESOURCE(
    mst_rsc,
    "title=\"Soil Moisture\"; rt = \"Text\"",
    mst_get_handler,
    NULL,
    mst_put_handler,
    NULL,
    mst_event_handler
)

/*--------------------------------------------*/

void get_soil_moisture(char msg[]){
    
    if(node_timers.sensor_timer_are_setted)
        ctimer_restart(&node_timers.mst_ctimer);

    short moisture = (15 + random_rand()%50);
    node_memory.measurements.soil_moisture = moisture;
    printf("[+] soil moisture detected: %d\n", moisture);

    sprintf(msg,"{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d, \"value\": %d } }",
        MOISTURE,
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        moisture);

    printf(" >  %s\n", msg);

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

/*------------------------------------------*/

static void mst_event_handler(void)
{
  coap_notify_observers(&mst_rsc);
}

/*----------------------------------------------*/


static void mst_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

    char msg[MSG_SIZE];
    get_soil_moisture(msg); 
    coap_set_header_content_format(response, TEXT_PLAIN);
    coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", msg));
}

/*--------------------------------------------*/

static void mst_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

    const char msg[MSG_SIZE];
    char reply[MSG_SIZE];
    int len = coap_get_post_variable(request, "value", &msg);
    printf("[!] MST_CMD command elaboration ...\n");
    
    int n_arguments = 3;
    char arguments[n_arguments][100];
    parse_json(msg, n_arguments, arguments);
        
    node_memory.configuration.mst_timer = atoi(arguments[2]);
    ctimer_set(&node_timers.mst_ctimer, node_memory.configuration.mst_timer * CLOCK_MINUTE, get_soil_moisture, NULL);

    send_status(reply) //TODO
    printf("[+] MST_CMD command elaborated with success\n");
    
    coap_set_header_content_format(response, TEXT_PLAIN);
    coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));
}