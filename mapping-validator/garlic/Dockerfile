FROM python:2-slim

# RUN apk update
RUN apt-get update
# RUN apk add git gcc python-dev musl-dev libzmq zeromq-dev libpng freetype-dev
RUN apt-get install -y git gcc

RUN pip install git+https://github.com/c-martinez/grlc.git@candyGene
RUN pip install jupyter ipywidgets matplotlib pandas
RUN pip install psycopg2 sqlalchemy
RUN jupyter nbextension enable --py widgetsnbextension

WORKDIR /root

RUN mkdir -p /.jupyter/custom/
COPY custom.js /.jupyter/custom/

RUN mkdir /queries
# Instead of copy, use a mount
#ADD config.docker.ini /queries/config.ini
#ADD gunicorn_config.py /queries/
#ADD *.rq /queries/
#ADD *.ipynb /queries/

WORKDIR /queries

CMD gunicorn -c gunicorn_config.py grlc.server:app & jupyter notebook --port=8888 --ip=0.0.0.0 --allow-root --NotebookApp.token=''
