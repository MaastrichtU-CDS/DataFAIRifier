FROM maven:3.5.2-jdk-8

RUN apt-get update && apt-get install -y python-pip
RUN pip install requests

RUN git clone https://github.com/jvsoest/r2rml.git

RUN cd /r2rml && \
    git fetch && \
    git checkout OracleIgnore && \
    mvn package && \
    mvn dependency:copy-dependencies

RUN cd /r2rml/target && \
    cp r2rml.jar /r2rml.jar && \
    cp -R dependency/ /dependency/

RUN mkdir /config

COPY run.py /run.py
COPY run.sh /run.sh

CMD ["sh", "run.sh"]

# docker build -t jvsoest/workflow2 ./