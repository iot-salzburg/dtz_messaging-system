# Kafka to Logstash Adapter with status webserver integrated in the Data Analytics Stack

This component subscribes to topics from the Apache Kafka message broker and forwards them to the Logstash instance of a running ELK Stack. Optionally, the adapter maps IDs with the SensorThings Server in order to provide a plain and intuitive data channel management.

The Kafka Adapter based on the components:
* Kafka Client [librdkafka](https://github.com/geeknam/docker-confluent-python) version **0.11.1**
* Python Kafka module [confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python) version **0.9.1.2**


## Contents

1. [Requirements](#requirements)
2. [Usage](#usage)
3. [Configuration](#configuration)
4. [Trouble-Shooting](#Trouble-shooting)


## Requirements

1. Install [Docker](https://www.docker.com/community-edition#/download) version **1.10.0+**
2. Install [Docker Compose](https://docs.docker.com/compose/install/) version **1.6.0+**
3. Clone this repository


## Usage

Make sure the `elastic stack` ist running on the same host if you start the DB-Adapter.
Test the `elastic stack` in your browser [http://hostname:5601/status](http://hostname:5601/status).


### Testing
Using `docker-compose`:

```bash
cd /DB-Adapter
sudo docker-compose up --build -d
```

The flag `-d` stands for running it in background (detached mode):


Watch the logs with:

```bash
sudo docker-compose logs -f
```


By default, the stack exposes the following ports:
* 3030: Kafka-ELK HTTP


### Deployment in a docker swarm
Using `docker stack`:

If not already done, add a regitry instance to register the image
```bash
cd /DB-Adapter
sudo docker service create --name registry --publish published=5001,target=5000 registry:2
curl 127.0.0.1:5001/v2/
```
This should output `{}`:


If running with docker-compose works, push the image in order to make the customized image runnable in the stack

```bash
cd ../DB-Adapter
sudo docker-compose build
sudo docker-compose push
```

Actually deploy the service in the stack:
```bash
cd ../DB-Adapter
sudo docker stack deploy --compose-file docker-compose.yml db-adapter
```


Watch if everything worked fine with:

```bash
sudo docker service ls
sudo docker stack ps db-adapter
sudo docker service logs db-adapter_kafka -f
```


By default, the stack exposes the following ports:
* 3030: Kafka-ELK HTTP



## Configuration

The Kafka-Adapter fetches automatically data from the kafka message bus on topic **SensorData**. However, the selected topics can be specified in `kafka-logstash-adapter/.env` by setting the environment
variables. Entries of `KAFKA_TOPICS` and `BOOTSTRAP_SERVERS` should be of the form `topic1,topic2,topic3,...`


```
# Versions
LIBRDKAFKA_VERSION=0.11.1
CONFLUENT_KAFKA_VERSION=0.9.1.2

# Kafka parameters:
# seperate kafka entries with ","
KAFKA_TOPICS=SensorData
BOOTSTRAP_SERVERS=il061,il062,il063

KAFKA_GROUP_ID = "il060"


enable_kafka_adapter=true
enable_sensorthings=true

```

The most important parameter here is **KAFKA_GROUP_ID**. It should be the
hostname of the instance, in order not to miss any data.
The KAFKA_GROUP_ID will be noticed by the kafka broker which stores the
offset for consumed data.
If any data is not consumed at streaming, kafka stores the messages up
to 2 weeks. You can consume this data by temporarily changing the KAFKA_GROUP_ID
to another value.


## Trouble-shooting

#### Can't apt-get update in Dockerfile:
Restart the service

```sudo service docker restart```

or add the file `/etc/docker/daemon.json` with the content:
```
{
    "dns": [your_dns, "8.8.8.8"]
}
```
where `your_dns` can be found with the command:

```bash
nmcli device show <interfacename> | grep IP4.DNS
```

####  Traceback of non zero code 4 or 128:

Restart service with
```sudo service docker restart```

or add your dns address as described above


####  Elasticsearch crashes instantly:

Check permission of `elasticsearch/data`.

```bash
sudo chown -r USER:USER .
sudo chmod -R 777 .
```

or remove redundant docker installations or reinstall it


#### Error starting userland proxy: listen tcp 0.0.0.0:3030: bind: address already in use

Bring down other services, or change the hosts port number in docker-compose.yml. 

Find all running services by:
```bash
sudo docker ps
```


#### errors while removing docker containers:

Remove redundant docker installations


#### "entire heap max virtual memory areas vm.max_map_count [...] likely too low, increase to at least [262144]"
    
Run on host machine:

```bash
sudo sysctl -w vm.max_map_count=262144
```

#### Redis warning: vm.overcommit_memory
Run on host:
```
sysctl vm.overcommit_memory=1

```

#### Redis warning: "WARNING you have Transparent Huge Pages (THP) support enabled in your kernel."

Just ignore this





