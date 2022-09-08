#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "coap-engine.h"
#include "coap-node.h"

static void config_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);

static void config_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);

static void config_del_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);
/*--------------------------------------------*/

EVENT_RESOURCE(
    config_rsc,
    "title=\"Configuration\"; rt = \"Text\"",
    config_get_handler,
    NULL,
    config_put_handler,
    config_del_handler,
    NULL
);

/*--------------------------------------*/

void send_status(char msg[]){

    sprintf(msg, "{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d, \"irr_config\": { \"enabled\": \"%s\", \"irr_limit\": %d, \"irr_duration\": %d }, \"mst_timer\": %d, \"ph_timer\": %d, \"light_timer\": %d, \"tmp_timer\": %d } } ",
        STATUS,
        node_memory.configuration.land_id,
        node_memory.configuration.node_id,
        node_memory.configuration.irr_config.enabled?"true":"false",
        node_memory.configuration.irr_config.irr_limit,
        node_memory.configuration.irr_config.irr_duration,
        node_memory.configuration.mst_timer,
        node_memory.configuration.ph_timer,
        node_memory.configuration.light_timer,
        node_memory.configuration.tmp_timer
        );
    
    printf(" >  %s \n", msg);
}

/*----------------------------------------------*/


static void config_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

    char msg[MSG_SIZE];
    send_status(msg); 
    coap_set_header_content_format(response, TEXT_PLAIN);
    coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", msg));
}

/*----------------------------------------------------------*/

void assign_config(char msg[]){

  printf("[!] ASSIGN_CONFIG command elaboration ...\n");

  int n_arguments = 8; 
  char arguments[n_arguments][100];
  parse_json(msg, n_arguments, arguments );

  node_memory.configuration.irr_config.enabled = arguments[1];
  node_memory.configuration.irr_config.irr_limit = atoi(arguments[2]);
  node_memory.configuration.irr_config.irr_duration = atoi(arguments[3]);
  node_memory.configuration.mst_timer = atoi(arguments[4]);
  node_memory.configuration.ph_timer = atoi(arguments[5]);
  node_memory.configuration.light_timer = atoi(arguments[6]);
  node_memory.configuration.tmp_timer = atoi(arguments[7]);

  printf("[+] ASSIGN_CONFIG command elaborated with success\n");
  
}

static void config_put_handler(
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
      printf("[-] no argument obteined from put request of config_rsc");
      return;
    }
    sprintf(msg, "%s", (char*)arg);
    
    assign_config(msg);
    send_status(reply);

    coap_set_header_content_format(response, TEXT_PLAIN);
    coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));
}

/*----------------------------------------------*/


static void config_del_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

    printf("[!] ERROR_LAND received, reset the node\n");
    process_exit(&coap_node);
}