docker build -t jvsoest/converter .\
docker stop cwl_postgres
docker stop cwl_blazegraph

docker rm cwl_postgres
docker rm cwl_blazegraph

docker run -d --name cwl_postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v /Users/johan/Repositories/DataFAIRifier/clinical-data-workflow/workflows/psql_init/:/docker-entrypoint-initdb.d/ postgres
docker run -d --name cwl_blazegraph -p 9999:9999 jvsoest/blazegraph

docker run --rm --link cwl_postgres:postgresdb --link cwl_blazegraph:blazegraph jvsoest/converter