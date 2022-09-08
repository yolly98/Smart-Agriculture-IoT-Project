#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "coap-engine.h"

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


struct configuration_str{

    unsigned int land_id;
    unsigned int node_id;
} configuration;


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

    sprintf(msg, "{ \"cmd\": \"%s\", \"body\": { \"land_id\": %d, \"node_id\": %d } } ",
        "config-status",
        configuration.land_id,
        configuration.node_id
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

  int n_arguments = 2; 
  char arguments[n_arguments][100];
  parse_json(msg, n_arguments, arguments );

  configuration.land_id = arguments[0];
  configuration.node_id = arguments[1];
  
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