FROM jvsoest/converter

COPY workflows/workflow.cwl.yml /cwl_scripts/
COPY workflows/pentaho_tool.cwl.yml /cwl_scripts/

COPY workflows/settings_cwl.yml /config/

# Don't run as a service, but just once at startup
# RUN mv /etc/service/cwl_run/ /cwl_run


CMD ["/sbin/my_init"]