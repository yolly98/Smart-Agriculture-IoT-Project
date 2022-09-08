#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "coap-engine.h"
#include "random.h"

#define CLOCK_MINUTE        CLOCK_SECOND * 60
#define MSG_SIZE            512

void parse_json(char json[], int n_arguments, char arguments[][100]);
bool isNumber(char * text);