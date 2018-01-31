docker stop graphdb
docker rm graphdb

docker run -d \
    --name graphdb \
    -p 7200:7200 \
    --restart unless-stopped \
    jvsoest/graphdb-free:8.4.1
