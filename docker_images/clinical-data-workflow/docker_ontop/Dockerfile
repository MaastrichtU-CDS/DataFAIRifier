FROM datafairifier/baseimage

RUN apt-get update && apt-get install -y wget unzip

RUN wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u141-b15/336fa29ff2bb4ef291e347e091f7f4a7/jdk-8u141-linux-x64.tar.gz
RUN tar -xzvf jdk-8u141-linux-x64.tar.gz

#RUN wget --no-check-certificate https://sourceforge.net/projects/ontop4obda/files/ontop-1.18.1/ontop-jetty-bundle-1.18.1.zip/download
#RUN mv download ontop_jetty.zip

COPY ontop-jetty-bundle-1.18.1.zip /ontop_jetty.zip

RUN unzip ontop_jetty.zip
RUN mv jetty-distribution-9.4.6.v20170531/ ontop_jetty/

COPY run /etc/service/ontop_jetty/
RUN chmod +x /etc/service/ontop_jetty/run

EXPOSE 8080