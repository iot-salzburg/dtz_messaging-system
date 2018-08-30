import time
import json
# from kafka import KafkaConsumer
# sudo apt-get install librdkafka-dev python-dev
from confluent_kafka import Consumer, KafkaError

# TODO create an adapter in python for polling data
# based on:
# channelID
# source own company name


KAFKA_TOPIC = 'dtz.sensorthings'

conf = {'bootstrap.servers': 'il081:9092,il082:9092,il083:9092',  # '192.168.48.81:9093,192.168.48.82:9094,192.168.48.83:9095',
        'group.id': 'testgroup',
        'default.topic.config': {'auto.offset.reset': 'smallest'}}

consumer = Consumer(**conf)
consumer.subscribe([KAFKA_TOPIC])

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
