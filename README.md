# DataFAIRifier
The DataFAIRifier is a system that supports the creation and validation of mappings of relational data to ontologies. The system is packaged as a set of Docker images. The frontend of the system is implemented as Jupyter Notebook.

This repository describes the bottom-up DataFAIRifier process, and FAIR (Findable, Accessible, Interoperable, Reusable) data station which will be setup when following the instructions.

## Getting started

### Prerequisites
To run this DataFAIRifier, you need the following software installed on your computer:
* Docker Engine
* Docker Compose

### Configuring the infrastructure
The full docker-compose collection of containers is given in [docker-compose.yml](docker-compose.yml)
The most minimalistic infrastructure can be executed by writing a docker-compose file (`docker-compose.yml`) with the following contents:
```
version: "2"
services:
  graphdb:
    image: jvsoest/graphdb-free:fairstation
    ports: 
      - "7200:7200"
```

This will create and run a GraphDB instance on your computer. The GraphDB web interface will be available on [http://localhost:7200](http://localhost:7200/).
If you want to add computation docker containers to this configuration, you can e.g. the O-RAW DICOM Radiomics pipeline:

```
version: "2"
services:
  graphdb:
    image: jvsoest/graphdb-free:fairstation
    ports: 
      - "7200:7200"
  oraw:
    image: jvsoest/oraw
    volumes:
      - ./dicom_import/:/data/
    links:
      - graphdb:graphdb
    environment:
      - RDF4J_URL=http://graphdb:7200
      - EXCLUDE_STRUCTURE_REGEX="(Patient.*|BODY.*|Body.*|NS.*|Couch.*|Isocenter.*)"
```

### Running the infrastructure.
To run this infrastructure, you can go to the folder where you have this docker-compose.yml stored, and type:
```docker-compose up```
This will download the necessary images, and run the container.

The following commands can help you as well:
* `docker-compose up -d`: Will start or run docker containers in detached mode, giving you back the command line (and run containers as service in background)
* `docker-compose stop`: will stop all running containers
* `docker-compose down`: Will stop all containders and **remove the active image including data**
* `docker logs <container_name>`: Will show the console logs for the running container, especially helpful in detached mode

### How to query and use GraphDB
Regarding the use of GraphDb, please have a look at the [quick start guide](http://graphdb.ontotext.com/documentation/free/quick-start-guide.html#explore-your-data-and-class-relationships)

## Implementation repositories
* [ProTRAIT](https://github.com/maastroclinic/ProTRAIT-FAIRifier)

## Frozen hackathon repositories
* [PBDW2018](http://github.com/jvsoest/PBDW2018_hackathon)
