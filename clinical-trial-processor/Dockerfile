#
# This image is built automatically on http://hub.docker.com/datafairifier/ctp-baseimage
#
FROM datafairifier/baseimage

# Define build packages here so we can remove them later
ENV BUILD_PACKAGES="wget"
ENV INSTALL_HOME="/opt"

# Set the front-end to noninteractive so debconf does not complain
ENV DEBIAN_FRONTEND noninteractive

# Switch to directory /opt
WORKDIR /opt
# The install script to install java, java-image-io and ctp
COPY install.sh install.sh

# This run script is run by the base image as a service
# The run script contains a exec command that starts the daemon
COPY run /etc/service/ctp/

# Make sure they are executable
RUN chmod +x /etc/service/ctp/run && chmod +x install.sh

# Install the dependencies
RUN dpkg --add-architecture i386 && apt-get update && apt-get install -y libc6:i386 $BUILD_PACKAGES

# Actually install java, java-image-io and ctp
RUN sh install.sh

# Remove the now unnecessary packages to keep the image small.
RUN apt-get remove --purge -y $BUILD_PACKAGES && \
    rm -rf /var/lib/apt/lists/*

# An empty base configuration
COPY config.xml $INSTALL_HOME/CTP/

# Make sure the container accepts connections on port 8080
EXPOSE 8080
