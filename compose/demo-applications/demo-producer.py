#!/usr/bin/env python3

import time
import json
import os
import sys
import random
from confluent_kafka import Producer, KafkaError

__author__ = "Salzburg Research"
__version__ = "1.1"
__date__ = "14 August 2018"
__email__ = "christoph.schranz@salzburgresearch.at"
__status__ = "Development"

SPS = 1000  # samples per second
INTERVALL = 10  # time span to produce in s
# bottleneck is the p.produce function. it needs


KAFKA_TOPIC = 'test-topic-1'
BOOTSTRAP_SERVERS_default = 'il081,il082,il083'
KAFKA_GROUP_ID = "test-app"

# get bootstrap_servers from environment variable or use defaults and configure Consumer
conf = {'bootstrap.servers': BOOTSTRAP_SERVERS_default, 'group.id': KAFKA_GROUP_ID}
        # 'message.max.bytes': 15728640}
p = Producer(**conf)

startt = time.time()

while True:
    try:
        tt = time.time()
        # print("sending:", i)
        value = random.randint(0,10)
        # p.produce(KAFKA_TOPIC, json.dumps("Message {}, at {}".format(i, time.time())).encode('utf-8'))
        msg = json.dumps(value).encode('utf-8')
        p.produce(KAFKA_TOPIC, msg)

    except BufferError:
        p.flush()
        p.produce(KAFKA_TOPIC, json.dumps(value).encode('utf-8'))



