#include "resource.h"

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
    NULL,
    NULL
);

/*--------------------------------------*/

void save_config(int land_id, int node_id){
  configuration.land_id = land_id;
  configuration.node_id = node_id;
}

void get_config(unsigned int* land_id,unsigned int* node_id){
  *land_id = configuration.land_id;
  *node_id = configuration.node_id;
}

/*--------------------------------------*/

void send_config_status(char msg[]){

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

    printf(" <  get config\n");
    char msg[MSG_SIZE];
    send_config_status(msg); 
    coap_set_header_content_format(response, TEXT_PLAIN);
    coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", msg));
}

/*----------------------------------------------------------*/


static void config_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

    printf(" <  put config\n");
    const uint8_t* arg;
    char msg[MSG_SIZE];
    char reply[MSG_SIZE];
    int len = coap_get_payload(request, &arg);
    if (len <= 0){
      printf("[-] no argument obteined from put request of config_rsc");
      return;
    }
    sprintf(msg, "%s", (char*)arg);
    
    int n_arguments = 2; 
    char arguments[n_arguments][100];
    parse_json(msg, n_arguments, arguments );
    save_config( atoi(arguments[0]),  atoi(arguments[1]));
    send_config_status(reply);

    coap_set_header_content_format(response, TEXT_PLAIN);
    coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));
}

/*----------------------------------------------*/


