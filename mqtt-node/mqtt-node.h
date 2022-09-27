#include "contiki.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "os/dev/serial-line.h"
#include <sys/etimer.h>
#include "os/dev/button-hal.h"
#include "os/dev/leds.h"
#include "random.h"

#include "net/netstack.h"
#include "net/routing/routing.h"
#include "mqtt.h"
#include "net/ipv6/uip.h"
#include "net/ipv6/uip-icmp6.h"
#include "net/ipv6/sicslowpan.h"
#include "sys/ctimer.h"
#include "lib/sensors.h"
#include "os/sys/log.h"
#include <strings.h>
/*------------------------------------*/
//COMMANDS

#define CONFIG_RQST         "config_rqst"
#define STATUS_I            "irr_status"
#define STATUS_T            "timer_status"
#define IRRIGATION          "irrigation"
#define MOISTURE            "moisture"
#define PH                  "ph"
#define LIGHT               "light"
#define TMP                 "tmp"
#define IS_ALIVE_ACK        "is_alive_ack"

#define IRR_CMD             "irr_cmd"
#define GET_CONFIG          "get_config"
#define ASSIGN_CONFIG       "assign_config"
#define ASSIGN_I_CONFIG     "assign_i_config"
#define ASSIGN_T_CONFIG     "assign_t_config"
#define ERROR_LAND          "error_land"
#define ERROR_ID            "error_id"
#define TIMER_CMD           "timer_cmd"
#define GET_SENSOR          "get_sensor"
#define IS_ALIVE            "is_alive"
#define CLOCK_MINUTE        CLOCK_SECOND * 60
#define MSG_SIZE            256

/*------------------------------------*/
//DATA STRUCTURES

static struct timers{
    struct etimer btn_etimer;
    struct etimer led_etimer;
    struct etimer mqtt_etimer;
    struct ctimer mst_ctimer;
    struct ctimer ph_ctimer;
    struct ctimer light_ctimer;
    struct ctimer tmp_ctimer;
    struct ctimer irr_duration_ctimer;
    bool sensor_timer_are_setted;
    bool irr_timer_is_setted;
}node_timers;

struct irr_config_str{
    bool enabled;
    unsigned short irr_limit;
    unsigned int irr_duration;
};

struct measurements_str{

    unsigned short soil_moisture;
    short soil_temperature;
    unsigned int light_raw;
    unsigned short ph_level;
};

struct configuration_str{

    unsigned int land_id;
    unsigned int node_id;
    struct irr_config_str irr_config;
    unsigned int mst_timer;
    unsigned int ph_timer;
    unsigned int light_timer;
    unsigned int tmp_timer;
};

static struct node_str{

    struct configuration_str configuration;
    bool irr_status;
    struct measurements_str measurements;
} node_memory;

//UTILITY
bool isNumber(char *text);
void print_config();
void parse_json(char json[], int n_arguments, char arguments[][100]);

//COMMAND ELABORATOR
bool elaborate_cmd(char msg[]);

void is_alive_received_sim(char msg[]);

//SENDING TO SERVER (SIMULATED)
void send_config_request();
void send_status();
void send_status_fake();
void send_irrigation();
void send_is_alive_ack();

//SENSORS READINGS (SIMULATED)
void irr_stopping();
void get_soil_moisture();
void get_ph_level();
void get_lihght_raw();
void get_soil_tmp();

void receive_configuration();

PROCESS(mqtt_node, "Mqtt node");
AUTOSTART_PROCESSES(&mqtt_node);

