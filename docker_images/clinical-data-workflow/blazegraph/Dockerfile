FROM datafairifier/baseimage

RUN apt-get update && apt-get install -y wget

RUN wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u141-b15/336fa29ff2bb4ef291e347e091f7f4a7/jdk-8u141-linux-x64.tar.gz
RUN tar -xzvf jdk-8u141-linux-x64.tar.gz

RUN wget https://sourceforge.net/projects/bigdata/files/bigdata/2.1.4/blazegraph.jar/download
RUN mv download blazegraph.jar

COPY run /etc/service/blazegraph/
RUN chmod +x /etc/service/blazegraph/run

EXPOSE 9999