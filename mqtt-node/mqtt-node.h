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

#define CONFIG_RQST     "config_rqst"
#define STATUS          "status"
#define IRRIGATION      "irrigation"
#define MOISTURE        "moisture"
#define PH              "ph"
#define LIGHT           "light"
#define TEMPERATURE     "tmp"

#define IRR_CMD         "irr_cmd"
#define GET_CONFIG      "get_config"
#define ASSIGN_CONFIG   "assign_config"
#define TIMER_CMD       "timer_cmd"
#define CLOCK_MINUTE    CLOCK_SECOND * 60

/*------------------------------------*/
//DATA STRUCTURES


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

struct node_str{

    struct configuration_str configuration;
    bool irr_status;
    struct measurements_str measurements;
} node_memory;

/*------------------------------------*/

