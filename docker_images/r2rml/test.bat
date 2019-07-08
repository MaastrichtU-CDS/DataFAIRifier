rem create an empty output file
echo. 2>output.ttl

rem Run the docker container in debug mode
docker run --rm -it ^
    -e DB_JDBC=jdbc:postgresql://172.17.0.1:2345/mydata ^
    -v C:\Users\johan\Documents\Repositories\FAIR\DataFAIRifier\notebooks\mapping.ttl:/mapping.ttl ^
    -v %cd%\output.ttl:/output.ttl ^
    jvsoest/r2rml bash run.sh --debug