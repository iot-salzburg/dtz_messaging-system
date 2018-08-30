import time
import json
import json
# from kafka import KafkaConsumer
# sudo apt-get install librdkafka-dev python-dev
from confluent_kafka import Consumer, KafkaError

# TODO create an adapter in python for polling data
# based on:
# channelID
# source own company name


KAFKA_TOPIC_IN = "test3"

conf = {'bootstrap.servers': 'localhost:9093',
        'group.id': 'mygroup',
        'default.topic.config': {'auto.offset.reset': 'smallest'}}

consumer = Consumer(**conf)
consumer.subscribe([KAFKA_TOPIC_IN])

print("Starting to poll")

try:
    while True:
        msg = consumer.poll(10)  # in ms
        if not msg.error():
            payload = json.loads(msg.value().decode('utf-8'))
            print(payload)
        elif msg.error().code() != KafkaError._PARTITION_EOF:
            print(msg.error())
            break

except KeyboardInterrupt:
    print("Closed Connection to {}".format(conf["bootstrap.servers"]))
finally:
    consumer.close()
