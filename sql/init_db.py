import sqlite3

DATABASE = 'iot_data.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
   
    # activate foreingn keys
    cursor.execute("PRAGMA foreign_keys = ON;")
   
   # create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_types (
            type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            unit TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            sensor_id INTEGER PRIMARY KEY,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
            measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER NOT NULL,
            type_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            value REAL NOT NULL,
            FOREIGN KEY (sensor_id) REFERENCES sensors (sensor_id) ON DELETE CASCADE,
            FOREIGN KEY (type_id) REFERENCES sensor_types (type_id) ON DELETE CASCADE
        )
    ''')
   
    # add default values
    cursor.executemany('''
        INSERT OR IGNORE INTO sensor_types (name, unit) 
        VALUES (?, ?)
    ''', [
        ('Temperature Sensor', '°C'),
        ('Pressure Sensor', 'hPa'),
        ('Air Quality Sensor', 'PM10'),
        ('CO2 Sensor', 'ppm')
    ])
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
