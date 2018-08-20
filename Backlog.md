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







________________________________________________________________________________________________

manually create docker-cluster. This solution with docker is harder than without docker
docker node update --label-add zoo=81 il081
docker node update --label-add kafka=81 il081
docker node update --label-add kafka=82 il082
docker node update --label-add kafka=83 il083

docker network create --driver overlay kafka-net


docker service create --name zookeeper   --mount type=volume,source=zoo-data,destination=/tmp/zookeeper --publish 2181:2181   --network kafka-net   --constraint node.labels.node==il081   --mode global   kafka:latest /kafka/bin/zookeeper-server-start.sh /kafka/config/zookeeper.properties


docker service create     --name kafka1     --mount type=volume,source=k1-logs,destination=/tmp/kafka-logs     --publish 9093:9093     --network kafka-net     --mode global     --constraint node.labels.node==il081 kafka:latest /kafka/bin/kafka-server-start.sh /kafka/config/server.properties --override listeners=INT://:9092,EXT://0.0.0.0:9093  --override listener.security.protocol.map=INT:PLAINTEXT,EXT:PLAINTEXT --override inter.broker.listener.name=INT --override advertised.listeners=INT://:9092,EXT://il081:9093  --override zookeeper.connect=zookeeper:2181  --override broker.id=1


docker service create  --name kafka2   --mount type=volume,source=k2-logs,destination=/tmp/kafka-logs   --publish 9094:9094   --network kafka-net   --mode global   --constraint node.labels.node==il082 kafka:latest /kafka/bin/kafka-server-start.sh /kafka/config/server.properties  --override listeners=INT://:9092,EXT://0.0.0.0:9094  --override listener.security.protocol.map=INT:PLAINTEXT,EXT:PLAINTEXT  --override inter.broker.listener.name=INT  --override advertised.listeners=INT://:9092,EXT://il082:9094  --override zookeeper.connect=zookeeper:2181  --override broker.id=2


docker service create  --name kafka3   --mount type=volume,source=k2-logs,destination=/tmp/kafka-logs   --publish 9095:9095   --network kafka-net   --mode global   --constraint node.labels.node==il083 kafka:latest /kafka/bin/kafka-server-start.sh /kafka/config/server.properties  --override listeners=INT://:9092,EXT://0.0.0.0:9095  --override listener.security.protocol.map=INT:PLAINTEXT,EXT:PLAINTEXT  --override inter.broker.listener.name=INT  --override advertised.listeners=INT://:9092,EXT://il083:9095  --override zookeeper.connect=zookeeper:2181  --override broker.id=3


Testing the installation

/kafka/bin/kafka-topics.sh --list --zookeeper zookeeper:2181

/kafka/bin/kafka-topics.sh  --zookeeper zookeeper:2181 --create --replication-factor 1 --partitions 1 --topic test

/kafka/bin/kafka-console-producer.sh --broker-list kafka1:9093 --topic test

/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka1:9093 --topic test --from-beginning
/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka2:9094 --topic test --from-beginning
/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka3:9095 --topic test --from-beginning



git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch compose/kafka-medium/base-image/kafka_2.11-1.1.0.tgz' --prune-empty --tag-name-filter cat -- --all







