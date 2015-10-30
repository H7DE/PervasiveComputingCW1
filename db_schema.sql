create table node (
    node_id  text primary key
);

create table readings (
    node_id   text not null references node(node_id) ON DELETE CASCADE,
    transmission_round integer not null,
    constraint pk_readings primary key (node_id, transmission_round)
);
