# Dockerfile
FROM ubuntu:16.04

# Install jdk
RUN apt-get update && apt-get install openjdk-8-jre wget -y

# Unzip kafka zip and rename at kafka
ENV kafka_version=0.11.0.3
RUN wget https://archive.apache.org/dist/kafka/${kafka_version}/kafka_2.11-${kafka_version}.tgz
RUN tar -xvzf kafka_2.11-${kafka_version}.tgz
RUN rm kafka_2.11-${kafka_version}.tgz
RUN mv kafka_2.11-${kafka_version} /kafka

# Create initial topics
#ADD bootstrap.sh /bootstrap.sh
#RUN chmod +x /bootstrap.sh
#RUN /bootstrap.sh

