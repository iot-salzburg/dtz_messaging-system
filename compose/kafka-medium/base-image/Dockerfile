# Dockerfile
FROM ubuntu:16.04

# Install jdk
RUN apt-get update && apt-get install openjdk-8-jre wget -y

# Unzip kafka zip and rename at kafka
ENV kafka_version=0.11.0.3
RUN wget https://archive.apache.org/dist/kafka/${kafka_version}/kafka_2.11-${kafka_version}.tgz
RUN tar -xvzf kafka_2.11-${kafka_version}.tgz
RUN mkdir /kafka
RUN mv kafka_2.11-${kafka_version}/* /kafka
# ADD ./kafka_${kafka_version}.tgz ./

