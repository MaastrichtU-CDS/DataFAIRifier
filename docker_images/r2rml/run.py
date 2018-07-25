import json
import requests
import urllib
import os
import subprocess

if(os.path.exists("mapping.ttl")):
    os.remove("mapping.ttl")
if(os.path.exists("out.ttl")):
    os.remove("out.ttl")

baseUrl = "http://graphdb:7200"
localGraph = "http://data.local/rdf"

#####################
# Get R2RML triples & store in file
#####################
response_r2rml = requests.post(baseUrl + "/repositories/r2rml", 
    data="CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o }", 
    headers={
        "Content-Type": "application/sparql-query",
        "Accept": "application/x-turtle"
    }
)
text_file = open("mapping.ttl", "w")
text_file.write(response_r2rml.text)
text_file.close()

#####################
# Run Ontop R2RML
#####################
cmdSteps = ["java", "-jar", "r2rml.jar", "/config/r2rml.properties"]
sink = subprocess.check_output(cmdSteps)

#####################
# Clear RDF store
#####################
transactionRequest = requests.post(baseUrl + "/repositories/data/transactions", 
    headers={
        "Accept": "application/json"
    }
)
transactionUrl = transactionRequest.headers["Location"]
query = "DROP GRAPH <%s>" % localGraph
dropRequest = requests.put(transactionUrl + "?action=UPDATE&update=%s" % query)
commitRequest = requests.put(transactionUrl + "?action=COMMIT")

#####################
# Load RDF store with new data
#####################

turtle = ""
with open('/output.ttl', 'r') as myfile:
    turtle=myfile.read()

loadRequest = requests.post((baseUrl + "/repositories/data/statements?context=%3C" + localGraph + "%3E"),
    data=turtle, 
    headers={
        "Content-Type": "application/x-turtle"
    }
)