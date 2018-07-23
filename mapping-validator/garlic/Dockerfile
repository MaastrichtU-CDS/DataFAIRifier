FROM python:2-slim

RUN apt-get update && apt-get install -y git build-essential graphviz

RUN pip install --upgrade pip
RUN pip install git+https://github.com/c-martinez/grlc.git@candyGene
RUN pip install jupyter ipywidgets matplotlib pandas
RUN pip install psycopg2 psycopg2-binary sqlalchemy SPARQLWrapper pymssql graphviz
RUN jupyter nbextension enable --py widgetsnbextension

WORKDIR /root
RUN mkdir -p /.jupyter/custom/
COPY custom.js /.jupyter/custom/

RUN mkdir /queries
WORKDIR /queries

CMD gunicorn -c gunicorn_config.py grlc.server:app & jupyter notebook --port=8888 --ip=0.0.0.0 --allow-root --NotebookApp.token=''
