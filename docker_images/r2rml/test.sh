docker run --rm -it \
    -v $(pwd)/run.sh:/run.sh \
    -v $(pwd)/run.py:/run.py \
    jvsoest/r2rml bash run.sh --debug