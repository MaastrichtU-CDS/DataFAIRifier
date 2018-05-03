from __future__ import print_function
from SPARQLWrapper import SPARQLWrapper, JSON
import ipywidgets as widgets
from IPython.display import clear_output
import pandas as pd

from comparisonEngine import ComparisonEngine

class R2RMLQueryEditor:
    def __init__(self, repoUrl, dbEngine):
        self.myWidgets = [ ]
        self.myButtons = dict()
        self.myCheckButtons = dict()
        self.r2rmlRepo = repoUrl
        self.dbEngine = dbEngine
        self.comparisonEngine = ComparisonEngine(dbEngine)

    def runQuery(self, endpointUrl, query):
        sparql = SPARQLWrapper(endpointUrl)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    def run_query_check(self, b):
        updateSet = self.myCheckButtons[b]
        sqlQuery = updateSet["textBox"].value.replace("\r", "").replace("\n", " ")
        myOutputBox = updateSet["output"]
        columnDef = updateSet["definition"]

        myOutputBox.clear_output()

        with myOutputBox:
            try:
                sqlResult = pd.read_sql_query(sqlQuery, self.dbEngine)

                print("SQL Count: ", sqlResult.shape[0])
                print("Expected columns: ", columnDef)
                for column in columnDef.split(","):
                    if (column not in sqlResult.columns.values):
                        print("Error: expected column ", column, " in the result, but it could not be found!")
                print(sqlResult)
            except Exception as e:
                print("Exception occured during query:", e)

    def run_query_check_silent(self, query, columnDef):
        errors = False
        message = ""
        try: 
            sqlResult = pd.read_sql_query(query, self.dbEngine)
            message += "Columns found: " + str(sqlResult.columns.values) + "\n"
            for column in columnDef.split(","):
                if (column not in sqlResult.columns.values):
                    errors = True
                    message += "Expected column " + column + " in the result, but it could not be found!\n"
        except Exception as e:
            errors = True
            message = e.message
        return errors, message

    def save_clicked(self, b):
        updateSet = self.myButtons[b]
        sqlQuery = updateSet["textBox"].value.replace("\r", "").replace("\n", " ")
        columnDef = updateSet["definition"]

        errors, message = self.run_query_check_silent(sqlQuery, columnDef)
        if errors:
            print("Aborting save. There were errors while checking the query:\n", message)
            return

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
            self.comparisonEngine.sqlQuery = sqlQuery
            print("Update executed. Please load this page again to make sure changes have applied to the database")
        except:
            print("Something went wrong during the update. Please check if the RDF repository is available.")
                

    def runInterface(self):
        queries = self.runQuery(self.r2rmlRepo, 
            """
            SELECT ?queryId ?query ?definition ?label
            WHERE {
                ?queryId <http://www.w3.org/ns/r2rml#sqlQuery> ?query.
                ?queryId <http://www.w3.org/2008/05/skos#definition> ?definition.
                ?queryId <http://www.w3.org/2000/01/rdf-schema#label> ?label.
            }
            """)

        for result in queries["results"]["bindings"]:
            myTextBox = widgets.Textarea(
                            value=result["query"]['value'],
                            placeholder=result["queryId"]['value'],
                            disabled=False,
                            rows=10,
                        )
            myDescription = widgets.HTML(value=("<p>" + result["label"]['value'] + "</p>"))
            myButton = widgets.Button(
                            description='Save',
                            disabled=False,
                            icon='check'
                        )
            self.myButtons[myButton] = {"textBox": myTextBox, "queryId": result["queryId"]['value'], "definition":  result["definition"]['value'] }
            myButton.on_click(self.save_clicked)

            checkButton = widgets.Button(
                            description='Check',
                            disabled=False,
                            icon='check'
                        )
            myOutputBox = widgets.Output(layout={'border': '1px solid black'})
            self.myCheckButtons[checkButton] = {"textBox": myTextBox, "output": myOutputBox, "definition":  result["definition"]['value'] }
            checkButton.on_click(self.run_query_check)

            self.myWidgets.append(
                widgets.HBox([
                    myTextBox,
                    widgets.VBox([
                            myDescription,
                            widgets.HBox([
                                checkButton,
                                myButton
                            ])
                    ]),
                ])
            )
            self.myWidgets.append(myOutputBox)
        return self.myWidgets