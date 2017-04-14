# Elastalert Docker image running on Ubuntu 15.04.
# Build image with: docker build -t ivankrizsan/elastalert:v1 .

FROM ubuntu:15.04

MAINTAINER jetyang, https://github.com/jetyang


#header

# URL from which to download Elastalert.
ENV ELASTALERT_URL https://github.com/jetyang2005/elastalert/archive/0.2.0.zip
# Directory to which Elastalert and Supervisor logs are written.
ENV LOG_DIR /opt/logs
# Elastalert home directory name.
ENV ELASTALERT_DIRECTORY_NAME elastalert
# Elastalert home directory full path.
ENV ELASTALERT_HOME /opt/${ELASTALERT_DIRECTORY_NAME}
# Alias, DNS or IP of Elasticsearch host to be queried by Elastalert. Set in default Elasticsearch configuration file.
ENV ELASTICSEARCH_HOST elasticsearch_host
# Port on above Elasticsearch host. Set in default Elasticsearch configuration file.
ENV ELASTICSEARCH_PORT 9200

WORKDIR /opt

# Install software required for Elastalert.
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y wget python python-dev unzip gcc python-mysqldb && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \

# Install pip - required for installation of Elastalert.
    wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py && \
# Download and unpack Elastalert.
    wget ${ELASTALERT_URL} && \
    unzip *.zip && \
    rm *.zip && \
    mv e* ${ELASTALERT_DIRECTORY_NAME}

WORKDIR ${ELASTALERT_HOME}

# Install Elastalert.
RUN python setup.py install && \
#    python ${ELASTALERT_HOME}/DBUtils-1.2/setup.py install && \
    pip install -e . && \
    pip install MySQL-python && \


# Create directories.
    mkdir ${LOG_DIR}


# Define mount points.
VOLUME [ "${LOG_DIR}" ]

# Launch Elastalert when a container is started.
CMD ["python", "elastalert/elastalert.py", "--verbose"]