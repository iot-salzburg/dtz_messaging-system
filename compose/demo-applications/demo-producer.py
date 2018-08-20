#!/usr/bin/env python3

import time
import json
import os
import sys
import random
import datetime
import pytz
from confluent_kafka import Producer, KafkaError

__author__ = "Salzburg Research"
__version__ = "1.1"
__date__ = "14 August 2018"
__email__ = "christoph.schranz@salzburgresearch.at"
__status__ = "Development"

#SPS = 1000  # samples per second
#INTERVALL = 10  # time span to produce in s
# bottleneck is the p.produce function. it needs


KAFKA_TOPIC = 'test-topic'
# The ports must be specified, as the default is 9092 for each one
BOOTSTRAP_SERVERS = 'il081:9093,il082:9094,il083:9095'
KAFKA_GROUP_ID = "test-app"

# get bootstrap_servers from environment variable or use defaults and configure Consumer
conf = {'bootstrap.servers': BOOTSTRAP_SERVERS, 'group.id': KAFKA_GROUP_ID}
        # 'message.max.bytes': 15728640}
p = Producer(**conf)

startt = time.time()

while True:
    msg = dict({"id": 0})
    msg["result"] = random.normalvariate(0, 1)
    msg["phenomenonTime"] = datetime.datetime.now().replace(tzinfo=pytz.UTC).isoformat()
    dumped_msg = json.dumps(msg).encode('utf-8')

    try:
        p.produce(KAFKA_TOPIC, dumped_msg)
        print("Produced: {}".format(msg))
    except BufferError:
        p.flush()
        print("Flushed")
        p.produce(KAFKA_TOPIC, dumped_msg)
        print("Produced: {}".format(msg))
    time.sleep(10)



