FROM landoop/fast-data-dev:cp4.0
#FROM landoop/fast-data-dev:1.1
MAINTAINER Christoph Schranz <christoph.schranz@salzburgresearch.at>

# Install required tools
RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

# Add scripts and install required libraries
RUN mkdir /home/src
WORKDIR /home/src
ADD src/* /home/src/
RUN pip install -r /home/src/requirements.txt

# Execute multiple scripts listed in the bash file
RUN chmod -R 755 /home/src
RUN chmod +x /home/src/run.sh

EXPOSE 2181 3030 3031 8081 8082 8083 9092
EXPOSE 3033

# Execute /home/src/run.sh
CMD ["/home/src/run.sh"]
