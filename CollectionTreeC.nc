#include <Timer.h>

module CollectionTreeC {
    uses interface Boot;
    uses interface SplitControl as RadioControl;
    uses interface StdControl as RoutingControl;
    uses interface Send;
    uses interface Leds;
    uses interface Timer<TMilli> as SensorTimer;
    uses interface Timer<TMilli> as BaseStationTimer;
    uses interface RootControl;
    uses interface Receive;
    uses interface Random;
}

implementation {
    message_t packet;
    uint8_t no_sensors = 2; // No of nodes that act as sensors
    uint8_t no_sampling_rounds = 1;
    uint32_t SENSOR_TIMER_INTERVAL_MILLI = 2000000;
    uint32_t BASE_STATION_TIMER_INTERVAL_MILLI = 2000000; 
    bool SIM_DONE = FALSE; 

    int results[10][1]; /*No sampling round, Sample at that round*/

    bool sendBusy = FALSE;
    uint8_t rand = 0;

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
            //call BaseStationTimer.startPeriodic(BASE_STATION_TIMER_INTERVAL_MILLI);
            }else{
                call SensorTimer.startPeriodic(SENSOR_TIMER_INTERVAL_MILLI);
        }}
    }

    event void RadioControl.stopDone(error_t err) {}

    void sendMessage() {
        CollectionMsg* msg =
            (CollectionMsg*)call Send.getPayload(&packet, sizeof(CollectionMsg));
        //rand = call Random.rand8();
        msg->data = TOS_NODE_ID;
        dbg("App", "Sending msg %u\n", msg->data);
        if (call Send.send(&packet, sizeof(CollectionMsg)) != SUCCESS) 
            call Leds.led0On();
        else 
            sendBusy = TRUE;
    }
    event void SensorTimer.fired() {
        if (!sendBusy)
            sendMessage();
    }
    event void BaseStationTimer.fired(){
        if(++current_sampling_round < SAMPLING_ROUND_LIMIT){
            //call BaseStationTimer.startOneShot(BASE_STATION_TIMER_INTERVAL_MILLI);
        } else{
            SIM_DONE = TRUE;    
            dbg("App", "Sim finishing\n");
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
                //results[sampling_round][pkt->data] = TRUE;
            }

            return msg;
        }
}
