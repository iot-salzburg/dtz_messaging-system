import time
import numpy as np
from confluent_kafka import Producer
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

BOOTSTRAP_SERVERS = 'il081:9093,il082:9094,il083:9095'
#BOOTSTRAP_SERVERS = 'localhost:9092'
# SCHEMA_REGISTRY_HOST = 'http://127.0.0.1:8082'


producer = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})
print("Successfully connected to the broker: {}".format(BOOTSTRAP_SERVERS))

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

while True:
    # Trigger any available delivery report callbacks from previous produce() calls
    producer.poll(0)

    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    randint = str(np.random.randn())
    print(randint)
    producer.produce('test', key='', value=randint.encode('utf-8'), callback=delivery_report)
    time.sleep(10)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()
