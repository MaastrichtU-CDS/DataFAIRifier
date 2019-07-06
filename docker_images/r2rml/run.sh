if [ -z "$SLEEPTIME" ]; then
    SLEEPTIME=60
    echo "SLEEPTIME set to $SLEEPTIME seconds"
fi

if [ -z "$DB_JDBC" ]; then
    DB_JDBC="jdbc:postgresql://dbhost/mydata"
    echo "DB_JDBC set to $DB_JDBC"
fi

if [ -z "$DB_USER" ]; then
    DB_USER="postgres"
    echo "DB_USER set to $DB_USER"
fi

if [ -z "$DB_PASS" ]; then
    DB_PASS="postgres"
    echo "DB_PASS set to $DB_PASS"
fi

if [ -z "$BASE_IRI" ]; then
    BASE_IRI="http://localhost/rdf/"
    echo "BASE_IRI set to $BASE_IRI"
fi

if [ -z "$R2RML_ENDPOINT" ]; then
    R2RML_ENDPOINT="http://graphdb:7200/repositories/r2rml"
    echo "R2RML_ENDPOINT set to $R2RML_ENDPOINT"
fi

if [ -z "$OUTPUT_ENDPOINT" ]; then
    OUTPUT_ENDPOINT="http://graphdb:7200/repositories/data"
    echo "OUTPUT_ENDPOINT set to $OUTPUT_ENDPOINT"
fi

if [ -z "$GRAPH_NAME" ]; then
    GRAPH_NAME="http://data.local/rdf"
    echo "GRAPH_NAME set to $GRAPH_NAME"
fi

echo "connectionURL = $DB_JDBC" > /config/r2rml.properties
echo "user = $DB_USER" >> /config/r2rml.properties
echo "password = $DB_PASS" >> /config/r2rml.properties
echo "mappingFile = /mapping.ttl" >> /config/r2rml.properties
echo "outputFile = /output.ttl" >> /config/r2rml.properties
echo "baseIRI = $BASE_IRI" >> /config/r2rml.properties
echo "format = TURTLE" >> /config/r2rml.properties

if [[ "$*" == "--debug" ]]
then
    python run.py $R2RML_ENDPOINT $OUTPUT_ENDPOINT $GRAPH_NAME "$@"
else
    while true
    do
        python run.py $R2RML_ENDPOINT $OUTPUT_ENDPOINT $GRAPH_NAME "$@"
        sleep $SLEEPTIME
    done
fi