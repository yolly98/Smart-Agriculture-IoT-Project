#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "coap-engine.h"

static void tmp_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);

static void tmp_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);

static void tmp_event_handler(void);

/*--------------------------------------------*/

EVENT_RESOURCE(
    tmp_rsc,
    "title=\"Soil Temperature\"; rt = \"Text\"",
    tmp_get_handler,
    NULL,
    tmp_put_handler,
    NULL,
    tmp_event_handler
)


/*----------------------------------*/

void get_soil_tmp(char msg[]){

    if(node_timers.sensor_timer_are_setted)
        ctimer_restart(&node_timers.tmp_ctimer);

    int tmp = (5 + random_rand()%35);
    node_memory.measurements.soil_temperature =  tmp;
    printf("[+] soil temperature detected: %d\n", tmp);

    sprintf(msg,"{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d, \"value\": %d } }",
        TMP,
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        tmp
        );
    printf(" >  %s\n", msg);
}

/*------------------------------------------*/

static void tmp_event_handler(void)
{
  coap_notify_observers(&tmp_rsc);
}

/*----------------------------------------------*/


static void tmp_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

    char msg[MSG_SIZE];
    get_soil_tmp(msg); 
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
    printf("[!] TMP_CMD command elaboration ...\n");
    
    int n_arguments = 3;
    char arguments[n_arguments][100];
    parse_json(msg, n_arguments, arguments);
  
    node_memory.configuration.tmp_timer = atoi(arguments[2]);
    ctimer_set(&node_timers.tmp_ctimer, node_memory.configuration.tmp_timer * CLOCK_MINUTE, get_soil_tmp, NULL);
    
    send_status(reply); //TODO
    printf("[+] TMP_CMD command elaborated with success\n");
    
    coap_set_header_content_format(response, TEXT_PLAIN);
    coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));
}