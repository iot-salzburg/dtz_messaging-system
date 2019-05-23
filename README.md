**This version is deprecated** Please check https://github.com/iot-salzburg/dtz_datastack and https://github.com/iot-salzburg/panta_rhei.

# Panta Rhei: Kafka based Messaging System with SensorThings semantics

This repository includes multiple implementations focusing on the
messaging bus. This includes:

* **sensorthings**: The involves a `docker-compose.yaml` which sets up
the sensorthings GOST server. The POST of instances belongs to
data producer adapter.

* **db-adapter**: The database adapter subscribes to all active topics


* fast-data-dev: a docker-compose that sets up an advanced kafka stack
for testing. Unfortunately, this solution is not scalable.

* kafka-medium: this sets up a scalable kafka stack via docker swarms.
However, when re-deploying, the docker images has to be pruned in
advanced. This is not suitable for our demands.

* connect: it is planned to move from the db-adapter to an integrated
kafka-connect solution, which will guarantee 1to1 delivery.

* Rest-API: Multiple rest APIs are stored here which could be useful
if implemented with a HTTP Proxy and the avro messaging format.

* avro_producer: here some scripts use the avro messaging format in
kafka. Currently we don't use this format.


## Contents

1. [Requirements](#requirements)
2. [Apache Kafka Setup](#apache-kafka-setup)
3. [Sensorthings Server](#sensorthings-server)
4. [DB-Adapter](#db-adapter)
5. [Trouble-Shooting](#trouble-shooting)


## Requirements

1. Install [Docker](https://www.docker.com/community-edition#/download) version **1.10.0+**
2. Install [Docker Compose](https://docs.docker.com/compose/install/) version **1.6.0+**
3. Clone this repository



## Apache Kafka Setup

The easiest way found to set up a kafka stack, is without the use of
docker, but instead install it directly via cli.

For each node:

```
sudo apt-get update && apt-get install openjdk-8-jre wget -y
set kafka_version=0.11.0.3
wget https://archive.apache.org/dist/kafka/${kafka_version}/kafka_2.11-${kafka_version}.tgz
tar -xvzf kafka_2.11-${kafka_version}.tgz
rm kafka_2.11-${kafka_version}.tgz
sudo mv kafka_2.11-${kafka_version} /kafka
sudo chmod +x /kafka/bin/*
cd /kafka
```
Then make a config file  for each broker on  node [k] :

```
cp config/server.properties config/il08[k].properties
```

And set for each the following properties:

```
broker.id=[k]
delete.topic.enable=true
log.dirs=/tmp/kafka-logs-[k]
zookeeper.connect=il081:2181
```

Note that zookeeper will run solely on node il081.
### Starting Kafka

Run zookeeper only on node il081, and kafka on each node [k].
The `-daemon` flag runs the process in background.
```
user@il081:~$ /kafka/bin/zookeeper-server-start.sh -daemon /kafka/config/zookeeper.properties
user@il081:~$ /kafka/bin/kafka-server-start.sh -daemon /kafka/config/il08[1].properties
user@il082:~$ /kafka/bin/kafka-server-start.sh -daemon /kafka/config/il08[2].properties
user@il083:~$ /kafka/bin/kafka-server-start.sh -daemon /kafka/config/il08[3].properties
```

### Testing
This is possible on any node.

```
/kafka/bin/kafka-topics.sh --zookeeper il081:2181 --list
/kafka/bin/kafka-topics.sh --zookeeper il081:2181 --create --topic test-topic --replication-factor 2 --partitions 3
/kafka/bin/kafka-topics.sh --zookeeper il081:2181 --describe --topic test-topic
/kafka/bin/kafka-console-producer.sh --broker-list il081:9092,il082:9092,il083:9092 --topic test-topic
/kafka/bin/kafka-console-consumer.sh --bootstrap-server il081:9092,il082:9092,il083:9092 --topic test-topic --from-beginning
```

Here we should see that data written from the producer will appear
to the consumer. It makes sense to use multiple terminals and nodes.


### Create our topics

The data should be persistent for at least 6 weeks
and cleaned up compactly.
```
/kafka/bin/kafka-topics.sh --zookeeper il081:2181 --create --topic dtz.sensorthings --replication-factor 2 --partitions 3 --config cleanup.policy=compact --config retention.ms=3628800000 --config retention.bytes=-1
/kafka/bin/kafka-topics.sh --zookeeper il081:2181 --create --topic dtz.logging --replication-factor 1 --partitions 3 --config cleanup.policy=compact --config retention.ms=3628800000 --config retention.bytes=-1
```

### Delete topics
```
/kafka/bin/zookeeper-shell.sh il081:2181 ls /brokers/topics
/kafka/bin/zookeeper-shell.sh il081:2181 rmr /brokers/topics/topicname
```





## Sensorthings Server

Using `docker`:

```bash
cd compose/sensorthings
./start-sensorthings.sh
```

The flag `-d` stands for running it in background (detached mode):

Watch the logs with:

```bash
docker service logs -f st
```



## DB-Adapter
Using `docker`:

```bash
cd compose/db-adapter
./start-adapter.sh
```




## Fast-data-dev services:
These services are obsolete by the current state of implementation.

### Producer services

Submit a contract to create a new channel
```
http://hostname:3033/submit_contract
{
  "name": "Ultimaker 2, number11",
  "description": "A 3D printing system in the 3D printing farm.",
  "properties": {
		"owner": "Salzburg Research",
		"from": "2018-04-19T13:11:12+00:00",
		"to": "2018-06-09T13:11:12+00:00",
		"viewers": ["viewingcompany"],
    "monitoring_clauses": {
			"machined part": "partID",
			"machined order": "orderID"
		}
  },
  "Locations": [{
    "name": "IoT Lab",
    "description": "Salzburg Research",
    "encodingType": "application/vnd.geo+json",
    "location": {
      "type": "Point",
      "coordinates": [13.040631, 47.822782]
    }
  }],
  "Datastreams": [{
    "name": "Air Temperature DS",
    "description": "Datastream for recording temperature",
    "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
    "unitOfMeasurement": {
      "name": "Degree Celsius",
      "symbol": "degC",
      "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#DegreeCelsius"
    },
    "ObservedProperty": {
      "name": "Area Temperature",
      "description": "The degree or intensity of heat present in the area",
      "definition": "http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#AreaTemperature"
    },
    "Sensor": {
      "name": "DHT22",
      "description": "DHT22 temperature sensor",
      "encodingType": "application/pdf",
      "metadata": "https://cdn-shop.adafruit.com/datasheets/DHT22.pdf"
    }
  },
								 {
    "name": "Nozzle Temperature DS",
    "description": "Datastream for recording temperature of the printe's nozzle",
    "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
    "unitOfMeasurement": {
      "name": "Degree Celsius",
      "symbol": "degC",
      "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#DegreeCelsius"
    },
    "ObservedProperty": {
      "name": "Nozzle Temperature",
      "description": "The degree or intensity of heat of the printer's nozzle",
      "definition": "http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#AreaTemperature"
    },
    "Sensor": {
      "name": "PT100",
      "description": "PT100 temperature sensor",
      "encodingType": "application/pdf",
      "metadata": "http://irtfweb.ifa.hawaii.edu/~iqup/domeenv/PDF/pt100plat.pdf"
    }
  }]
}
```
This request will return an augmented payload. One important field is
"@iot.dataChannelID" which is an unique identifier for created data-channel.


Send Data on a channel
```
http://hostname:8082/topics/<@iot.dataChannelID>
{
  "records": [
    {
      "key": "998",
      "value": {"iot.id": 998,
	"phenomenonTime": "{% now 'iso-8601', '' %}",
	"resultTime": "{% now 'iso-8601', '' %}",
	"result": 1234.56}
    }
  ]
}
```


### Consumer Services:
Create a Consumer
```
http://hostname:8082/consumers/my-consumer-group
{
  "name": "my_consumer_json",
  "format": "json",
  "auto.offset.reset": "earliest",
  "auto.commit.enable": "false"
}
```


Subscribe Consumer to topics
```
http://hostname:8082/consumers/my-consumer-group/instances/my_consumer_json/subscription
{
  "topics": [
    "<@iot.dataChannelID>"
  ]
}
```

Get Data from Consumer
```GET
http://hostname:8082/consumers/my-consumer-group/instances/my_consumer_json/records?timeout=1000&max_bytes=300000
```





## Trouble-Shooting

* ERROR org.apache.kafka.common.errors.TopicExistsException:
Topic 'topic-name' already exists.
If data is sent before kafka topics are restored, an error will be returned.

* ERROR in all gost applications: "invalid data found"
There could be a version jump between postgresql 9 and 10, which leads to
invalid data representation. Remove all images involving GOST

