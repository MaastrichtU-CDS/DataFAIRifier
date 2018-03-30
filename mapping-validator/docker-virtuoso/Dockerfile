FROM joernhees/virtuoso:7.2.4.2
MAINTAINER Martine de Vos


# Get and install vad package for rdb2rdf 
COPY ./rdb2rdf_dav.vad /import/rdb2rdf_dav.vad

RUN /etc/init.d/virtuoso-opensource-7 start \
&& isql-vt "EXEC=vad_install('/import/rdb2rdf_dav.vad');"\
&& /etc/init.d/virtuoso-opensource-7 stop


COPY run_and_import.sh /
RUN chmod +x /run_and_import.sh

COPY import_csv_data.isql /import/ 

ENTRYPOINT ["/run_and_import.sh"]
