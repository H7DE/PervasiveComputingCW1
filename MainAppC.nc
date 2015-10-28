configuration MainAppC {}
implementation {
    components CollectionTreeC, MainC, LedsC, ActiveMessageC;
    components CollectionC as Collector;
    components new CollectionSenderC(0xee);
    components new TimerMilliC();
    components RandomC;

    CollectionTreeC.Boot -> MainC;
    CollectionTreeC.RadioControl -> ActiveMessageC;
    CollectionTreeC.RoutingControl -> Collector;
    CollectionTreeC.Leds -> LedsC;
    CollectionTreeC.Timer -> TimerMilliC;
    CollectionTreeC.Send -> CollectionSenderC;
    CollectionTreeC.RootControl -> Collector;
    CollectionTreeC.Receive -> Collector.Receive[0xee];
    CollectionTreeC.Random -> RandomC;
}

