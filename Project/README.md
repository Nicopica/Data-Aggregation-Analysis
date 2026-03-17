clean built:
docker-compose down

docker rm -f iot_server sensor_temp_1 sensor_pres_1 sensor_air_1 sensor_pres_extra hadoop_node
docker network rm iot_network




create & start server:

docker network create iot_network
docker run -d --network iot_network --name iot_server -p 8080:8080 iot_server_img

start visual sensors:

docker build -t virtual_sensor_img -f docker/Dockerfile.sensor .

docker run -d --network iot_network -e SENSOR_ID=1 -e LAT=45.0 -e LON=9.0 -e TYPE="Temperature Sensor" --name sensor_temp_1 virtual_sensor_img

docker run -d --network iot_network -e SENSOR_ID=2 -e LAT=45.5 -e LON=9.5 -e TYPE="Pressure Sensor" --name sensor_pres_1 virtual_sensor_img

docker run -d --network iot_network -e SENSOR_ID=3 -e LAT=46.0 -e LON=10.0 -e TYPE="Air Quality Sensor" --name sensor_air_1 virtual_sensor_img


fetch data & start hadloop:
curl "http://127.0.0.1:8080/fetch?type=Temperature%20Sensor" > hadoop/input.txt

docker build -t hadoop_streaming_img -f docker/Dockerfile.hadoop .

docker run -d --network iot_network --name hadoop_node hadoop_streaming_img


run hadoop:
docker exec hadoop_node hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
    -input /app/input.txt \
    -output /app/output_data \
    -mapper "/app/mapper.py" \
    -reducer "/app/reducer.py" \
    -cmdenv TARGET_X=45.0 \
    -cmdenv TARGET_Y=9.0 \
    -cmdenv MAX_D=100.0


see results:
docker exec hadoop_node cat /app/output_data/part-00000
