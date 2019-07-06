import json
import requests
import urllib
import os
import subprocess
import sys
from subprocess import Popen, PIPE

if(os.path.exists("mapping.ttl")):
    os.remove("mapping.ttl")
if(os.path.exists("out.ttl")):
    os.remove("out.ttl")

r2rmlEndpoint = sys.argv[1]
outputEndpoint = sys.argv[2]
graphName = sys.argv[3]

baseUrl = "http://graphdb:7200"

#####################
# Get R2RML triples & store in file
#####################
if "--debug" not in sys.argv:
    response_r2rml = requests.post(r2rmlEndpoint, 
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
cmdSteps = "java -jar r2rml.jar /config/r2rml.properties"
p = subprocess.Popen(cmdSteps, stdout=PIPE, stderr=PIPE, shell=True)
out, err = p.communicate()

if "--debug" in sys.argv:
    print(out.decode("utf-8"))
    print(err.decode("utf-8"))
    sys.exit()

#####################
# Clear RDF store
#####################
transactionRequest = requests.post(outputEndpoint + "/transactions", 
    headers={
        "Accept": "application/json"
    }
)
transactionUrl = transactionRequest.headers["Location"]
query = "DROP GRAPH <%s>" % graphName
dropRequest = requests.put(transactionUrl + "?action=UPDATE&update=%s" % query)
commitRequest = requests.put(transactionUrl + "?action=COMMIT")

#####################
# Load RDF store with new data
#####################

turtle = ""
with open('/output.ttl', 'r') as myfile:
    turtle=myfile.read()

loadRequest = requests.post((outputEndpoint + "/statements?context=%3C" + graphName + "%3E"),
    data=turtle, 
    headers={
        "Content-Type": "application/x-turtle"
    }
)