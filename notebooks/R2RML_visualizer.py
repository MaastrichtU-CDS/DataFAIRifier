import rdflib
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from graphviz import Digraph

class R2RML_visualizer:
    def __init__(self, loadNamespaces=None, loadTerminologies=None, excludePredicates=None, remoteTermEndpoint=None):
        self.termStore = rdflib.Graph()
        self.remoteTermStore = remoteTermEndpoint
        self.rmlStore = rdflib.Graph()
        self.rdfStore = None
        self.graph = None
        self.excludedLiteralPredicates = [ ]
        self.namespaces = {
            "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#": "ncit:",
            "http://www.cancerdata.org/roo/": "roo:",
            "http://mapping.local/": "map_",
            "http://purl.obolibrary.org/obo/UO_": "UO:",
            "http://www.w3.org/2001/XMLSchema#": "xsd:",
            "http://www.w3.org/2000/01/rdf-schema#": "rdfs:",
            "http://purl.bioontology.org/ontology/ICD10/": "icd:"
        }
        if loadNamespaces is not None:
            self.namespaces = loadNamespaces
        
        if loadTerminologies is not None:
            for url in loadTerminologies:
                self.termStore.load(url)
        
        if excludePredicates is not None:
            self.excludedLiteralPredicates = excludePredicates
    
    def loadScript(self, fileLocation, clear=False):
        if(clear):
            self.rmlStore = rdflib.Graph()
        self.rmlStore.parse(fileLocation, format="n3")
        
    def uploadR2RML(self, endpointUrl):
        rdfString = self.rmlStore.serialize(format='nt')
        # Create insert query
        insertQuery = "INSERT { %s } WHERE { }" % rdfString
        # Execute insert query
        endpoint = SPARQLWrapper(endpointUrl + "/statements")
        endpoint.setQuery(insertQuery)
        endpoint.method = "POST"
        try:
            endpoint.query()
            print("Mapping succesfully uploaded")
        except:
            print("Something went wrong during upload.")
    
    def uploadTermStore(self, endpointUrl):
        turtle = self.termStore.serialize(format='nt')
        try:
            loadRequest = requests.post(endpointUrl,
                data=turtle, 
                headers={
                    "Content-Type": "text/turtle"
                }
            )
            print("Mapping succesfully uploaded")
        except:
            print("Something went wrong during upload.")
    
    def clearRemoteR2RMLStore(self, endpointUrl):
        endpoint = SPARQLWrapper(endpointUrl + "/statements")
        endpoint.setQuery("DROP ALL;")
        endpoint.method = "POST"
        endpoint.query()
    
    def replaceToNamespace(self, uriObj):
        classString = str(uriObj)
        for key in self.namespaces.keys():
            classString = classString.replace(key, self.namespaces[key])
        return classString
    
    def plotGraph(self):
        # create new graphviz canvas
        self.graph = Digraph(comment='R2RML Structure', format="png")
        self.graph.node_attr.update(color='lightblue2', style='filled')
        
        # create in-memory rdf store and load mapping and terminologies
        self.rdfStore = rdflib.Graph()
        self.rdfStore.parse(data=self.rmlStore.serialize())
        self.rdfStore.parse(data=self.termStore.serialize())
        
        #loop over nodes and start plotting
        nodes = self.getNodes()
        for node in nodes:
            self.plotNode(node)
            
            # Get all object predicates
            predicateObjects = self.getNodeRelations(node)
            for predicateObject in predicateObjects:
                self.plotPredicatObjectForNode(node, predicateObject)
            
            # Get all literal predicates
            predicateLiterals = self.getNodeLiterals(node)
            for predicateLiteral in predicateLiterals:
                self.plotPredicateLiteralForNode(node, predicateLiteral)
        
        return self.graph
    
    def getNodes(self):
        res = self.rdfStore.query("""prefix rr: <http://www.w3.org/ns/r2rml#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?map ?mapClass
            WHERE {
                ?map a rr:TriplesMap.
                ?map rr:subjectMap [
                    rr:class ?mapClass
                ]
            }""")
        return res
    
    def getNodeRelations(self, node):
        res = self.rdfStore.query("""prefix rr: <http://www.w3.org/ns/r2rml#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?predicate ?otherMap
            WHERE {
                <%s> rr:predicateObjectMap [
                    rr:predicate ?predicate;
                    rr:objectMap [
                        rr:parentTriplesMap ?otherMap
                    ]
                ].
            }""" % str(node["map"]))
        return res
    
    def getNodeLiterals(self, node):
        res = self.rdfStore.query("""prefix rr: <http://www.w3.org/ns/r2rml#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?predicate ?literalType
            WHERE {
                <%s> rr:predicateObjectMap [
                    rr:predicate ?predicate;
                    rr:objectMap [
                        rr:datatype ?literalType
                    ]
                ]
            }""" % str(node["map"]))
        return res
    
    def getLabelForUri(self, uri, includeNewline=True):
        myQuery = """prefix rr: <http://www.w3.org/ns/r2rml#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?uriLabel
            WHERE {
                <%s> rdfs:label ?uriLabel.
            }""" % str(uri)
        
        if (len(self.termStore)>0):
            return self.getLabelForUriLocal(myQuery, includeNewline)
        else:
            if not self.remoteTermStore == None:
                return self.getLabelForUriRemote(myQuery, self.remoteTermStore, includeNewline)
    
    def getLabelForUriRemote(self, myQuery, endpoint, includeNewline):
        endpoint = SPARQLWrapper(endpoint)
        endpoint.setQuery(myQuery)
        endpoint.method = "POST"
        endpoint.setReturnFormat(JSON)
        results = endpoint.query().convert()

        for result in results["results"]["bindings"]:
            retVal = str(result["uriLabel"]["value"])
            if includeNewline:
                retVal + "\n"
            return retVal
        return ""
    
    def getLabelForUriLocal(self, myQuery, includeNewLine):
        res = self.rdfStore.query(myQuery)
        
        for row in res:
            retVal = str(row["uriLabel"])
            if includeNewline:
                retVal + "\n"
            return retVal
        return ""
    
    def plotNode(self, node):
        mapClass = self.replaceToNamespace(node["map"])
        targetClass = self.replaceToNamespace(node["mapClass"])
        targetClassLabel = self.getLabelForUri(node["mapClass"])
        self.graph.node(mapClass, targetClassLabel+"\n["+targetClass+"]")
    
    def plotPredicatObjectForNode(self, node, predicateObject):
        mapClass = self.replaceToNamespace(node["map"])
        predicateUri = self.replaceToNamespace(predicateObject["predicate"])
        predicateLabel = self.getLabelForUri(predicateObject["predicate"])
        objClass = self.replaceToNamespace(predicateObject["otherMap"])
        self.graph.edge(mapClass, objClass, predicateLabel+"\n["+predicateUri+"]")
    
    def plotPredicateLiteralForNode(self, node, predicateLiteral):
        mapClass = self.replaceToNamespace(node["map"])
        predicateUri = self.replaceToNamespace(predicateLiteral["predicate"])
        if predicateUri not in self.excludedLiteralPredicates:
            predicateLabel = self.getLabelForUri(predicateLiteral["predicate"])
            literal = self.replaceToNamespace(predicateLiteral["literalType"])
            
            nodeName = mapClass+"_"+literal.replace(":","_")
            self.graph.node(nodeName, "LITERAL\n["+literal+"]")
            self.graph.edge(mapClass, nodeName, predicateLabel+"\n["+predicateUri+"]")