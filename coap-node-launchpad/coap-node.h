#include "contiki.h"
#include "contiki-net.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "os/dev/serial-line.h"
#include <sys/etimer.h>
#include "os/dev/button-hal.h"
#include "os/dev/leds.h"
#include "net/netstack.h"
#include "net/routing/routing.h"
#include "coap-engine.h"
#include "coap-blocking-api.h"
#include "net/ipv6/uip.h"
#include "net/ipv6/uip-icmp6.h"
#include "net/ipv6/sicslowpan.h"
#include "sys/ctimer.h"
#include "lib/sensors.h"
#include "arch/cpu/cc26x0-cc13x0/dev/cc26xx-uart.h"


/*------------------------------------*/
#define SERVER_EP           "coap://[fd00::1]:5683"
#define STATE_INITIALIZED   0
#define STATE_REGISTERED    1
#define STATE_CONFIGURED    2
#define STATE_ERROR         3
#define CLOCK_MINUTE        CLOCK_SECOND * 60
#define MSG_SIZE            200

/*------------------------------------*/

static struct etimer btn_etimer;
static struct etimer led_etimer;

static struct coap_module_str{
    coap_endpoint_t server_ep;
    coap_message_t request[1]; 
}coap_module;

static unsigned int STATE;

extern coap_resource_t config_rsc;
extern coap_resource_t irr_rsc;
extern coap_resource_t is_alive_rsc;
extern coap_resource_t mst_rsc;
extern coap_resource_t ph_rsc;
extern coap_resource_t light_rsc;
extern coap_resource_t tmp_rsc;

//UTILITY
bool isNumber(char *text);
void print_config();
void parse_json(char json[], int n_arguments, char arguments[][100]);

//COAP
void coap_init();
void client_chunk_handler(coap_message_t *response);

//CONFIGURATION RESOURCE FUNCTIONS
void save_config(int land_id, int node_id);
void config_error();
void get_config(unsigned int* land_id,unsigned int* node_id);


//IS_ALIVE RESOURCE FUNCTIONS
void is_alive_init();
void is_alive_error();

//IRRIGATION RESOURCE FUNCTIONS
void save_irr_config(bool enabled, unsigned int irr_limit, unsigned int irr_duration, bool irr_status);
void irr_error();
void get_irr_config(bool* enabled, unsigned int* irr_limit, unsigned int* irr_duration, bool* irr_status);
void set_irr_timer();
void reset_irr_timer(int interval);
void restart_irr_timer();
bool check_irr_timer_expired();
void irr_stopping();
void irr_starting(int moisture);

//MOISTURE RESOURCE FUNCTIONS
void save_mst_timer(int timer);
void mst_error();
int get_mst_timer();
int get_mst_value();
void set_mst_timer();
void reset_mst_timer(int interval);
void restart_mst_timer();
bool check_mst_timer_expired();

//PH RESOURCE FUNCTIONS
void save_ph_timer(int timer);
void ph_error();
int get_ph_timer();
void set_ph_timer();
void reset_ph_timer(int interval);
void restart_ph_timer();
bool check_ph_timer_expired();

//LIGHT RESOURCE FUNCTIONS
void save_light_timer(int timer);
void light_error();
int get_light_timer();
void set_light_timer();
void reset_light_timer(int interval);
void restart_light_timer();
bool check_light_timer_expired();

//TRMPERATURE RESOURCE FUNCTIONS
void save_tmp_timer(int timer);
void tmp_error();
int get_tmp_timer();
void set_tmp_timer();
void reset_tmp_timer(int interval);
void restart_tmp_timer();
bool check_tmp_timer_expired();

PROCESS(coap_node, "Coap node");
AUTOSTART_PROCESSES(&coap_node);

