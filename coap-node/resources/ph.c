#include "resource.h"

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

static struct ph_str{
  unsigned int ph_level;
  unsigned int ph_timer;
  struct etimer ph_etimer;
  int state;
}ph_mem;

EVENT_RESOURCE(
    ph_rsc,
    "title=\"Ph\"; rt = \"Text\"",
    ph_get_handler,
    NULL,
    ph_put_handler,
    NULL,
    ph_event_handler
);

/*--------------------------------------------*/

void save_ph_timer(int timer){
  ph_mem.ph_timer = timer;
  ph_mem.state = STATE_CONFIGURED;
}

void ph_error(){
  ph_mem.state = STATE_ERROR;
}

int get_ph_timer(){
  return ph_mem.ph_timer;
}

void set_ph_timer(){
  etimer_set(&ph_mem.ph_etimer, ph_mem.ph_timer * CLOCK_MINUTE);
}

void reset_ph_timer(){
  etimer_reset_with_new_interval(&ph_mem.ph_etimer, ph_mem.ph_timer * CLOCK_MINUTE);
}

void restart_ph_timer(){
  etimer_restart(&ph_mem.ph_etimer);
}

bool check_ph_timer_expired(){
  return etimer_expired(&ph_mem.ph_etimer);
}
/*---------------------------------------*/

void send_ph_level(char msg[]){
 
    ph_mem.ph_level = 4 + random_rand()%5;
    printf("[+] ph level detected: %d\n", ph_mem.ph_level);

    sprintf(msg,"{\"cmd\":\"%s\",\"value\":%d}",
        "ph", 
        ph_mem.ph_level
        );
    
    printf(" >  %s\n", msg);
}

/*------------------------------------------*/

void send_ph_status(char msg[]){
  sprintf(msg,"{\"cmd\":\"%s\",\"timer\":%d}",
      "ph-status",
      ph_mem.ph_timer
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

  if(ph_mem.state == STATE_ERROR)
      return;

  char reply[MSG_SIZE] = "";

  printf(" <  get sensor/ph\n");
  
  send_ph_level(reply);
  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));

}

/*-------------------------------------------------*/

static void ph_put_handler(
  coap_message_t *request,
  coap_message_t *response,
  uint8_t *buffer,
  uint16_t preferred_size,
  int32_t *offset
  ){

  if(ph_mem.state == STATE_ERROR)
      return;

  printf(" <  put sensor/ph\n");
  const uint8_t* arg;
  char msg[MSG_SIZE];
  char reply[MSG_SIZE];
  int len = coap_get_payload(request, &arg);
  if (len <= 0){
    printf("[-] no argument obteined from put request of ph_rsc\n");
    return;
  }
  sprintf(msg, "%s", (char*)arg);
  
  if(strcmp(msg, "status") == 0){
    printf(" <  get sensor/ph-status\n");
    send_ph_status(reply);
    coap_remove_observer_by_uri(NULL, ph_rsc.url); //remove observer
  }
  else{
    ph_mem.ph_timer = atoi(msg);
    reset_ph_timer();
    send_ph_status(reply); 
  }
  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));
}
