CONTIKI_PROJECT = coap-node
PLATFORMS_ONLY = cc26x0-cc13x0
all: $(CONTIKI_PROJECT)

MODULES_REL += ./resources

CONTIKI = ../..

include $(CONTIKI)/Makefile.dir-variables
MODULES += $(CONTIKI_NG_APP_LAYER_DIR)/coap

-include $(CONTIKI)/Makefile.identify-target

include $(CONTIKI)/Makefile.include