#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "coap-engine.h"
#include "coap-node.h"

static void ph_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);

static void ph_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);

static void ph_event_handler(void);

/*--------------------------------------------*/

EVENT_RESOURCE(
    ph_rsc,
    "title=\"Ph\"; rt = \"Text\"",
    ph_get_handler,
    NULL,
    ph_put_handler,
    NULL,
    ph_event_handler
);

/*---------------------------------------*/

void get_ph_level(char msg[]){

    if(node_timers.sensor_timer_are_setted)
        ctimer_restart(&node_timers.ph_ctimer);

    short ph_level = (5 + random_rand()%5);
    node_memory.measurements.ph_level =  ph_level;
    printf("[+] ph level detected: %d\n", ph_level);

    sprintf(msg,"{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d, \"value\": %d } }",
        PH, 
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        ph_level
        );
    
    printf(" >  %s\n", msg);
}

/*------------------------------------------*/

static void ph_event_handler(void)
{
  coap_notify_observers(&ph_rsc);
}

/*----------------------------------------------*/


static void ph_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

    char msg[MSG_SIZE];
    get_ph_level(msg); 
    coap_set_header_content_format(response, TEXT_PLAIN);
    coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", msg));
}

/*-------------------------------------------------*/

static void ph_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

  const char* arg;
  char msg[MSG_SIZE];
  char reply[MSG_SIZE];
  int len = coap_get_post_variable(request, "value", &arg);
  if (len <= 0){
    printf("[-] no argument obteined from put request of ph_rsc");
    return;
  }
  sprintf(msg, "%s", (char*)arg);
  printf("[!] PH_CMD command elaboration ...\n");
  
  int n_arguments = 3;
  char arguments[n_arguments][100];
  parse_json(msg, n_arguments, arguments);

  node_memory.configuration.ph_timer = atoi(arguments[2]);
  ctimer_set(&node_timers.ph_ctimer, node_memory.configuration.ph_timer * CLOCK_MINUTE, get_ph_level, NULL);

  send_status(reply); //TODO
  printf("[+] PH_CMD command elaborated with success\n");
  
  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));
}
