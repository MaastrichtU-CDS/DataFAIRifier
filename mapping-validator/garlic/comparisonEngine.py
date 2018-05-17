from __future__ import print_function

import requests
import pandas as pd
import matplotlib as plt
from StringIO import StringIO

from ipywidgets import interact, interactive, fixed, interact_manual
from ipykernel.pylab.backend_inline import flush_figures

from resultWidget import ResultWidget
import sqlalchemy

class ComparisonEngine:
    def __init__(self, engine, query_base_path = '/queries/', base_url = 'http://localhost:8088/api/local/local'):
        self.dbEngine = engine
        self.query_base_path = query_base_path
        self.base_url = base_url
        self.sqlQuery = None
        self.plot_kinds = ['line', 'bar', 'hist', 'box', 'density', 'area', 'scatter', 'hexbin', 'pie']
        self.sqlResult = None
        self.sparqlResult = None

        self.metadata = sqlalchemy.MetaData()
        self.metadata.reflect(self.dbEngine)

    def callAPI(self, query, params={}, parse_dates=None):
        headers = {"Accept": "text/csv"}
        query_url = self.base_url + query
        
        resp = requests.get(query_url, headers=headers,  params=params)
        # boldly assuming response was code 200
        df = pd.read_csv(StringIO(resp.text), parse_dates=parse_dates)
        return df

    def getSparqlResult(self, name, parse_dates=None):
        df = self.callAPI('/' + name, params={}, parse_dates=parse_dates)
        return df

    def getSqlResult(self, name, parse_dates=None):
        return pd.read_sql_query(self.sqlQuery, self.dbEngine, parse_dates=parse_dates)

    def getSqlResultByQuery(self, query):
        return pd.read_sql_query(query, self.dbEngine)

    def loadDatasets(self, name, sqlDateColumns=None, sparqlDateColumns=None):
        if self.sqlQuery is None:
            raise Exception("sqlQuery has not yet been saved!")
        sql = self.getSqlResult(name, parse_dates=sqlDateColumns)
        
        sparql = self.getSparqlResult(name, parse_dates=sparqlDateColumns)
        
        return sql, sparql

    def drawGraph(self, sqlX, sqlY, sparqlX, sparqlY, kind='bar', figsize=(12, 6)):       
        fig, axes = plt.pyplot.subplots(1, 2, figsize=figsize)
        self.sqlResult[sqlY].value_counts().plot(ax=axes[0], kind=kind)
        self.sparqlResult[sparqlY].value_counts().plot(ax=axes[1], kind=kind)

        axes[0].set_title("SQL Result Graph: " + sqlY)
        axes[1].set_title("SPARQL Result Graph: " + sparqlY)
        flush_figures()
    
    def interact(self, figsize=(12, 6)):
        self.sqlWidgets = ResultWidget(self.sqlResult, 'SQL')
        self.sparqlWidgets = ResultWidget(self.sparqlResult, 'SPARQL')
        self.sqlInteract = interact_manual(self.drawGraph,
                                           sqlX=self.sqlWidgets.x_widget, sqlY=self.sqlWidgets.y_widget, 
                                           sparqlX=self.sparqlWidgets.x_widget, sparqlY=self.sparqlWidgets.y_widget,
                                           kind=self.plot_kinds, figsize=fixed(figsize))
        
    def getTables(self):
        return self.metadata.tables.keys()

    def getTableColumns(self, table):
        t = self.metadata.tables[table]
        return [(c.name, c.type) for c in t.columns]

    def load(self, sparqlName, sqlDateColumns=[], sparqlDateColumns=[]):
        self.sqlResult, self.sparqlResult = self.loadDatasets(sparqlName, sqlDateColumns=[], sparqlDateColumns=[])

        print("SQL Columns: ", self.sqlResult.columns.values)
        print("RDF Columns: ", self.sparqlResult.columns.values)

        print("SQL Count: ", self.sqlResult.shape[0])
        print("RDF Count: ", self.sparqlResult.shape[0])