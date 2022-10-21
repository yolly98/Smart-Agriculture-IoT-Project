#include "mqtt-node.h"


/*---------------------------------------------------------------------------*/
#define LOG_MODULE "mqtt-client"
#ifdef MQTT_CLIENT_CONF_LOG_LEVEL
#define LOG_LEVEL MQTT_CLIENT_CONF_LOG_LEVEL
#else
#define LOG_LEVEL LOG_LEVEL_DBG
#endif

/*---------------------------------------------------------------------------*/
/* MQTT broker address. */
#define MQTT_CLIENT_BROKER_IP_ADDR "fd00::1"

static const char *broker_ip = MQTT_CLIENT_BROKER_IP_ADDR;

// Defaukt config values
#define DEFAULT_BROKER_PORT         1883
#define DEFAULT_PUBLISH_INTERVAL    (30 * CLOCK_SECOND)

// We assume that the broker does not require authentication

/*---------------------------------------------------------------------------*/

#define STATE_INIT    		    0
#define STATE_NET_OK    	    1
#define STATE_CONNECTING      2
#define STATE_CONNECTED       3
#define STATE_SUBSCRIBING     4
#define STATE_SUBSCRIBED      5
#define STATE_DISCONNECTED    6
#define STATE_CONFIGURED      7
#define STATE_ERROR           8

/*---------------------------------------------------------------------------*/
/* Maximum TCP segment size for outgoing segments of our socket */
#define MAX_TCP_SEGMENT_SIZE    32
#define CONFIG_IP_ADDR_STR_LEN   64
/*---------------------------------------------------------------------------*/
/*
 * Buffers for Client ID and Topics.
 * Make sure they are large enough to hold the entire respective string
 */
#define BUFFER_SIZE 64

// Periodic timer to check the state of the MQTT client
#define STATE_MACHINE_PERIODIC     (CLOCK_SECOND * 5)

/*---------------------------------------------------------------------------*/
/*
 * The main MQTT buffers.
 * We will need to increase if we start publishing more data.
 */
#define APP_BUFFER_SIZE 512
#define MAX_MSGS 10

struct mqtt_publish_list{
  char msg[APP_BUFFER_SIZE];
  char cmd[BUFFER_SIZE];
  struct mqtt_publish_list * ptr;
};

static struct mqtt_module_str{
  uint8_t state;
  mqtt_status_t status;
  char broker_address[CONFIG_IP_ADDR_STR_LEN];
  char client_id[BUFFER_SIZE];
  char pub_topic[BUFFER_SIZE];
  char sub_topic[BUFFER_SIZE];
  char app_buffer[APP_BUFFER_SIZE];
  struct mqtt_message *msg_ptr;
  struct mqtt_connection conn;
  uip_ipaddr_t dest_ipaddr;
  struct mqtt_publish_list* plist_head;
  struct mqtt_publish_list* plist_tail;
  unsigned int messages;
} mqtt_module;

/*--------------------------------------------------------*/

void print_mqtt_status(){

    if(LOG_ENABLED) printf("state: %d\n", mqtt_module.state);
    if(LOG_ENABLED) printf("-----BUFFER MQTT--------\n");
    struct mqtt_publish_list *p = mqtt_module.plist_head;
    int i;
    for(i = 0; i < mqtt_module.messages; i++){
        if(LOG_ENABLED) printf("[ %s, len: %ld]->", p->cmd, (long int)(strlen(p->msg)));
        p = p->ptr;
    }
    if(LOG_ENABLED) printf("\n");
    if(LOG_ENABLED) printf("------------------\n");

}


/*--------------------------------------------------------*/

bool mqtt_publish_service(char msg[], char cmd[]){ //add to list

  if(mqtt_module.messages == MAX_MSGS){
    if(LOG_ENABLED) printf("[-] buffer for msg to publish is full\n");
    return false;
  }

  if(LOG_ENABLED) printf("[!] adding message to mqtt list\n");
  
  struct mqtt_publish_list *new_msg = (struct mqtt_publish_list*)malloc(sizeof(struct mqtt_publish_list));
  sprintf(new_msg->msg, "%s", msg);
  sprintf(new_msg->cmd, "%s", cmd);
  new_msg->ptr = NULL;

  if(mqtt_module.plist_head == NULL){
    mqtt_module.plist_head = new_msg;
    mqtt_module.plist_tail = new_msg;
  }
  else{
    new_msg->ptr = mqtt_module.plist_head;
    mqtt_module.plist_head = new_msg;
  }

  mqtt_module.messages++;
  //print_mqtt_status();
  return true;
}

/*--------------------------------------------------------*/

bool get_msg_to_publish(char msg[], char topic[]){ //remove from list

  if(mqtt_module.messages == 0)
    return false;

  char cmd[BUFFER_SIZE];
  sprintf(msg, "%s",  mqtt_module.plist_tail->msg);
  sprintf(cmd, "%s",  mqtt_module.plist_tail->cmd);
  sprintf(topic, "%s", "SERVER");

  if(LOG_ENABLED) printf("[!] Publishing [ %s, len: %ld]\n", cmd, (long int)(strlen(msg)));

  if(mqtt_module.messages == 1){
    mqtt_module.plist_head = NULL;
    mqtt_module.plist_tail = NULL;
  }
  else{
    struct mqtt_publish_list *p = mqtt_module.plist_head;
    int i;
    for(i = 0; i < mqtt_module.messages ; i++){
      if(i == mqtt_module.messages - 2)
        break;
      p = p->ptr;
    }

    mqtt_module.plist_tail = p;
    mqtt_module.plist_tail->ptr = NULL;
  }

  mqtt_module.messages--;
  //print_mqtt_status();
  return true;

}

/*---------------------------------------------------------------------------*/

static void pub_handler(
  const char *topic,
  uint16_t topic_len,
  const uint8_t *chunk,
   uint16_t chunk_len
   ){

  if (mqtt_module.state == STATE_ERROR)
    return;

  if(LOG_ENABLED) printf("[!] received: topic='%s' (len=%u), chunk_len=%u\n", topic,
          topic_len, chunk_len);

  elaborate_cmd((char*)chunk);
}

/*---------------------------------------------------------------------------*/

static void mqtt_event(struct mqtt_connection *m, mqtt_event_t event, void *data){
  
  if (mqtt_module.state == STATE_ERROR)
    return;

  switch(event) {
    case MQTT_EVENT_CONNECTED: {
        if(LOG_ENABLED) printf("[+] Application has a MQTT connection\n");

        mqtt_module.state = STATE_CONNECTED;
        break;
    }
    case MQTT_EVENT_DISCONNECTED: {
      if(LOG_ENABLED) printf("[-] MQTT Disconnect. Reason %u\n", *((mqtt_event_t *)data));

      mqtt_module.state = STATE_DISCONNECTED;
      process_poll(&mqtt_node);
      break;
    }
    case MQTT_EVENT_PUBLISH: {
      mqtt_module.msg_ptr = data;

      pub_handler(mqtt_module.msg_ptr->topic, strlen(mqtt_module.msg_ptr->topic),
                  mqtt_module.msg_ptr->payload_chunk, mqtt_module.msg_ptr->payload_length);
      break;
    }
    case MQTT_EVENT_SUBACK: {
#if MQTT_311
      mqtt_suback_event_t *suback_event = (mqtt_suback_event_t *)data;

      if(suback_event->success) {
        if(LOG_ENABLED) printf("[+] Application is subscribed to topic successfully\n");
        mqtt_module.state = STATE_SUBSCRIBED;

      } else {
        if(LOG_ENABLED) printf("[-] Application failed to subscribe to topic (ret code %x)\n", suback_event->return_code);
      }
#else
      if(LOG_ENABLED) printf("[+] Application is subscribed to topic successfully\n");
      mqtt_module.state = STATE_SUBSCRIBED;
#endif
      break;
    }
    case MQTT_EVENT_UNSUBACK: {
      if(LOG_ENABLED) printf("[+] Application is unsubscribed to topic successfully\n");
      break;
    }
    case MQTT_EVENT_PUBACK: {
      if(LOG_ENABLED) printf("[+] Publishing complete.\n");
      break;
    }
    default:
      if(LOG_ENABLED) printf("[-] Application got a unhandled MQTT event: %i\n", event);
      break;
  }
}

/*--------------------------------------------------------------*/

static bool have_connectivity(void){
  if(uip_ds6_get_global(ADDR_PREFERRED) == NULL ||
     uip_ds6_defrt_choose() == NULL) {
    return false;
  }
  return true;
}

/*---------------------------------------------------------------------------*/

void mqtt_init_service(){

  if(LOG_ENABLED) printf("MQTT Service\n");

  mqtt_module.msg_ptr = 0;
  mqtt_module.plist_head = NULL;
  mqtt_module.plist_tail = NULL;
  mqtt_module.messages = 0;

  // Initialize the ClientID as MAC address
  snprintf(mqtt_module.client_id, BUFFER_SIZE, "%02x%02x%02x%02x%02x%02x",
                     linkaddr_node_addr.u8[0], linkaddr_node_addr.u8[1],
                     linkaddr_node_addr.u8[2], linkaddr_node_addr.u8[5],
                     linkaddr_node_addr.u8[6], linkaddr_node_addr.u8[7]);

  // Broker registration					 
  mqtt_register(&mqtt_module.conn, &mqtt_node, mqtt_module.client_id, mqtt_event,
                  MAX_TCP_SEGMENT_SIZE);
				  
  mqtt_module.state = STATE_INIT;

  etimer_set(&node_timers.mqtt_etimer, STATE_MACHINE_PERIODIC);

}

/*---------------------------------------------------------------------------*/

void mqtt_connection_service(){

  if(mqtt_module.state==STATE_INIT){
    if(have_connectivity()==true)  
      mqtt_module.state = STATE_NET_OK;
  } 
  
  if(mqtt_module.state == STATE_NET_OK){
    // Connect to MQTT server
    if(LOG_ENABLED) printf("[!] Connecting!\n");
    
    memcpy(mqtt_module.broker_address, broker_ip, strlen(broker_ip));
    
    mqtt_connect(
              &mqtt_module.conn, mqtt_module.broker_address,
              DEFAULT_BROKER_PORT,
              (DEFAULT_PUBLISH_INTERVAL * 3) / CLOCK_SECOND,
              MQTT_CLEAN_SESSION_ON);
    mqtt_module.state = STATE_CONNECTING;
  }
  
  if(mqtt_module.state==STATE_CONNECTED){

    // Subscribe to a topic
    int land_id = node_memory.configuration.land_id;
    int node_id = node_memory.configuration.node_id;
    sprintf(mqtt_module.sub_topic, "NODE/%d/%d", land_id, node_id);

    mqtt_module.status = mqtt_subscribe(&mqtt_module.conn, NULL, mqtt_module.sub_topic, MQTT_QOS_LEVEL_0);

    if(LOG_ENABLED) printf("[!] Subscribing for topic %s\n", mqtt_module.sub_topic);

    if(mqtt_module.status == MQTT_STATUS_OUT_QUEUE_FULL) {
      if(LOG_ENABLED) printf("[-] Tried to subscribe but command queue was full!\n");
      mqtt_module.state = STATE_INIT;
    }
    mqtt_module.state = STATE_SUBSCRIBING;
  }

  if(mqtt_module.state == STATE_SUBSCRIBED || mqtt_module.state == STATE_CONFIGURED){
    
    if(!get_msg_to_publish(mqtt_module.app_buffer, mqtt_module.pub_topic)){
      etimer_restart(&node_timers.mqtt_etimer);
      return;
    }
      
    mqtt_publish(&mqtt_module.conn, NULL, mqtt_module.pub_topic, (uint8_t *)mqtt_module.app_buffer,
            strlen(mqtt_module.app_buffer), MQTT_QOS_LEVEL_0, MQTT_RETAIN_OFF);

  }
  else if ( mqtt_module.state == STATE_DISCONNECTED ){
    if(LOG_ENABLED) printf("[-] Disconnected form MQTT broker\n");	
    mqtt_module.state = STATE_INIT;
  }

  etimer_restart(&node_timers.mqtt_etimer);

}

/*---------------------------------------------------------------------------*/
