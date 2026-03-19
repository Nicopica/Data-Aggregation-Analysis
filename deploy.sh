#!/bin/bash

echo " Deleting old containers and networks"
sudo docker rm -f $(sudo docker ps -aq) 2>/dev/null
sudo docker-compose down 2>/dev/null

sudo docker network rm iot_network project_default 2>/dev/null

sudo docker rmi -f iot_server_img virtual_sensor_img 2>/dev/null

echo "Building images and creating network"
sudo docker network create iot_network
sudo docker build -t iot_server_img -f docker/Dockerfile .
sudo docker build -t virtual_sensor_img -f docker/Dockerfile.sensor .

echo "Starting hadoop"
sudo docker-compose up -d

echo "Waiting 30 seconds to initialize"
sleep 30

echo "Starting web server"
sudo docker run -d --network iot_network --name iot_server -p 8080:8080 iot_server_img
sleep 3

echo "Configuring hadoop"
sudo docker exec namenode hdfs dfsadmin -safemode leave

for node in namenode nodemanager1 nodemanager2; do
    sudo docker exec -u 0 $node bash -c "
        sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list; 
        sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list; 
        sed -i '/stretch-updates/d' /etc/apt/sources.list; 
        apt-get update >/dev/null 2>&1 && apt-get install -y python3 >/dev/null 2>&1"
done

echo "Starting sensors"
sudo docker run -d --network iot_network -e SENSOR_ID=1 -e LAT=45.0 -e LON=9.0 \
  -e TYPE="Temperature Sensor,Pressure Sensor" --name sensor_1 virtual_sensor_img

sudo docker run -d --network iot_network -e SENSOR_ID=2 -e LAT=45.5 -e LON=9.5 \
  -e TYPE="Air Quality Sensor,CO2 Sensor" --name sensor_2 virtual_sensor_img

sudo docker run -d --network iot_network -e SENSOR_ID=3 -e LAT=46.0 -e LON=10.0 \
  -e TYPE="Temperature Sensor,Air Quality Sensor" --name sensor_3 virtual_sensor_img

sudo docker run -d --network iot_network -e SENSOR_ID=4 -e LAT=44.0 -e LON=8.0 \
  -e TYPE="Temperature Sensor,Pressure Sensor,Air Quality Sensor,CO2 Sensor" --name sensor_4 virtual_sensor_img
echo "Finished"
