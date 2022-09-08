#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "coap-engine.h"
#include "coap-node.h"

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

static struct light_str{
  unsigned int light_raw;
  unsigned int light_timer;
  struct etimer light_etimer;
}light_mem;

EVENT_RESOURCE(
    light_rsc,
    "title=\"Light\"; rt = \"Text\"",
    light_get_handler,
    NULL,
    light_put_handler,
    NULL,
    light_event_handler
);

/*-----------------------------------------*/

void send_light_raw(char msg[]){

    etimer_set(&light_mem.light_etimer, light_mem.light_timer * CLOCK_MINUTE);

    int light = random_rand()%28;
    light_mem.light_raw =  light;
    printf("[+] light raw detected: %d\n", light);

    sprintf(msg,"{ \"cmd\": \"%s\", \"value\": %d }",
        "light",
        light_mem.light_raw
        );
    printf(" >  %s\n", msg);
} 

/*------------------------------------------*/

void send_light_status(char msg[]){
  sprintf(msg,"{ \"cmd\": \"%s\", \"timer\": %d }",
      "light-status",
      light_mem.light_timer
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

  const char* value;
  char msg[MSG_SIZE];
  char reply[MSG_SIZE];

  int len = coap_get_query_variable(request, "value", value);
  sprintf(msg, "%s", (char*)value);
  if(len == 0)
    send_light_raw(reply);
  else if(len > 0 and strcmp(value, "status") == 0)
    send_light_status(reply)
  else{
    printf("[-] error unknown in get light sensor");
    return;
  } 

  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));
}

/*-------------------------------------------*/

static void light_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

  const char *arg;
  char msg[MSG_SIZE];
  char reply[MSG_SIZE];
  int len = coap_get_post_variable(request, "value", &arg);
  if (len <= 0){
    printf("[-] no argument obteined from put request of light_rsc");
    return;
  }
  sprintf(msg, "%s", (char*)arg);    
  light_mem.light_timer = atoi(msg);
  //ctimer_set(&node_timers.light_ctimer, node_memory.configuration.light_timer * CLOCK_MINUTE, send_light_raw, NULL);
  etimer_set(&light_mem.light_etimer, light_mem.light_timer * CLOCK_MINUTE);
  send_light_status(reply); 
  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));
}
