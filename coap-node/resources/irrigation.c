#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "coap-engine.h"
#include "coap-node.h"

static void irr_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);

static void irr_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);

static void irr_event_handler(void);

/*--------------------------------------------*/

EVENT_RESOURCE(
    irr_rsc,
    "title=\"Irrigation\"; rt = \"Text\"",
    irr_get_handler,
    NULL,
    irr_put_handler,
    NULL,
    irr_event_handler
);

/*-----------------------------------------------*/

void send_irrigation(char msg[]){

    sprintf(msg, "{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d, \"status\": \"%s\" } }",
        IRRIGATION,
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        node_memory.irr_status?"on":"off"
        );
    printf(" >  %s \n", msg);
}

/*------------------------------------------*/

static void irr_event_handler(void)
{
  coap_notify_observers(&irr_rsc);
}

/*----------------------------------------------*/


static void irr_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

  char msg[MSG_SIZE];
  send_irrigation(msg); 
  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", msg));
}

/*----------------------------------------------*/

static void irr_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

  const char* arg:
  char msg[MSG_SIZE];
  char reply[MSG_SIZE];

  int len = coap_get_post_variable(request, "value", &arg);
  if (len <= 0){
    printf("[-] no argument obteined from put request of irr_rsc");
    return;
  }
  sprintf(msg, "%s", (char*)arg);
  

  printf("[!] IRR_CMD command elaboration ...\n");

  int n_arguments = 5;
  char arguments[n_arguments][100];
  parse_json(msg, n_arguments, arguments);

  if(strcmp(arguments[1], "null") != 0)
      node_memory.configuration.irr_config.enabled = ((strcmp(arguments[2], "true") == 0)?true:false);
  if(strcmp(arguments[2], "null") != 0)
      node_memory.irr_status = ((strcmp(arguments[3], "on") == 0)?true:false);
  if(isNumber(arguments[3]) && atoi(arguments[3]) != 0)
      node_memory.configuration.irr_config.irr_limit = atoi(arguments[3]);
  if(isNumber(arguments[4]) && atoi(arguments[4]) != 0)
      node_memory.configuration.irr_config.irr_duration = atoi(arguments[4]);

  send_irrigation(reply);
  printf("[+] IRR_CMD command elaborated with success\n");

  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));

}