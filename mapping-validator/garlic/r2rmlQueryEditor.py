from SPARQLWrapper import SPARQLWrapper, JSON
import ipywidgets as widgets

class R2RMLQueryEditor:
    def __init__(self, repoUrl):
        self.myWidgets = [ ]
        self.myButtons = dict()
        self.r2rmlRepo = repoUrl

    def runQuery(self, endpointUrl, query):
        sparql = SPARQLWrapper(endpointUrl)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    def save_clicked(self, b):
        updateSet = self.myButtons[b]
        sqlQuery = updateSet["textBox"].value.replace("\r", "").replace("\n", " ")
        query = """
            DELETE {
              <%s> <http://www.w3.org/ns/r2rml#sqlQuery> ?query.
            } WHERE {
              <%s> <http://www.w3.org/ns/r2rml#sqlQuery> ?query.
            };

            INSERT {
              <%s> <http://www.w3.org/ns/r2rml#sqlQuery> "%s".
            } WHERE { }
            """ % (updateSet["queryId"], updateSet["queryId"], updateSet["queryId"], sqlQuery)
        sparql = SPARQLWrapper(self.r2rmlRepo + "/statements")
        sparql.setQuery(query)
        sparql.method = "POST"
        
        try:
            sparql.query()
            print("Update executed. Please load this page again to make sure changes have applied to the database")
        except:
            print("Something went wrong during the update. Please check if the RDF repository is available.")
                

    def runInterface(self):
        queries = self.runQuery(self.r2rmlRepo, 
            """
            SELECT ?queryId ?query ?definition
            WHERE {
                ?queryId <http://www.w3.org/ns/r2rml#sqlQuery> ?query.
                OPTIONAL { ?queryId <http://www.w3.org/2004/02/skos/core#defintition> ?definition }
            }
            """)

        for result in queries["results"]["bindings"]:
            myTextBox = widgets.Textarea(
                            value=result["query"]['value'],
                            placeholder=result["queryId"]['value'],
                            disabled=False,
                            rows=10,
                        )
            myDescription = widgets.HTML(value=("<p>" + result["definition"]['value'] + "</p>"))
            myButton = widgets.Button(
                            description='Save',
                            disabled=False,
                            icon='check'
                        )
            self.myButtons[myButton] = {"textBox": myTextBox, "queryId": result["queryId"]['value'] }
            myButton.on_click(self.save_clicked)

            self.myWidgets.append(
                widgets.HBox([
                    myTextBox,
                    widgets.VBox([
                            myDescription,
                            myButton
                    ])
                ])
            )
        return self.myWidgets