This docker image runs a Virtuoso Database.
===========================================

Simple Usage:
-------------
Simple use like this just runs the DB (using ~ 4 GB of RAM):

    docker run -p 1111:1111 -p 8890:8890 \
        -e "NumberOfBuffers=$((4*85000))" \
        joernhees/virtuoso


Volume for DB Directory:
------------------------
The database is placed inside a volume of this container in Virtuoso's default
path /var/lib/virtuoso-opensource-7 . You can mount it to the host's filesystem
like this:

    docker run -p 8890:8890 \
        -v /host/db/dir:/var/lib/virtuoso-opensource-7 \
        joernhees/virtuoso


Help:
-----
The image can print this README for quick lookup of options / copy-pasting:

    docker run --rm joernhees/virtuoso help


Import:
-------
To import mass data such as Ntriple dumps (can be gzipped) you can mount an
external folder to /import and use the "import <graph_URI>" args. This will
recursively import all files into the specified graph_URI, e.g.:

    docker run -it \
        -v /host/db/dir:/var/lib/virtuoso-opensource-7 \
        -v /data/dbpedia:/import:ro \
        joernhees/virtuoso import 'http://dbpedia.org'

After importing, the container will properly trigger & wait for full text index
building. It will also spawn a bash for you if you specified the `-it` arg as
in the example above. This allows you to inspect the results, for example by
starting an `isql-vt` in the container. If the `-it` flag is left away the
container will stop after the import. The importer will also check for errors
reported by Virtuoso and will set its exit-code accordingly. This allows
external scripts to easily check for errors during the import.


Config:
-------
You can override the virtuoso.ini NumberOfBuffers, MaxDirtyBuffers and
MaxDirtyBuffers by setting environment variables like in the following. If you
only specify NumberOfBuffers the others will be computed according to the
recommendations by OpenLink. The recommended NumberOfBuffers per GB of RAM is
85000, so to use 8 GB do the following:

    docker run -v /data/dbpedia:/import:ro -e "NumberOfBuffers=$((8*85000))" \
        joernhees/virtuoso import 'http://dbpedia.org'

If you want to override more virtuoso.ini variables you can simply mount a host
virtuoso.ini file in the container like this (don't use the env-var approach at
the same time, it will try to modify your file):

    # to get a default virtuoso.ini in your home directory:
    container_id=$(docker run -d joernhees/virtuoso run)
    docker cp $container_id:/etc/virtuoso-opensource-7/virtuoso.ini ~/
    docker stop $container_id
    docker rm -v $container_id
    # to use it after you modified it:
    docker run -v ~/virtuoso.ini:/etc/virtuoso-opensource-7/virtuoso.ini:ro \
        joernhees/virtuoso


Debugging / Interactive Mode:
-----------------------------
Similar to the import mode, the container supports interactive mode that will
spawn a bash for you in the database directory via the `-it` run args:

    docker run -it joernhees/virtuoso

The above will spawn the bash after starting virtuoso. The DB will shutdown on
exit.

In case you want to start the bash _before_ the DB starts you can append the
"bash" arg like this:

    docker run -it joernhees/virtuoso bash


Installing Virtuoso VAD Packages:
---------------------------------
To install Virtuoso VAD packages you can use the web-interface (should be
reachable on http://localhost:8890/conductor with default user `dba` and
password `dba`). The image puts all default VAD files plus the DBpedia one in
the standard folder `/usr/share/virtuoso-opensource-7/vad/`. Alternatively, you
can install those VAD files via the container's interactive command line or an
external `docker exec` command. To add other VAD files i'd suggest to simply
mount them as files into `/usr/share/virtuoso-opensource-7/vad/` as well.
Provided the VAD package you want to install is already in the container's
filesystem (and in a folder which is allowed in the virtuoso.ini), you can for
example run the following from the interactive command inside the container:

    isql-vt "EXEC=vad_install('/usr/share/virtuoso-opensource-7/vad/dbpedia_dav.vad');"

Or similar from outside the container with `docker exec`:

    docker run -d --name tmp joernhees/virtuoso &&
    docker exec tmp wait_ready &&  # waits for Virtuoso to accept connections
    docker exec tmp isql-vt \
        "EXEC=vad_install('/usr/share/virtuoso-opensource-7/vad/dbpedia_dav.vad');" &&
    docker stop tmp &&
    docker rm -v tmp


Waiting for Virtuoso DB to accept connections:
----------------------------------------------
The above also shows how to wait for the Virtuoso DB to actually accept
connections, which is especially useful with big DBs started in background and
with a lot of RAM. To wait for Virtuoso to be ready simply use:

    docker exec container_name wait_ready


Example:
--------
Putting it all together to create a DBpedia container:

    # importing DBpedia 2015-04 vocabulary and files with throw-away containers
    # note how any failures will prevent the following commands from running
    # by joining them with &&:
    db_dir=~/dbpedia_virtuoso_db
    dump_dir=/usr/local/data/datasets/remote/dbpedia/2015-04

    # install some VAD packages in the db which we'll keep in db_dir
    docker run -d --name dbpedia-vadinst \
        -v "$db_dir":/var/lib/virtuoso-opensource-7 \
        joernhees/virtuoso &&
    docker exec dbpedia-vadinst wait_ready &&
    docker exec dbpedia-vadinst isql-vt PROMPT=OFF VERBOSE=OFF BANNER=OFF \
        "EXEC=vad_install('/usr/share/virtuoso-opensource-7/vad/rdf_mappers_dav.vad');" &&
    docker exec dbpedia-vadinst isql-vt PROMPT=OFF VERBOSE=OFF BANNER=OFF \
        "EXEC=vad_install('/usr/share/virtuoso-opensource-7/vad/dbpedia_dav.vad');" &&
    docker stop dbpedia-vadinst &&
    docker rm -v dbpedia-vadinst &&

    # starting the import (main part with 64 GB of RAM)
    docker run --rm \
        -v "$db_dir":/var/lib/virtuoso-opensource-7 \
        -v "$dump_dir"/importedGraphs/classes.dbpedia.org:/import:ro \
        joernhees/virtuoso import 'http://dbpedia.org/resource/classes#' &&
    docker run --rm \
        -v "$db_dir":/var/lib/virtuoso-opensource-7 \
        -v "$dump_dir"/importedGraphs/dbpedia.org:/import:ro \
        -e "NumberOfBuffers=$((64*85000))" \
        joernhees/virtuoso import 'http://dbpedia.org' &&

    # actually running a local endpoint on port 8891:
    docker run --name dbpedia \
        -v "$db_dir":/var/lib/virtuoso-opensource-7 \
        -p 8891:8890 \
        -e "NumberOfBuffers=$((32*85000))" \
        joernhees/virtuoso

    # access one of the following for example:
    # http://localhost:8891/sparql
    # http://localhost:8891/resource/Bonn
    # http://localhost:8891/conductor (user: dba, pw: dba)

