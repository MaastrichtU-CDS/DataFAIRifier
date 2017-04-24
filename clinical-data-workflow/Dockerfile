FROM datafairifier/baseimage

# Define build packages here so we can remove them later
ENV BUILD_PACKAGES="wget"
ENV INSTALL_HOME="/opt"

# Set the front-end to noninteractive so debconf does not complain
ENV DEBIAN_FRONTEND noninteractive

# Switch to directory /opt
WORKDIR /opt

COPY installPentaho.sh installPentaho.sh
COPY pdi-ce-7.0.0.0-25.zip pdi-ce-7.0.0.0-25.zip 

# Make sure the file is executable
RUN chmod +x installPentaho.sh

RUN sh installPentaho.sh

EXPOSE 2020
