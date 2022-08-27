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

#define STATE_INIT    		  0
#define STATE_NET_OK    	  1
#define STATE_CONNECTING      2
#define STATE_CONNECTED       3
#define STATE_SUBSCRIBED      4
#define STATE_DISCONNECTED    5

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
#define STATE_MACHINE_PERIODIC     (CLOCK_SECOND*1)

/*---------------------------------------------------------------------------*/
/*
 * The main MQTT buffers.
 * We will need to increase if we start publishing more data.
 */
#define APP_BUFFER_SIZE 512


#define MAX_TOPIC 7

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
} mqtt_module;

/*---------------------------------------------------------------------------*/
static void pub_handler(
  const char *topic,
  uint16_t topic_len,
  const uint8_t *chunk,
   uint16_t chunk_len
   ){
  printf("received: topic='%s' (len=%u), chunk_len=%u\n", topic,
          topic_len, chunk_len);

  elaborate_cmd((char*)chunk, (char*)topic);
}
/*---------------------------------------------------------------------------*/
static void mqtt_event(struct mqtt_connection *m, mqtt_event_t event, void *data){
  switch(event) {
    case MQTT_EVENT_CONNECTED: {
        printf("Application has a MQTT connection\n");

        mqtt_module.state = STATE_CONNECTED;
        break;
    }
    case MQTT_EVENT_DISCONNECTED: {
      printf("MQTT Disconnect. Reason %u\n", *((mqtt_event_t *)data));

      mqtt_module.state = STATE_DISCONNECTED;
      //process_poll(&mqtt_client_process);
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
        printf("Application is subscribed to topic successfully\n");
      } else {
        printf("Application failed to subscribe to topic (ret code %x)\n", suback_event->return_code);
      }
#else
      printf("Application is subscribed to topic successfully\n");
#endif
      break;
    }
    case MQTT_EVENT_UNSUBACK: {
      printf("Application is unsubscribed to topic successfully\n");
      break;
    }
    case MQTT_EVENT_PUBACK: {
      printf("Publishing complete.\n");
      break;
    }
    default:
      printf("Application got a unhandled MQTT event: %i\n", event);
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

  printf("MQTT Service\n");

  mqtt_module.msg_ptr = 0;

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
    printf("Connecting!\n");
    
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
    strcpy(mqtt_module.sub_topic, "#");

    mqtt_module.status = mqtt_subscribe(&mqtt_module.conn, NULL, mqtt_module.sub_topic, MQTT_QOS_LEVEL_0);

    printf("Subscribed for topic %s\n", mqtt_module.sub_topic);

    if(mqtt_module.status == MQTT_STATUS_OUT_QUEUE_FULL) 
      LOG_ERR("Tried to subscribe but command queue was full!\n");
      //PROCESS_EXIT();
    
    mqtt_module.state = STATE_SUBSCRIBED;

  }
  else if ( mqtt_module.state == STATE_DISCONNECTED ){
    LOG_ERR("Disconnected form MQTT broker\n");	
    // Recover from error
  }

  etimer_restart(&node_timers.mqtt_etimer);

}

/*---------------------------------------------------------------------------*/

void mqtt_publish_service(char msg[],char topic[]){

  if(mqtt_module.state == STATE_SUBSCRIBED){
      sprintf(mqtt_module.pub_topic, "%s", topic);
      sprintf(mqtt_module.app_buffer, "%s", msg);
      printf("%s Publishing ... [len = %ld]\n", mqtt_module.app_buffer, strlen(msg));
        
      mqtt_publish(&mqtt_module.conn, NULL, mqtt_module.pub_topic, (uint8_t *)mqtt_module.app_buffer,
              strlen(mqtt_module.app_buffer), MQTT_QOS_LEVEL_0, MQTT_RETAIN_OFF);
  }
  else
    printf("publishing failed\n");
}