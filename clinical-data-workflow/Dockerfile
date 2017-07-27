FROM datafairifier/baseimage

# Define build packages here so we can remove them later
ENV BUILD_PACKAGES="wget"
ENV INSTALL_HOME="/opt"

# Set the front-end to noninteractive so debconf does not complain
ENV DEBIAN_FRONTEND noninteractive

COPY workflows/d2r_tool.cwl.yml d2r_tool.cwl.yml
COPY workflows/pentaho_tool.cwl.yml pentaho_tool.cwl.yml
COPY workflows/curl.cwl.yml curl.cwl.yml
COPY workflows/workflow.cwl.yml workflow.cwl.yml

COPY workflows/load_csv_to_db.ktr load_csv_to_db.ktr
COPY workflows/settings_cwl.yml settings_cwl.yml

COPY workflows/registry_mapping.ttl registry_mapping.ttl

COPY workflows/data/thunderSubSet.csv thunderSubSet.csv

# Switch to directory /opt
WORKDIR /opt

COPY install.sh install.sh
COPY pdi-ce-7.1.0.0-12.zip pdi-ce-7.1.0.0-12.zip
COPY d2rq-0.8.3-dev.zip d2rq-0.8.3-dev.zip

# Make sure the file is executable
RUN chmod +x install.sh

RUN sh install.sh

COPY run /etc/service/cwl_run/
RUN chmod +x /etc/service/cwl_run/run

EXPOSE 2020