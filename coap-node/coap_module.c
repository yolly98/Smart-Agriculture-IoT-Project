#include "coap-node.h"

#define SERVER_EP           "coap://[fd00::1]:5683"
#define STATE_INITIALIZED   0
#define STATE_CONFIGURED    1

static struct coap_module_str{
    coap_endpoint_t server_ep;
    coap_message_t request[1]; 
    unsigned int state;
}coap_module;

/*---------------------------------------*/

void coap_init(){

    coap_endpoint_parse(SERVER_EP, strlen(SERVER_EP), &coap_module.server_ep);
//    coap_activate_resource(&config_rsc);
//    coap_activate_resource(&irr_rsc);
//    coap_activate_resource(&isalive_rsc);
//    coap_activate_resource(&mst_rsc);
//    coap_activate_resource(&ph_rsc);
//    coap_activate_resource(&light_rsc);
//    coap_activate_resource(&tmp_rsc);
    coap_module.state = STATE_INITIALIZED;
}

/*-----------------------------------------*/

void client_chunk_handler(coap_message_t *response){

    const uint8_t *chunk;

    if(response == NULL) {
        puts("Request timed out");
        return;
    }

    int len = coap_get_payload(response, &chunk);
    char msg[MSG_SIZE];
    sprintf(msg,"%s",chunk);
    assign_config(msg);
    //congig_rsc.trigger();
    printf("|%.*s", len, (char *)chunk);
}

/*---------------------------------------*/

void coap_send(char msg[]){

    /* prepare coap_module.request, TID is set by COAP_BLOCKING_REQUEST() */
    coap_init_message(coap_module.request, COAP_TYPE_CON, COAP_POST, 0);
    coap_set_header_uri_path(coap_module.request, "/new_config");

    coap_set_payload(coap_module.request, (uint8_t *)msg, strlen(msg) - 1);

    COAP_BLOCKING_REQUEST(&coap_module.server_ep, coap_module.request, client_chunk_handler);

}



