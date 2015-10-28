#include <Timer.h>

module CollectionTreeC {
    uses interface Boot;
    uses interface SplitControl as RadioControl;
    uses interface StdControl as RoutingControl;
    uses interface Send;
    uses interface Leds;
    uses interface Timer<TMilli>;
    uses interface RootControl;
    uses interface Receive;
    uses interface Random;
}
implementation {
    message_t packet;
    uint8_t no_sensors = 2; // No of nodes that act as sensors
    uint8_t no_sampling_rounds = 1;
    uint16_t TIMER_INTERVAL_MILLI = 1000000;
    bool SIM_DONE = FALSE; 

    uint8_t results[1][1];

    bool sendBusy = FALSE;
    uint8_t rand = 0;
    


    typedef nx_struct CollectionMsg {
        nx_uint16_t data;
    } CollectionMsg;

    event void Boot.booted() {
        call RadioControl.start();
    }

    event void RadioControl.startDone(error_t err) {
        if (err != SUCCESS)
            call RadioControl.start();
        else {
            call RoutingControl.start();
            if (TOS_NODE_ID == 0) 
                call RootControl.setRoot();
            else
                call Timer.startPeriodic(TIMER_INTERVAL_MILLI);
        }
    }

    event void RadioControl.stopDone(error_t err) {}

    void sendMessage() {
        CollectionMsg* msg =
            (CollectionMsg*)call Send.getPayload(&packet, sizeof(CollectionMsg));
        //rand = call Random.rand8();
        msg->data = rand;
        dbg("App", "Sending msg\n");
        if (call Send.send(&packet, sizeof(CollectionMsg)) != SUCCESS) 
            call Leds.led0On();
        else 
            sendBusy = TRUE;
    }
    event void Timer.fired() {
        if (!sendBusy)
            sendMessage();
    }

    event void Send.sendDone(message_t* m, error_t err) {
        if (err != SUCCESS) 
            call Leds.led0On();
        sendBusy = FALSE;
    }

    event message_t* 
        Receive.receive(message_t* msg, void* payload, uint8_t len) {
            call Leds.led1Toggle();    
            dbg("App", "Received msg: %u\n", msg->data);
            return msg;
        }
}
