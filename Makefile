COMPONENT=MainAppC
CFLAGS += -I$(TOSDIR)/lib/net \
		  -I$(TOSDIR)/lib/net/le \
		  -I$(TOSDIR)/lib/net/ctp
include $(MAKERULES)
