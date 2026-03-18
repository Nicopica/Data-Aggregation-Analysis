#!/bin/bash

# --- CONFIGURACIÓN ---
TARGET_X=45.0
TARGET_Y=9.0
MAX_D=100.0
SENSOR_TYPE="Temperature Sensor"
OUTPUT_DIR="/output_data"
INPUT_HDFS="/input/input.txt"

echo "=== 1. Asegurando que el clúster esté ARRIBA ==="
docker-compose up -d
sleep 5 # Esperamos a que respiren

echo "=== 2. Descargando datos desde el servidor Flask ==="
curl -s "http://127.0.0.1:8080/fetch?type=$(echo $SENSOR_TYPE | sed 's/ /%20/g')" > input.txt

if [ ! -s input.txt ]; then
    echo "❌ Error: No hay datos. ¿Están los sensores corriendo?"
    exit 1
fi

echo "=== 3. Reparando Repositorios y instalando Python 3 ==="
for node in namenode nodemanager1; do
    echo "Configurando $node..."
    # Este comando cambia los repositorios muertos de Debian por los de ARCHIVE (el truco del almendruco)
    docker exec -u 0 $node bash -c "sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list; sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list; sed -i '/stretch-updates/d' /etc/apt/sources.list; apt-get update && apt-get install -y python3"
done

echo "=== 4. Preparando archivos en carpetas seguras ==="
# IMPORTANTE: No los ponemos en / para evitar el error de Hadoop
docker exec namenode mkdir -p /tmp/hadoop_scripts
docker cp input.txt namenode:/tmp/hadoop_scripts/input.txt
docker cp hadoop/mapper.py namenode:/tmp/hadoop_scripts/mapper.py
docker cp hadoop/reducer.py namenode:/tmp/hadoop_scripts/reducer.py

echo "=== 5. Cargando datos a HDFS ==="
docker exec namenode hdfs dfs -mkdir -p /input
docker exec namenode hdfs dfs -rm -r $OUTPUT_DIR 2>/dev/null
docker exec namenode hdfs dfs -put -f /tmp/hadoop_scripts/input.txt $INPUT_HDFS

echo "=== 6. Ejecutando Hadoop Streaming (MapReduce) ==="
# Ejecutamos desde dentro de la carpeta temporal para que las rutas sean relativas
docker exec -w /tmp/hadoop_scripts namenode hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
    -file mapper.py \
    -file reducer.py \
    -input $INPUT_HDFS \
    -output $OUTPUT_DIR \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -cmdenv TARGET_X=$TARGET_X \
    -cmdenv TARGET_Y=$TARGET_Y \
    -cmdenv MAX_D=$MAX_D

echo ""
echo "=== 7. RESULTADOS FINALES ==="
echo "----------------------------------------------------"
docker exec namenode hdfs dfs -cat $OUTPUT_DIR/part-00000 2>/dev/null || echo "⚠️  No hubo salida. Revisa los logs de los contenedores."
echo "----------------------------------------------------"
