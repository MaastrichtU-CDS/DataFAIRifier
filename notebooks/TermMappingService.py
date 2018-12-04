from SPARQLWrapper import SPARQLWrapper, JSON
from IPython.display import clear_output
import rdflib
import ipywidgets as widgets
import collections

class TermMappingService:
    def __init__(self, repoUrl, terminologyUrl):
        self.rdfRepo = repoUrl
        self.queryLocalTerms = """PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?type ?value
FROM <http://www.ontotext.com/explicit>
WHERE {
	?obj rdf:type ?type.
    ?obj roo:local_value ?value .
    FILTER(?type NOT IN (owl:NamedIndividual, owl:Thing)).
}
ORDER BY ?type"""
        self.ontologyGraph = rdflib.Graph()
        self.ontologyGraph.load(terminologyUrl)
        self.myWidgets = [ ]
        self.myButtonList = dict()
        self.myMappedWidgets = [ ]
        self.myDeleteButtonList = dict()
    
    def runQuery(self, query):
        sparql = SPARQLWrapper(self.rdfRepo)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()
    
    def printLocalValues(self):
        localValues = self.runQuery(self.rdfRepo, self.queryLocalTerms)
        for localValue in localValues["results"]["bindings"]:
            print(localValue["type"]["value"] + ": " + localValue["value"]["value"])
    
    def getLocalMappings(self):
        query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX roo: <http://www.cancerdata.org/roo/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            SELECT ?term ?superClass ?localValue
            FROM <http://www.ontotext.com/explicit>
            WHERE {
                ?term owl:equivalentClass [
                    rdf:type owl:Class;
                    owl:intersectionOf [
                        rdf:first ?superClass;
                        rdf:rest [
                            rdf:first [
                                rdf:type owl:Class;
                                owl:unionOf [
                                    rdf:first [
                                        rdf:type owl:Restriction;
                                        owl:hasValue ?localValue;
                                        owl:onProperty roo:local_value;
                                    ];
                                    rdf:rest rdf:nil;
                                ]
                            ];
                            rdf:rest rdf:nil;
                        ]
                    ]
                ].
            }
        """
        foundMappings = self.runQuery(query)
        mappings = [ ]
        for foundMapping in foundMappings["results"]["bindings"]:
            mappings.append({"term": foundMapping["term"]["value"],
                             "superClass": foundMapping["superClass"]["value"],
                             "localValue": foundMapping["localValue"]["value"],
                             "termLabel": self.getLabelForClass(foundMapping["term"]["value"]),
                             "superClassLabel": self.getLabelForClass(foundMapping["superClass"]["value"])})
        return mappings
            
    def getMappingsForValues(self, superClass, localValue):
        query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX roo: <http://www.cancerdata.org/roo/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            SELECT ?term
            FROM <http://www.ontotext.com/explicit>
            WHERE {
                ?term owl:equivalentClass [
                    rdf:type owl:Class;
                    owl:intersectionOf [
                        rdf:first <%s>;
                        rdf:rest [
                            rdf:first [
                                rdf:type owl:Class;
                                owl:unionOf [
                                    rdf:first [
                                        rdf:type owl:Restriction;
                                        owl:hasValue "%s"^^xsd:string;
                                        owl:onProperty roo:local_value;
                                    ];
                                    rdf:rest rdf:nil;
                                ]
                            ];
                            rdf:rest rdf:nil;
                        ]
                    ]
                ].
            }
        """ % (superClass, localValue)
        foundTerms = self.runQuery(query)
        terms = [ ]
        for foundTerm in foundTerms["results"]["bindings"]:
            terms.append(foundTerm["term"]["value"])
        return terms
            
    def delete_reasoning(self, localValue, superClass, term):
        query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX roo: <http://www.cancerdata.org/roo/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            DELETE {
            GRAPH <http://data.local/mapping> {
                <%s> owl:equivalentClass ?p1.
                ?p1 rdf:type owl:Class.
                ?p1 owl:intersectionOf ?p2.
                        ?p2 rdf:first <%s>.
                        ?p2 rdf:rest ?p3.
                            ?p3 rdf:first ?p4.
                                ?p4 rdf:type owl:Class.
                                ?p4 owl:unionOf ?p5.
                                    ?p5 rdf:first ?p6.
                                        ?p6 rdf:type owl:Restriction.
                                        ?p6 owl:hasValue "%s"^^xsd:string.
                                        ?p6 owl:onProperty roo:local_value.
                                    ?p5 rdf:rest rdf:nil.
                            ?p3 rdf:rest rdf:nil.
            } } WHERE {
                <%s> owl:equivalentClass ?p1.
                ?p1 rdf:type owl:Class.
                ?p1 owl:intersectionOf ?p2.
                        ?p2 rdf:first <%s>.
                        ?p2 rdf:rest ?p3.
                            ?p3 rdf:first ?p4.
                                ?p4 rdf:type owl:Class.
                                ?p4 owl:unionOf ?p5.
                                    ?p5 rdf:first ?p6.
                                        ?p6 rdf:type owl:Restriction.
                                        ?p6 owl:hasValue "%s"^^xsd:string.
                                        ?p6 owl:onProperty roo:local_value.
                                    ?p5 rdf:rest rdf:nil.
                            ?p3 rdf:rest rdf:nil.
            }""" % (term, superClass, localValue, term, superClass, localValue)
        #print(query)

        sparql = SPARQLWrapper(self.rdfRepo + "/statements")
        sparql.setQuery(query)
        sparql.method = "POST"

        try:
            sparql.query()
            print("Mapping removed, please reload the page to see the effect.")
        except:
            print("Something went wrong during the update. Please check if the RDF repository is available.")
    
    def save_reasoning(self, localValue, superClass, term):
        query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX roo: <http://www.cancerdata.org/roo/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            INSERT {
            GRAPH <http://data.local/mapping> {
                <%s> owl:equivalentClass [
                    rdf:type owl:Class;
                    owl:intersectionOf [
                        rdf:first <%s>;
                        rdf:rest [
                            rdf:first [
                                rdf:type owl:Class;
                                owl:unionOf [
                                    rdf:first [
                                        rdf:type owl:Restriction;
                                        owl:hasValue "%s"^^xsd:string;
                                        owl:onProperty roo:local_value;
                                    ];
                                    rdf:rest rdf:nil;
                                ]
                            ];
                            rdf:rest rdf:nil;
                        ]
                    ]
                ].
            } } WHERE { }
        """ % (term, superClass, localValue)
        #print(query)

        sparql = SPARQLWrapper(self.rdfRepo + "/statements")
        sparql.setQuery(query)
        sparql.method = "POST"

        try:
            sparql.query()
            print("Mapping saved, please reload the page to see the effect.")
        except:
            print("Something went wrong during the update. Please check if the RDF repository is available.")
    
    def save_action(self, b):
        myButtonObjects = self.myButtonList[b]
        
        #loop over all entries for this dropdown, to find the correct ID
        uri = None
        label = None
        for entry in myButtonObjects["classList"]:
            if(entry["id"] == myButtonObjects["dropdown"].value):
                uri = entry["uri"]
                label = entry["label"]
        if (uri is not None) & (label is not None):
            self.save_reasoning(myButtonObjects["localValue"], myButtonObjects["superClass"], uri)
      
    def delete_action(self, b):
        myButtonObjects = self.myDeleteButtonList[b]
        
        #delete the actual reasoning
        self.delete_reasoning(myButtonObjects["localValue"],
                            myButtonObjects["superClass"],
                            myButtonObjects["term"])
    
    def getLabelForClass(self, classUri):
        
        myQuery = "SELECT ?label WHERE { <%s> rdfs:label ?label. }" % classUri
        for row in self.ontologyGraph.query(myQuery):
            return str(row.label)
        return "noLabel"
        
    def initMappedValues(self):
        localMappings = self.getLocalMappings()
        
        #remove previous mapping widgets (if they exist)
        self.myMappedWidgets = [ ]
        self.myDeleteButtonList = dict()
        
        for localMapping in localMappings:
            mappedValueWidget = widgets.Text(value=localMapping["localValue"], disabled=True, description=localMapping["superClassLabel"] + ":", style={"description_width": "initial"})
            standardTermWidget = widgets.Text(value=localMapping["termLabel"], disabled=True)
            
            # create save button
            deleteWidget = widgets.Button(
                description="Delete",
                icon='remove',
            )
            
            self.myDeleteButtonList[deleteWidget] = localMapping
            deleteWidget.on_click(self.delete_action)
            
            self.myMappedWidgets.append(widgets.HBox([mappedValueWidget, standardTermWidget, deleteWidget]))
        return self.myMappedWidgets
    
    def initInterface(self):
        localValues = self.runQuery(self.queryLocalTerms)
        
        # remove previous stored values (if they exist)
        self.myWidgets = [ ]
        self.myButtonList = dict()
        
        #loop over all found local values
        for localValue in localValues["results"]["bindings"]:
            superClass = localValue["type"]["value"]
            localValue = localValue["value"]["value"]
            
            # if there exists a rule for a given local value and superclass, then ignore this value
            if len(self.getMappingsForValues(superClass, localValue)) > 0:
                continue

            # check the rdfs:label for superclass
            superClassName = self.getLabelForClass(superClass)

            # create textfield with the local value as text, superclass label as description
            valueWidget = widgets.Text(value=localValue, disabled=True, description=superClassName, style={"description_width": "initial"})

            # lookup subclasses (possible matching candidates)
            myQuery = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                SELECT ?subClass ?label 
                WHERE { 
                    ?subClass rdfs:subClassOf* <%s>.
                    ?subClass rdfs:label ?label.

                    FILTER (?subClass != <%s>).
                }
                ORDER BY ?label""" % (superClass, superClass)
            queryResult = self.ontologyGraph.query(myQuery)

            # make list for dropdown
            classList = list()
            i=0
            for subClassResultRow in queryResult:
                classList.append({"uri": str(subClassResultRow.subClass), "label": str(subClassResultRow.label), "id": i})
                i = i+1

            dropdownValues = dict()
            selectedId = 0
            for myClass in classList:
                dropdownValues[myClass["label"]] = myClass["id"]
                ##add here to set the value

            dropdownValues = collections.OrderedDict(sorted(dropdownValues.items()))

            # create dropdown
            standardValWidget = widgets.Dropdown(
                options=dropdownValues
            )
            
            if len(dropdownValues)>0 :
                standardValWidget = widgets.Dropdown(
                    options=dropdownValues,
                    value=selectedId
                )

            # create save button
            saveWidget = widgets.Button(
                description="Save",
                icon='save',
            )

            self.myButtonList[saveWidget] = {"superClass": superClass, "localValue": localValue, "dropdown": standardValWidget, "classList": classList}
            saveWidget.on_click(self.save_action)

            #align all three widget objects
            self.myWidgets.append(widgets.HBox([valueWidget, standardValWidget, saveWidget]))
        return self.myWidgets