import time
import json
# from kafka import KafkaConsumer
# sudo apt-get install librdkafka-dev python-dev
from confluent_kafka import Consumer, KafkaError

# TODO create an adapter in python for polling data
# based on:
# channelID
# source own company name


KAFKA_TOPIC_IN = "test-topic"

conf = {'bootstrap.servers': 'il081:9093,il082:9094,il083:9095',
        'group.id': 'testgroup',
        'default.topic.config': {'auto.offset.reset': 'smallest'}}

consumer = Consumer(**conf)
consumer.subscribe([KAFKA_TOPIC_IN])

print("Starting to poll")

running = True
while running:
    msg = consumer.poll(10)  # in ms
    if not msg:
        continue
    elif not msg.error():
        print('Received message: %s' % msg.value().decode('utf-8'))
    elif msg.error().code() != KafkaError._PARTITION_EOF:
        print(msg.error())
        running = False

consumer.close()
