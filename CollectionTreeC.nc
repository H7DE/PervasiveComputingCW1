#include <Timer.h>

module CollectionTreeC {
    uses interface Boot;
    uses interface SplitControl as RadioControl;
    uses interface StdControl as RoutingControl;
    uses interface Send;
    uses interface Leds;
    uses interface Timer<TMilli> as SensorTimer;
    uses interface RootControl;
    uses interface Receive;
    uses interface Random;
}

implementation {
    message_t packet;
    bool sendBusy = FALSE;
    
    uint16_t SENSOR_TIMER_INTERVAL_MILLI = 2000000;


    uint16_t current_sampling_round = 0;
    uint16_t SAMPLING_ROUND_LIMIT = 10;


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
            if (TOS_NODE_ID == 0) {
                call RootControl.setRoot();
            }else{
                call SensorTimer.startPeriodic(SENSOR_TIMER_INTERVAL_MILLI);
            }}
    }

    event void RadioControl.stopDone(error_t err) {}

    void sendMessage() {
        CollectionMsg* msg =
            (CollectionMsg*)call Send.getPayload(&packet, sizeof(CollectionMsg));
        msg->data = TOS_NODE_ID;
        dbg("App", "Sending msg %u\n", msg->data);
        if (call Send.send(&packet, sizeof(CollectionMsg)) == SUCCESS){ 
            sendBusy = TRUE;}
    }
    event void SensorTimer.fired() {
        if (!sendBusy){
            sendMessage();
        }
    }
    event void Send.sendDone(message_t* m, error_t err) {
        sendBusy = FALSE;
    }

    event message_t* 
        Receive.receive(message_t* msg, void* payload, uint8_t len) {
            if(sizeof(CollectionMsg) == len){
                CollectionMsg* pkt = (CollectionMsg*) payload;
                dbg("App", "Received msg: from node %u \n", pkt->data);
            }
            return msg;
        }
}
