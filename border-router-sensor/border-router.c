
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "contiki.h"

/* Log configuration */
#include "sys/log.h"
#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_APP

/* Declare and auto-start this file's process */
PROCESS(border_router, "Border router");
AUTOSTART_PROCESSES(&border_router);


PROCESS_THREAD(border_router, ev, data){
  PROCESS_BEGIN();

#if BORDER_ROUTER_CONF_WEBSERVER
  PROCESS_NAME(webserver_nogui_process);
  process_start(&webserver_nogui_process, NULL);
#endif /* BORDER_ROUTER_CONF_WEBSERVER */

  LOG_INFO("Border router online\n");
  PROCESS_END();
}
