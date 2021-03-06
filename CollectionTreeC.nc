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

    uint16_t SENSOR_TIMER_INTERVAL_MILLI = 15000;


    uint16_t current_sampling_round = 0; //Current no of samples sent 
    uint16_t SAMPLING_ROUND_LIMIT = 100; //Max number of samples to send


    //Message struct, pkt contains a node id and a what sampling round the pkt was sent in
    typedef nx_struct CollectionMsg {
        nx_uint16_t node_id;
        nx_uint16_t round;
    } CollectionMsg;

    event void Boot.booted() {
        call RadioControl.start();
    }

    task void BootTask(){
        call RoutingControl.start();
        if (TOS_NODE_ID == 0) {
            call RootControl.setRoot();
        } else {
            call SensorTimer.startOneShot(SENSOR_TIMER_INTERVAL_MILLI);
        }
    }

    event void RadioControl.startDone(error_t err) {
        if (err != SUCCESS)
            call RadioControl.start();
        else {
            post BootTask();
        }
    }

    event void RadioControl.stopDone(error_t err) {}

    void sendMessage() {
        CollectionMsg* msg =
            (CollectionMsg*)call Send.getPayload(&packet, sizeof(CollectionMsg));
        msg->node_id = TOS_NODE_ID;
        msg->round = current_sampling_round; 

        // dbg("App", "Sending msg %u\n", msg->node_id);
        if (call Send.send(&packet, sizeof(CollectionMsg)) == SUCCESS){ 
            sendBusy = TRUE;
        }
    }


    task void TimerTask(){
        
        if(++current_sampling_round > SAMPLING_ROUND_LIMIT){
            return;    
        }

        if (!sendBusy){
            sendMessage();
        }
        call SensorTimer.startOneShot(SENSOR_TIMER_INTERVAL_MILLI);

    }

    event void SensorTimer.fired() {
        post TimerTask(); 
    }

    event void Send.sendDone(message_t* m, error_t err) {
        sendBusy = FALSE;
    }

    event message_t* 
        Receive.receive(message_t* msg, void* payload, uint8_t len) {
            if(sizeof(CollectionMsg) == len){
                CollectionMsg* pkt = (CollectionMsg*) payload;
                dbg("App", "Node: %u, Round: %u\n", pkt->node_id, pkt->round);
            }
            return msg;
        }
}
