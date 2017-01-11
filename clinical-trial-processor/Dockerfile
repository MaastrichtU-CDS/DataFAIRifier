FROM datafairifier/baseimage

ENV BUILD_PACKAGES="wget"
ENV INSTALL_HOME="/opt"

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /opt
COPY install.sh install.sh
COPY run /etc/service/ctp/

RUN chmod +x /etc/service/ctp/run && chmod +x install.sh

RUN dpkg --add-architecture i386 && apt-get update && apt-get install -y libc6:i386 $BUILD_PACKAGES

RUN sh install.sh

RUN apt-get remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
    rm -rf /var/lib/apt/lists/*

COPY config.xml $INSTALL_HOME/CTP/

EXPOSE 8080
