echo. 2>output.ttl

docker run --rm -it ^
    -v %cd%\run.sh:/run.sh ^
    -v %cd%\run.py:/run.py ^
    -e DB_JDBC=jdbc:postgresql://172.17.0.1:2345/mydata ^
    -v C:\Users\johan\Documents\Repositories\FAIR\DataFAIRifier\notebooks\mapping.ttl:/mapping.ttl ^
    -v %cd%\output.ttl:/output.ttl ^
    jvsoest/r2rml bash run.sh --debug