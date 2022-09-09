#include "resource.h"

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

void save_mst_timer(int timer){
  mst_mem.mst_timer = timer;
}

int get_mst_timer(){
  return mst_mem.mst_timer;
}

int get_mst_value(){
  return mst_mem.soil_moisture;
}

void set_mst_timer(){
  etimer_set(&mst_mem.mst_etimer, mst_mem.mst_timer * CLOCK_MINUTE);
}

bool check_mst_timer_expired(){
  return etimer_expired(&mst_mem.mst_etimer);
}

/*--------------------------------------------*/

void send_soil_moisture(char msg[]){

    int moisture = (15 + random_rand()%50);
    mst_mem.soil_moisture = moisture;
    printf("[+] soil moisture detected: %d\n", moisture);

    sprintf(msg,"{ \"cmd\": \"%s\", \"value\": %d }",
        "mst",
        mst_mem.soil_moisture
      );

    printf(" >  %s\n", msg);

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

  char reply[MSG_SIZE];

  printf(" <  get sensor/mst\n");
  send_soil_moisture(reply);

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

  printf(" <  get sensor/put\n");
  const uint8_t* arg;
  char msg[MSG_SIZE];
  char reply[MSG_SIZE];
  int len = coap_get_payload(request, &arg);
  if (len <= 0){
    printf("[-] no argument obteined from put request of mst_rsc\n");
    return;
  }

  sprintf(msg, "%s", (char*)arg);
  if(strcmp(msg, "status") == 0){
    printf(" <  get sensor/mst-status\n");
    send_mst_status(reply);
  } 
  else{
    mst_mem.mst_timer = atoi(msg);
    etimer_set(&mst_mem.mst_etimer, mst_mem.mst_timer * CLOCK_MINUTE);
    send_mst_status(reply); 
  }
  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_payload(response, buffer, snprintf((char *)buffer, preferred_size, "%s", reply));
}