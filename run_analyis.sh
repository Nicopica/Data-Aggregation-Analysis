#!/bin/bash

# default values
TARGET_X=${1:-45.0}
TARGET_Y=${2:-9.0}
MAX_D=${3:-100.0}
TYPE=${4:-"Temperature Sensor"}

curl -s "http://localhost:8080/fetch?type=${TYPE// /%20}" -o input.txt
sudo docker cp input.txt namenode:/tmp/data.txt
sudo docker cp hadoop/mapper.py namenode:/tmp/mapper.py
sudo docker cp hadoop/reducer.py namenode:/tmp/reducer.py

sudo docker exec namenode bash -c "
  chmod +x /tmp/mapper.py /tmp/reducer.py

  hdfs dfs -rm -r -f /output/results 2>/dev/null
  hdfs dfs -mkdir -p /input
  hdfs dfs -put -f /tmp/data.txt /input/


  mapred streaming \
    -files /tmp/mapper.py,/tmp/reducer.py \
    -input /input/data.txt \
    -output /output/results \
    -mapper '/tmp/mapper.py' \
    -reducer '/tmp/reducer.py' \
    -cmdenv TARGET_X=$TARGET_X \
    -cmdenv TARGET_Y=$TARGET_Y \
    -cmdenv MAX_D=$MAX_D
  
  hdfs dfs -cat /output/results/part-00000
"
