#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "coap-engine.h"

static void light_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);

static void light_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);

static void light_event_handler(void);

/*--------------------------------------------*/

EVENT_RESOURCE(
    light_rsc,
    "title=\"Light\"; rt = \"Text\"",
    light_get_handler,
    NULL,
    light_put_handler,
    NULL,
    light_event_handler
)

/*-----------------------------------------*/

void get_lihght_raw(char msg[]){

    if(node_timers.sensor_timer_are_setted)
        ctimer_restart(&node_timers.light_ctimer);

    int light = random_rand()%28;
    node_memory.measurements.light_raw =  light;
    printf("[+] light raw detected: %d\n", light);

    sprintf(msg,"{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d, \"value\": %d } }",
        LIGHT,
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        light
        );
    printf(" >  %s\n", msg);
} 

/*------------------------------------------*/

static void light_event_handler(void)
{
  coap_notify_observers(&light_rsc);
}

/*----------------------------------------------*/


static void light_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

    char msg[MSG_SIZE];
    get_lihght_raw(msg); 
    coap_set_header_content_format(response, TEXT_PLAIN);
    coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", msg));
}

/*-------------------------------------------*/

static void light_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

    const char msg[MSG_SIZE];
    char reply[MSG_SIZE];
    int len = coap_get_post_variable(request, "value", &msg);
    printf("[!] LIGHT_CMD command elaboration ...\n");
    
    int n_arguments = 3;
    char arguments[n_arguments][100];
    parse_json(msg, n_arguments, arguments);
  
    node_memory.configuration.light_timer = atoi(arguments[2]);
    ctimer_set(&node_timers.light_ctimer, node_memory.configuration.light_timer * CLOCK_MINUTE, get_lihght_raw, NULL);
    
    send_status(reply); //TODO
    printf("[+] LIGHT_CMD command elaborated with success\n");
    
    coap_set_header_content_format(response, TEXT_PLAIN);
    coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));
}
