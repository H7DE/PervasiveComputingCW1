create table experiments (
    experiment_id  text primary key,
    no_nodes integer not null,
    topology_type text not null,
    expected_no_transmission_per_node integer not null
);

create table readings (
    experiment_id  text not null references experiments(experiment_id) ON DELETE CASCADE,
    node_id   text not null,
    transmission_round integer not null
);
