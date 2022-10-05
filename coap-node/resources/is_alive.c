#include "resource.h"

static void is_alive_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
);

/*--------------------------------------------*/

int is_alive_state;

EVENT_RESOURCE(
    is_alive_rsc,
    "title=\"Is Alive\"; rt = \"Text\"",
    is_alive_get_handler,
    NULL,
    NULL,
    NULL,
    NULL
);

/*------------------------------------------------*/

void is_alive_init(){
  is_alive_state = STATE_CONFIGURED;
}

void is_alive_error(){
  is_alive_state = STATE_ERROR;
}

void send_is_alive_ack(char msg[]){

    sprintf(msg, "{ \"cmd\": \"%s\" }", "is_alive_ack");  
    printf(" >  %s \n", msg);
}

/*----------------------------------------------*/


static void is_alive_get_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

    if(is_alive_state == STATE_ERROR)
      return;

    printf(" <  get is alive\n");
    char msg[MSG_SIZE];
    send_is_alive_ack(msg); 
    coap_set_header_content_format(response, TEXT_PLAIN);
    coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", msg));
}