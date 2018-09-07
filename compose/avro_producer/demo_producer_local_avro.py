import time
import json
import numpy as np
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer


# BOOTSTRAP_SERVERS = 'localhost:9092'
# SCHEMA_REGISTRY_HOST = 'http://127.0.0.1:8082'


value_schema_str = """
{
   "namespace": "my.test",
   "name": "value",
   "type": "record",
   "fields" : [
     {
       "name" : "result",
       "type" : "double"
     }
   ]
}
"""

key_schema_str = """
{
   "namespace": "my.test",
   "name": "key",
   "type": "record",
   "fields" : [
     {
       "name" : "name",
       "type" : "string"
     }
   ]
}
"""

value_schema = avro.loads(value_schema_str)
key_schema = avro.loads(key_schema_str)
value = {"name": "Value"}
key = {"name": "Key"}

avroProducer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://127.0.0.1:8082'
    }, default_key_schema=key_schema, default_value_schema=value_schema)


#avroProducer.produce(topic='my_topic', value=value, key=key)
#avroProducer.flush()



# producer = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})
print("Successfully connected to the broker")

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

while True:
    # Trigger any available delivery report callbacks from previous produce() calls
    avroProducer.poll(0)

    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    value = dict({"name": str(np.random.randn())})
    key = {"name": "mykey"}
    print(value)
    avroProducer.produce(topic='avro-connect', value=value, key=key)
    avroProducer.flush()
    time.sleep(10)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.

