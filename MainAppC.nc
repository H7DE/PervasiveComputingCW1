configuration MainAppC {}
implementation {
    components CollectionTreeC, MainC, LedsC, ActiveMessageC;
    components CollectionC as Collector;
    components new CollectionSenderC(0xee);
    components new TimerMilliC() as SensorTimer;
    components new TimerMilliC() as BaseStationTimer;
    components RandomC;

    CollectionTreeC.Boot -> MainC;
    CollectionTreeC.RadioControl -> ActiveMessageC;
    CollectionTreeC.RoutingControl -> Collector;
    CollectionTreeC.Leds -> LedsC;
    CollectionTreeC.SensorTimer -> SensorTimer;
    //CollectionTreeC.BaseStationTimer -> BaseStationTimer;
    CollectionTreeC.Send -> CollectionSenderC;
    CollectionTreeC.RootControl -> Collector;
    CollectionTreeC.Receive -> Collector.Receive[0xee];
    CollectionTreeC.Random -> RandomC;
}

