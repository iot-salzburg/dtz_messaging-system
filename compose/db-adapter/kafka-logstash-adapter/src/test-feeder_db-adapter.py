import os
import sys
import time
import json
import logging
from datetime import datetime
import pytz
from multiprocessing import Process
import requests
from flask import Flask, jsonify
from redis import Redis
from logstash import TCPLogstashHandler

import random

# confluent_kafka is based on librdkafka, details in requirements.txt
from confluent_kafka import Consumer, KafkaError

# logstash parameters
HOST_default = 'iot86'  # 'il060'  # 'logstash'  # important to set
PORT_default = 5000
STATUS_FILE = "status.log"

# webservice setup
app = Flask(__name__)
redis = Redis(host='redis', port=6379)


@app.route('/')
def print_adapter_status():
    """db-adapter
    This function is called by a sebserver request and prints the current meta information.
    :return:
    """
    try:
        with open(STATUS_FILE) as f:
            adapter_status = json.loads(f.read())
    except FileNotFoundError:
        adapter_status = {"application": "db-adapter",
                          "status": "initialisation"}
    return jsonify(adapter_status)


class KafkaStAdapter:
    def __init__(self, enable_kafka_adapter, enable_sensorthings):
        self.enable_kafka_adapter = enable_kafka_adapter
        self.enable_sensorthings = enable_sensorthings

    def stream_kafka(self):
        """
        This function configures a kafka consumer and a logstash logger instance.
        :returndb-adapter
        """

        # Init logstash logging
        logging.basicConfig(level='WARNING')
        logger_data = logging.getLogger("testlogger-data")
        logger_data.setLevel(logging.INFO)
        #  use default and init Logstash Handler
        logstash_handler_data = TCPLogstashHandler(host=HOST_default,
                                                   port=PORT_default,
                                                   version=1)
        logger_data.addHandler(logstash_handler_data)

        # Init logstash logging
        logging.basicConfig(level='WARNING')
        logger_logs = logging.getLogger("testlogger-logs")
        logger_logs.setLevel(logging.INFO)
        #  use default and init Logstash Handler
        logstash_handler_logs = TCPLogstashHandler(host=HOST_default,
                                                   port=PORT_default,
                                                   version=1)
        logger_logs.addHandler(logstash_handler_logs)

        # Set status and write to shared file
        adapter_status = {
            "application": "test-feeder_db-adapter",
            "status": "waiting for Logstash",
            "kafka input": "None",
            "logstash output": {
                "host": HOST_default,
                "port": PORT_default
            },
            "sensorthings mapping": {
                "enabled sensorthings": "No"
            },
            "version": {
                "number": "test"
            }
        }
        with open(STATUS_FILE, "w") as f:
            f.write(json.dumps(adapter_status))

        # time for logstash init
        logstash_reachable = False
        while not logstash_reachable:
            try:
                # use localhost if running local
                r = requests.get("http://" + HOST_default + ":9600")
                status_code = r.status_code
                if status_code in [200]:
                    logstash_reachable = True
            except:
                continue
            finally:
                time.sleep(0.25)

        # ready to stream flag
        adapter_status["status"] = "running"
        with open(STATUS_FILE, "w") as f:
            f.write(json.dumps(adapter_status))
        print("Adapter Status:", str(adapter_status))
        logger_data.info('Logstash reachable')

        while True:
            data = {'Datastream': {'@iot.id': 0, 'name': 'testdata'},
                    'phenomenonTime': datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat(),
                    'result': random.normalvariate(mu=0, sigma=1),
                    'resultTime': '2018-02-07T08:40:51.273061+00:00'}

            print(json.dumps(data))
            logger_data.info('', extra=data)
            time.sleep(5.0)

            log = "This is a logfile"
            print(log)
            logger_logs.info(log)

            time.sleep(5.0)


if __name__ == '__main__':
    # Load variables set by docker-compose, enable kafka as data input and sensorthings mapping by default
    enable_kafka_adapter = True
    if os.getenv('enable_kafka_adapter', "true") in ["false", "False", 0]:
        enable_kafka_adapter = False

    enable_sensorthings = True
    if os.getenv('enable_sensorthings', "true") in ["false", "False", 0]:
        enable_sensorthings = False

    # Create an kafka to logstash instance
    adapter_instance = KafkaStAdapter(enable_kafka_adapter, enable_sensorthings)

    # start kafka to logstash streaming in a subprocess
    kafka_streaming = Process(target=adapter_instance.stream_kafka, args=())
    kafka_streaming.start()

    app.run(host="0.0.0.0", debug=False, port=3031)
