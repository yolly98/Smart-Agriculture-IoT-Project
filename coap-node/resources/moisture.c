#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "coap-engine.h"
#include "coap-node.h"

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
static struct mst_str{
  unsigned int soil_moisture;
  unsigned int mst_timer;
  struct etimer mst_etimer;
}mst_mem;

EVENT_RESOURCE(
    mst_rsc,
    "title=\"Soil Moisture\"; rt = \"Text\"",
    mst_get_handler,
    NULL,
    mst_put_handler,
    NULL,
    mst_event_handler
);

/*--------------------------------------------*/

void send_soil_moisture(char msg[]){
    
    etimer_set(&mst_mem.mst_etimer, mst_mem.mst_timer * CLOCK_MINUTE);

    int moisture = (15 + random_rand()%50);
    mst_mem.soil_moisture = moisture;
    printf("[+] soil moisture detected: %d\n", moisture);

    sprintf(msg,"{ \"cmd\": \"%s\", \"value\": %d }".
        "mst",
        mst_mem.soil_moisture
      );

    printf(" >  %s\n", msg);

  // TODO
  //  bool irr_enabled = node_memory.configuration.irr_config.enabled;
  //  int irr_limit = node_memory.configuration.irr_config.irr_limit;
  //  if( irr_enabled && moisture < irr_limit){
  //      node_memory.irr_status = true;
  //      int irr_duration = node_memory.configuration.irr_config.irr_duration;
  //      send_irrigation();
  //      if(!node_timers.irr_timer_is_setted){
  //          ctimer_set(&node_timers.irr_duration_ctimer, irr_duration * CLOCK_MINUTE, irr_stopping, NULL);
  //          node_timers.irr_timer_is_setted = true;
  //      }
  //      else
  //          ctimer_restart(&node_timers.irr_duration_ctimer);
  //  }

}

/*------------------------------------------*/

void send_mst_status(char msg[]){
  sprintf(msg,"{ \"cmd\": \"%s\", \"timer\": %d }",
      "mst-status",
      mst_mem.mst_timer
      );
  printf(" >  %s\n", msg);
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

  const char* value;
  char msg[MSG_SIZE];
  char reply[MSG_SIZE];

  int len = coap_get_query_variable(request, "value", value);
  sprintf(msg, "%s", (char*)value);
  if(len == 0)
    send_soil_moisture(reply);
  else if(len > 0 and strcmp(value, "status") == 0)
    send_mst_status(reply)
  else{
    printf("[-] error unknown in get moisture sensor");
    return;
  } 

  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));

}

/*--------------------------------------------*/

static void mst_put_handler(
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
    printf("[-] no argument obteined from put request of mst_rsc");
    return;
  }
  sprintf(msg, "%s", (char*)arg);
  mst_mem.mst_timer = atoi(msg);
  //ctimer_set(&node_timers.mst_ctimer, node_memory.configuration.mst_timer * CLOCK_MINUTE, send_soil_moisture, NULL);
  etimer_set(&mst_mem.mst_etimer, mst_mem.mst_timer * CLOCK_MINUTE);
  send_mst_status(reply) 
  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));
}