# DataFAIRifier
The DataFAIRifier is a system that supports the creation and validation of mappings of relational data to ontologies. The system is packaged as a set of Docker images. The frontend of the system is implemented as a set of Jupyter Notebooks.

This repository describes the bottom-up DataFAIRifier process, and FAIR (Findable, Accessible, Interoperable, Reusable) data station which will be setup when following the instructions.

## Getting started

### Prerequisites
To run the DataFAIRifier, you need the following software installed on your computer:
* Docker Engine
* Docker Compose

### How to run it
1. Clone this repository
```
git clone https://github.com/maastroclinic/DataFAIRifier.git && cd DataFAIRifier
```
2. Start the infrastructure (the full docker-compose collection of containers is given in [docker-compose.yml](docker-compose.yml))
```
docker-compose up
```
If you changed a dockerfile or the contents of its build directory, run  
```
docker-compose up --build
```
3. Open [http://localhost:8888](http://localhost:8888) in a web browser to view the Jupyter Notebooks
4. Run the Jupyter notebooks in the following order:
  * **import.ipynb** to initialize the database
  * **loadR2RML.ipynb** to initialize the mapping
  * **Validator.ipynb** to create a mapping of the table structure, i.e. columns; 
    make sure you save the mapping before you run the next cells  
  * **termMapping.ipynb** to create a mapping of the table terminology, i.e. values

## License
Source code and data of DataFAIRifier is licensed under the Apache License, version 2.0.
