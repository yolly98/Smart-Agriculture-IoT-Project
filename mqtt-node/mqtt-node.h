#include "contiki.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "os/dev/serial-line.h"
#include <sys/etimer.h>
#include "os/dev/button-hal.h"
#include "os/dev/leds.h"
#include "random.h"

/*------------------------------------*/
//TOPICS

#define CONFIG_RQST     "CONFIG_RQST"
#define STATUS          "STATUS"
#define IRRIGATION      "IRRIGATION"
#define MOISTURE        "MOISTURE"
#define PH              "PH"
#define LIGHT           "LIGHT"
#define TMP             "TMP"
#define IS_ALIVE_ACK    "IS_ALIVE_ACK"

#define IRR_CMD         "IRR_CMD"
#define GET_CONFIG      "GET_CONFIG"
#define ASSIGN_CONFIG   "ASSIGN_CONFIG"
#define TIMER_CMD       "TIMER_CMD"
#define GET_SENSOR      "GET_SENSOR"
#define IS_ALIVE        "IS_ALIVE"
#define CLOCK_MINUTE    CLOCK_SECOND * 60

/*------------------------------------*/
//DATA STRUCTURES

static struct timers{
    struct etimer btn_etimer;
    struct etimer led_etimer;
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
bool elaborate_cmd(char msg[], char topic[]);

//COMMAND RECEIVED (SIMULATED)
void irr_cmd_received_sim(char msg[], char topic[]);
void get_config_received_sim(char msg[], char topic[]);
void assign_config_received_sim(char msg[], char topic[]);
void timer_cmd_received_sim(char msg[], char topic[]);
void get_sensor_received_sim(char msg[], char topic[]);
void is_alive_received_sim(char msg[], char topic[]);

//SENDING TO SERVER (SIMULATED)
void config_request_sim();
void status_sim();
void irrigation_sim();
void is_alive_ack_sim();

//SENSORS READINGS (SIMULATED)
void irr_stopping();
void get_soil_moisture();
void get_ph_level();
void get_lihght_raw();
void get_soil_tmp();

void receive_configuration();

