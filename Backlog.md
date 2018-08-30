# Internal Backlog of the Cluster setup
Project: https://github.com/iot-salzburg/messaging-system

Dir: /mnt/D/sr_config/cschranz/Dokumente/DTZ/github_messaging-system

fast-data-dev is just good for testing.
Therefore the installation is done manually


## Label the nodes
docker node update --label-add zoo=81 il081

docker node update --label-add kafka=81 il081

docker node update --label-add kafka=82 il082

docker node update --label-add kafka=83 il083


## kafka-medium:
Finally works with changes (on same page as comment)

cd messaging-system/compose/kafka-medium

See the [tutorial](https://medium.com/@NegiPrateek/wtf-setting-up-kafka-cluster-using-docker-stack-5efc68841c23)

sudo apt-get update

sudo apt-get dist-upgrade

sudo apt-get install openjdk-8-jre wget -y

wget https://archive.apache.org/dist/kafka/0.11.0.3/kafka_2.11-0.11.0.3.tgz

sudo tar -xvzf kafka_2.11-0.11.0.3.tgz

sudo mv kafka_2.11-0.11.0.3 /kafka

Start the swarm with:

./start-kafka-stack.sh


## Test the cluster with bash in the container

docker container ls

docker exec -it uid bash


### Test the system
/kafka/bin/kafka-topics.sh --zookeeper zookeeper:2181 --list

/kafka/bin/kafka-topics.sh --zookeeper zookeeper:2181 --create --topic test-topic --replication-factor 2 --partitions 3


/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka1:9092,kafka2:9092,kafka3:9092 --topic test-topic --from-beginning

/kafka/bin/kafka-console-producer.sh --broker-list kafka1:9092,kafka2:9092,kafka3:9092 --topic test-topic


### Create desired topics
/kafka/bin/kafka-topics.sh --zookeeper zookeeper:2181 --create --topic dtz-sensorthings --replication-factor 2 --partitions 3

/kafka/bin/kafka-topics.sh --zookeeper zookeeper:2181 --create --topic dtz-logging --replication-factor 1 --partitions 3

### Delete topics
/kafka/bin/zookeeper-shell.sh zookeeper:2181 ls /brokers/topics

/kafka/bin/zookeeper-shell.sh zookeeper:2181 rmr /brokers/topics/topicname


**Note**: That implementation doesn't work well, because docker must
load and recreate the image
after every restart from scratch. This is in docker swarm very complex.


# Install Kafka classically

[Official Quickstart Guide](https://kafka.apache.org/quickstart)

In step 6, use rename the config to 'il08k.properties' and change the
following lines:

broker.id=k
delete.topic.enable=true
log.dirs=/tmp/kafka-logs-k
zookeeper.connect=il081:2181

/kafka/bin/zookeeper-server-start.sh /kafka/config/zookeeper.properties
/kafka/bin/kafka-server-start.sh /kafka/config/il081.properties

Start on the il081 zookeeper and on all nodes kafka with the proper server config
 into the autostart script `~/.bashrc`:

/kafka/bin/zookeeper-server-start.sh -daemon /kafka/config/zookeeper.properties

/kafka/bin/kafka-server-start.sh -daemon /kafka/config/il08[k].properties


### Test the system
/kafka/bin/kafka-topics.sh --zookeeper il081:2181 --list

/kafka/bin/kafka-topics.sh --zookeeper il081:2181 --create --topic test-topic --replication-factor 2 --partitions 3

/kafka/bin/kafka-console-producer.sh --broker-list il081:9092,il082:9092,il083:9092 --topic test-topic

/kafka/bin/kafka-console-consumer.sh --bootstrap-server il081:9092,il082:9092,il083:9092 --topic test-topic --from-beginning


### Create desired topics
/kafka/bin/kafka-topics.sh --zookeeper il081:2181 --create --topic dtz.sensorthings --replication-factor 2 --partitions 3

/kafka/bin/kafka-topics.sh --zookeeper il081:2181 --create --topic dtz.logging --replication-factor 1 --partitions 3

### Delete topics
/kafka/bin/zookeeper-shell.sh il081:2181 ls /brokers/topics

/kafka/bin/zookeeper-shell.sh il081:2181 rmr /brokers/topics/topicname







