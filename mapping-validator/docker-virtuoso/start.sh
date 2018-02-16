#!/bin/bash
set -e
# set -x

CONF_FILE=/etc/virtuoso-opensource-7/virtuoso.ini
DB_DIR=/var/lib/virtuoso-opensource-7
DB_DIR_ORIG=$DB_DIR.orig
INIT_SCRIPT=/etc/init.d/virtuoso-opensource-7
IMPORT_DIR=/import
PID_FILE=/var/run/virtuoso-opensource-7.pid

retval=0

function usage {
	cat /root/README_VIRTUOSO.md >&2
	exit 1
}

function terminate {
	# stop service and clean up here
	echo "stopping virtuoso"
	"$INIT_SCRIPT" stop

	if pgrep "virtuoso" > /dev/null ; then
		echo -n "some virtuoso process is still running waiting "
		while pgrep "virtuoso" > /dev/null ; do echo -n "." ; sleep 1 ; done
		echo " done."
	fi
	echo "exited virtuoso"
	exit $retval
}
trap terminate HUP INT QUIT TERM



function check_numeric {
	if [[ "$2" != +([0-9]) ]] ; then
		echo "$1 needs to be a number but was $2" >&2
		retval=1
		terminate
	fi
}

if [[ -n "$NumberOfBuffers" ]] ; then
	# replace NumberOfBuffers in virtuoso.ini
	check_numeric "NumberOfBuffers" "$NumberOfBuffers"
	sed -i "/^NumberOfBuffers\s*=/ s/[0-9]*\s*$/$NumberOfBuffers/" "$CONF_FILE"

	if [[ -z "${MaxDirtyBuffers+xxx}" ]] ; then
		# MaxDirtyBuffers unset, calculate from NumberOfBuffers
		MaxDirtyBuffers=$(($NumberOfBuffers * 75 / 100))
	fi

	if [[ -z "${MaxCheckpointRemap+xxx}" ]] ; then
		# MaxCheckpointRemap unset, calculate from NumberOfBuffers
		MaxCheckpointRemap=$(($NumberOfBuffers * 25 / 100))
	fi
fi

if [[ -n "$MaxDirtyBuffers" ]] ; then
	# replace MaxDirtyBuffers in virtuoso.ini
	check_numeric "MaxDirtyBuffers" "$MaxDirtyBuffers"
	sed -i "/^MaxDirtyBuffers\s*=/ s/[0-9]*\s*$/$MaxDirtyBuffers/" "$CONF_FILE"
fi

if [[ -n "$MaxCheckpointRemap" ]] ; then
	# replace MaxCheckpointRemap (the first only) in virtuoso.ini
	check_numeric "MaxCheckpointRemap" "$MaxCheckpointRemap"
	sed -i "0,/^MaxCheckpointRemap\s*=/ s/^MaxCheckpointRemap\s*=\s*[0-9]*\s*$/MaxCheckpointRemap = $MaxCheckpointRemap/" "$CONF_FILE"
fi

# - no arg: simply start the db.
# - arg "run": same as no arg (simply start the db)
# - arg "bash:" will execute a bash _before_ starting the db
#   (use no arg / "run" with docker's -it switch to run a bash after db start)
# - args "import <graph_name>": recursively imports everything mounted to the
#   container's /import directory into <graph_name>
if [[ $# -gt 2 ]] ; then usage ; fi
if [[ $# -eq 1 ]] ; then
	case "$1" in
		"run") ;;
		"bash") exec bash ;;
		*) usage
	esac
fi
if [[ $# -eq 2 && $1 != "import" ]] ; then usage ; fi

if [[ -z $(ls "$DB_DIR") ]] ; then
	# db dir is empty by host mount, re-init
	echo -n "initializing db dir... "
	cp -a "$DB_DIR_ORIG"/* "$DB_DIR"/
	if [[ -f "$DB_DIR/db/virtuoso.lck" ]] ; then
		echo -e "\nWARNING: it seems as if init db wasn't shut down properly on image build. Maybe try removing the db/virtuoso.lck file?"
	fi
	echo "done."
fi

# start service in background here
"$INIT_SCRIPT" start

if [[ $1 == "import" ]] ; then
	isql-vt PROMPT=OFF VERBOSE=OFF BANNER=OFF <<-EOF
		ld_dir_all('$IMPORT_DIR', '*.*', '$2');
		SELECT 'importing this file / these files:';
		SELECT ll_file FROM DB.DBA.LOAD_LIST WHERE ll_state = 0;
		SELECT 'starting import', CURRENT_TIMESTAMP();
		rdf_loader_run();
		checkpoint;
		commit work;
		checkpoint;
		SELECT 'import finished', CURRENT_TIMESTAMP();
		SELECT 'graph $2 now contains n triples:';
		sparql SELECT COUNT(*) as ?c { GRAPH <$2> {?s ?p ?o.} };
	EOF
	errors=$(isql-vt BANNER=OFF VERBOSE=OFF 'EXEC=SELECT * FROM DB.DBA.LOAD_LIST WHERE ll_error IS NOT NULL;')
	if [[ -n $errors ]] ; then
		retval=3
		echo "ERROR: there was at least one error during the import:" >&2
		echo "$errors" >&2
	fi
	isql-vt PROMPT=OFF VERBOSE=OFF BANNER=OFF <<-EOF
		SELECT 'start completion of full-text index', CURRENT_TIMESTAMP();
		DB.DBA.VT_INC_INDEX_DB_DBA_RDF_OBJ();
		checkpoint;
		commit work;
		checkpoint;
		SELECT 'completion of full-text index finished', CURRENT_TIMESTAMP();
		shutdown;
	EOF

	if [[ -t 1 ]] ; then
		# we have a terminal
		bash
	fi
	terminate
fi

if [[ -t 1 ]] ; then
	# we have a terminal
	bash
else
	while "$INIT_SCRIPT" status > /dev/null ; do sleep 1; done
fi

terminate
