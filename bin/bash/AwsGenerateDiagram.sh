#! /bin/bash

DIRECTORY_OUTPUT=output
DIRECTORY_TMP=tmp

mkdir -p $DIRECTORY_OUTPUT $DIRECTORY_TMP

FILE_DOT=$DIRECTORY_OUTPUT/graph.dot
FILE_IMAGE=$DIRECTORY_OUTPUT/result.png
FILE_INSTANCES=$DIRECTORY_TMP/instances

function clean_agd {
	rm -rf $DIRECTORY_OUTPUT/*
	#rm -rf $DIRECTORY_TMP/*
}

function get_instances {
	if [[ ! -f $FILE_INSTANCES || $(wc -l $FILE_INSTANCES | awk '{print($1)}' ) -lt 5 ]]; then
		aws --profile copa ec2 describe-instances | tee $FILE_INSTANCES
	else
		cat $FILE_INSTANCES
	fi
}

echo Cleaning files
clean_agd

echo Creating DOT file
echo 'Graph {' > $FILE_DOT
INSTANCES="$(get_instances | jq '.Reservations[].Instances[] | select(.Tags[].Key == "Name") | .Tags[].Value' | tr -d '"')"
echo "$INSTANCES" | sed -r -e 's/\-/_/g' -e 's/$/ \[\]/g' -e 's/^/\t/g' -e 's/\[\]/\[image="icons\/ec2_instance.png" peripheries=0 fixedsize=shape\]/g' >> $FILE_DOT

#echo "$INSTANCES"

echo '}' >> $FILE_DOT

echo Creating Image
fdp -o $FILE_IMAGE -Tpng $FILE_DOT
