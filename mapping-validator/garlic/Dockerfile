FROM python:2-slim

RUN apt-get update && apt-get install -y git build-essential unixodbc unixodbc-dev

RUN pip install --upgrade pip
RUN pip install git+https://github.com/c-martinez/grlc.git@candyGene
RUN pip install jupyter ipywidgets matplotlib pandas
RUN pip install psycopg2 sqlalchemy
RUN jupyter nbextension enable --py widgetsnbextension

COPY odbc /usr/lib/odbc
COPY odbc.ini /etc/odbc.ini

WORKDIR /root
RUN mkdir -p /.jupyter/custom/
COPY custom.js /.jupyter/custom/

RUN git clone https://github.com/maparent/virtuoso-python.git

WORKDIR /root/virtuoso-python
RUN pip install -r requirements.txt .

RUN mkdir /queries
# Instead of copy, use a mount
#ADD config.docker.ini /queries/config.ini
#ADD gunicorn_config.py /queries/
#ADD *.rq /queries/
#ADD *.ipynb /queries/

WORKDIR /queries

CMD gunicorn -c gunicorn_config.py grlc.server:app & jupyter notebook --port=8888 --ip=0.0.0.0 --allow-root --NotebookApp.token=''
