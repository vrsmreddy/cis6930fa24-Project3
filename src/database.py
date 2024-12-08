# src/database.py
import os
import sqlite3


def createdb():
    resource_path = './resources'
    os.makedirs(resource_path, exist_ok=True)
    database_name = os.path.join(resource_path, 'normanpd.db')
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS incident')
        cursor.execute('CREATE TABLE incident (Time TEXT, Incident_Number TEXT, Location TEXT, Nature TEXT, Incident_ORI TEXT);')
    return database_name


# Function to populate the database with incident records
def populatedb(database_name, incident_records):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO incident VALUES (?,?,?,?,?)", incident_records)
    return len(incident_records)
