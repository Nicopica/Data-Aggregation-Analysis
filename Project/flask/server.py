import sqlite3
from flask import Flask, g, request, Response

DATABASE = 'iot_data.db'
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # CRITICAL: Enable foreign key support for cascading deletes (Grade 4 requirement)
        db.execute("PRAGMA foreign_keys = ON;")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/store')
def store():
    sensor_id = request.args.get('sensor_id', type=int)
    lat = request.args.get('latitude', type=float)
    lon = request.args.get('longitude', type=float)
    sensor_type = request.args.get('type', type=str)
    value = request.args.get('value', type=float)
    timestamp = request.args.get('timestamp', type=str)

    db = get_db()
    
    cur = db.execute("SELECT type_id FROM sensor_types WHERE name = ?", (sensor_type,))
    type_row = cur.fetchone()
    if not type_row:
        return f"Error: Sensor type '{sensor_type}' is not registered.", 400
    type_id = type_row[0]

    db.execute("INSERT OR IGNORE INTO sensors (sensor_id, latitude, longitude) VALUES (?, ?, ?)", 
               (sensor_id, lat, lon))

    db.execute("INSERT INTO measurements (sensor_id, type_id, timestamp, value) VALUES (?, ?, ?, ?)", 
               (sensor_id, type_id, timestamp, value))
    db.commit()
    
    return "Data stored successfully", 200

@app.route('/retrieve')
def retrieve():
    sensor_id = request.args.get('sensor_id', type=int)
    start_time = request.args.get('start_time', type=str)
    end_time = request.args.get('end_time', type=str)

    db = get_db()
    cur = db.execute('''
        SELECT st.name, st.unit, m.timestamp, m.value 
        FROM measurements m
        JOIN sensor_types st ON m.type_id = st.type_id
        WHERE m.sensor_id = ? AND m.timestamp BETWEEN ? AND ?
        ORDER BY st.name ASC, m.timestamp ASC
    ''', (sensor_id, start_time, end_time))
    
    rows = cur.fetchall()
    if not rows:
        return "No data found for this sensor in the specified time range."

    grouped_data = {}
    for row in rows:
        type_name, unit, timestamp, value = row
        if type_name not in grouped_data:
            grouped_data[type_name] = {'unit': unit, 'records': []}
        grouped_data[type_name]['records'].append((timestamp, value))

    html = "<html><body>"
    for type_name, data in grouped_data.items():
        html += f"<h3>{type_name}</h3>"
        html += "<table border='1'><tr><th>Timestamp (UTC)</th><th>" + data['unit'] + "</th></tr>"
        for record in data['records']:
            html += f"<tr><td>{record[0]}</td><td>{record[1]}</td></tr>"
        html += "</table><br>"
    html += "</body></html>"
    
    return html

@app.route('/fetch')
def fetch():
    sensor_type = request.args.get('type', type=str)
    
    db = get_db()
    cur = db.execute('''
        SELECT s.latitude, s.longitude, m.value 
        FROM measurements m
        JOIN sensors s ON m.sensor_id = s.sensor_id
        JOIN sensor_types st ON m.type_id = st.type_id
        WHERE st.name = ?
    ''', (sensor_type,))
    
    rows = cur.fetchall()
    
    plain_text = "\n".join([f"{row[0]}\t{row[1]}\t{row[2]}" for row in rows])
    
    return Response(plain_text, mimetype='text/plain')

@app.route('/add_type')
def add_type():
    name = request.args.get('name', type=str)
    unit = request.args.get('unit', type=str)
    db = get_db()
    try:
        db.execute("INSERT INTO sensor_types (name, unit) VALUES (?, ?)", (name, unit))
        db.commit()
        return f"Successfully added {name} ({unit})."
    except sqlite3.IntegrityError:
        return "Error: Sensor type already exists.", 400

@app.route('/delete_type')
def delete_type():
    name = request.args.get('name', type=str)
    db = get_db()
    db.execute("DELETE FROM sensor_types WHERE name = ?", (name,))
    db.commit()
    return f"Successfully deleted {name} and all its associated measurements."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

