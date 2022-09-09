#include "resource.h"

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

struct irr_config_str{
    bool enabled;
    unsigned int irr_limit;
    unsigned int irr_duration;
    bool irr_status;
    struct etimer irr_duration_etimer;
}irr_mem;

EVENT_RESOURCE(
    irr_rsc,
    "title=\"Irrigation\"; rt = \"Text\"",
    irr_get_handler,
    NULL,
    irr_put_handler,
    NULL,
    irr_event_handler
);

/*------------------------------------------------*/

void save_irr_config(bool enabled, unsigned int irr_limit, unsigned int irr_duration, bool irr_status){

  irr_mem.enabled = enabled;
  irr_mem.irr_limit = irr_limit;
  irr_mem.irr_duration = irr_duration;
  irr_mem.irr_status = irr_status;

}

void get_irr_config(bool* enabled, unsigned int* irr_limit, unsigned int* irr_duration, bool* irr_status){
  *enabled = irr_mem.enabled;
  *irr_limit = irr_mem.irr_limit;
  *irr_duration = irr_mem.irr_duration;
  *irr_status = irr_mem.irr_status;
}

void set_irr_timer(){
  etimer_set(&irr_mem.irr_duration_etimer, irr_mem.irr_duration * CLOCK_MINUTE); 
}

bool check_irr_timer_expired(){
  return (etimer_expired(&irr_mem.irr_duration_etimer) && irr_mem.irr_status);
}
/*-------------------------------------------------*/

void irr_stopping(){
  irr_mem.irr_status = false;
  irr_rsc.trigger();
}

/*------------------------------------------------*/

void irr_starting(int moisture){
  bool irr_enabled =irr_mem.enabled;
  int irr_limit = irr_mem.irr_limit;
  if( irr_enabled && moisture < irr_limit){
      irr_mem.irr_status = true;
      int irr_duration = irr_mem.irr_duration;
      irr_rsc.trigger();
      etimer_set(&irr_mem.irr_duration_etimer, irr_duration * CLOCK_MINUTE); 
  }
}

/*-----------------------------------------------*/
void send_irr_status(char msg[]){

  sprintf(msg, "{ \"cmd\": \"%s\", \"body\": { \"enabled\": \"%s\", \"irr_limit\": %d, \"irr_duration\": %d, \"status\": \"%s\" } }",
      "irr-status",
      irr_mem.enabled?"true":"false",
      irr_mem.irr_limit,
      irr_mem.irr_duration,
      irr_mem.irr_status?"on":"off"
      );
  printf(" >  %s \n", msg);
}

/*----------------------------------------------*/

void send_irrigation(char msg[]){

    sprintf(msg, "{ \"cmd\": \"%s\", \"status\": \"%s\" }",
        "irrigation",
        irr_mem.irr_status?"on":"off"
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

  const char* value;
  //char msg[MSG_SIZE];
  char reply[MSG_SIZE];
  //coap_endpoint_print(coap_get_src_endpoint(request));
  printf("\n");
  
  int len = coap_get_query_variable(request, "value", &value);
  if(len == 0){
    printf(" <  get irrigation\n");
    send_irrigation(reply);
  }
/*  else if(len > 0 && strcmp(msg, "irrigation-status") == 0){
    printf(" <  get irrigation-status\n");
    snprintf(msg, len + 1, "%s", (char*)value);
    if(strcmp(msg, "status") == 0)
      send_irr_status(reply);
    else{
      printf("[-] error unknown in get irr_rsc [value: %s]\n", msg);
      return;
    }
  } */
  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));
}

/*----------------------------------------------*/

static void irr_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){


  printf(" <  put irrigation\n");
  const uint8_t* arg;
  char msg[MSG_SIZE];
  char reply[MSG_SIZE];

  int len = coap_get_payload(request, &arg);
  if (len <= 0){
    printf("[-] no argument obteined from put request of irr_rsc\n");
    return;
  }
  sprintf(msg, "%s", (char*)arg);
  
  if(strcmp(msg, "status") == 0){
    printf(" <  get irrigation-status\n");
    send_irr_status(reply);
  } 
  else{
    printf("[!] IRR_CMD command elaboration ...\n");

    int n_arguments = 4;
    char arguments[n_arguments][100];
    parse_json(msg, n_arguments, arguments);

    if(strcmp(arguments[0], "null") != 0)
        irr_mem.enabled = ((strcmp(arguments[0], "true") == 0)?true:false);
    if(strcmp(arguments[1], "null") != 0)
        irr_mem.irr_status = ((strcmp(arguments[1], "on") == 0)?true:false);
    if(isNumber(arguments[2]) && atoi(arguments[2]) != 0)
        irr_mem.irr_limit = atoi(arguments[2]);
    if(isNumber(arguments[3]) && atoi(arguments[3]) != 0)
      irr_mem.irr_duration = atoi(arguments[3]);

    send_irr_status(reply);
    printf("[+] IRR_CMD command elaborated with success\n");
  }

  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));

}