#include "resource.h"

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

void save_light_timer(int timer){
  light_mem.light_timer = timer;
}

int get_light_timer(){
  return light_mem.light_timer;
}

void set_light_timer(){
  etimer_set(&light_mem.light_etimer, light_mem.light_timer * CLOCK_MINUTE);
}

bool check_light_timer_expired(){
  return etimer_expired(&light_mem.light_etimer);
}
/*-----------------------------------------*/

void send_light_raw(char msg[]){

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
  //char msg[MSG_SIZE];
  char reply[MSG_SIZE];

  int len = coap_get_query_variable(request, "value", &value);
  if(len == 0){
    printf(" <  get sensor/light\n");
    send_light_raw(reply);
  }
  /*else if(len > 0){
    printf(" <  get sensor/light-satus\n");
    snprintf(msg, len + 1, "%s", (char*)value);
    if(strcmp(msg, "status") == 0)
      send_light_status(reply);
    else{
      printf("[-] error unknown in get light sensor [value: %s] \n", msg);
      return;
    }
  } */

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

  printf(" <  put sensor/light\n");
  const uint8_t* arg;
  char msg[MSG_SIZE];
  char reply[MSG_SIZE];
  int len = coap_get_payload(request, &arg);
  if (len <= 0){
    printf("[-] no argument obteined from put request of light_rsc\n");
    return;
  }
  sprintf(msg, "%s", (char*)arg);  
  if(strcmp(msg, "status") == 0){
    printf(" <  get sensor/light-satus\n");
    send_light_status(reply);
  }   
  else{
    light_mem.light_timer = atoi(msg);
    //ctimer_set(&node_timers.light_ctimer, node_memory.configuration.light_timer * CLOCK_MINUTE, send_light_raw, NULL);
    etimer_set(&light_mem.light_etimer, light_mem.light_timer * CLOCK_MINUTE);
    send_light_status(reply); 
  }
  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));
}
