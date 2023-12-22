import sqlite3

# Create a new SQLite database
conn = sqlite3.connect('./data/image_data.db')
# Create a table
conn.execute('''
CREATE TABLE IF NOT EXISTS image_data (
    id INTEGER PRIMARY KEY,
    model_name TEXT,
    alarm_size INTEGER,
    conf REAL,
    mode TEXT,
    object_count INTEGER,
    max_box_width INTEGER,
    confidence REAL,
    inference REAL,
    processing_time REAL,
    current_time TEXT,
    latitude REAL,
    longitude REAL,
    gpu_info TEXT,
    image_size TEXT
)
''')

conn.close()
