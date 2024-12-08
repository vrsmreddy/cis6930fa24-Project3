# tests/test_main.py

import os
import sqlite3
import pytest
from src.utils import extractincidents
from src.database import createdb, populatedb
from src.visualizations import create_bubble_chart, create_bar_graph

@pytest.fixture
def sample_db(tmp_path):
    # Create a temporary database for testing
    db_path = tmp_path / "test_normanpd.db"
    db_path = str(db_path)
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE incident (
            Time TEXT,
            Incident_Number TEXT,
            Location TEXT,
            Nature TEXT,
            Incident_ORI TEXT
        );
    """)
    conn.close()
    return db_path

def test_createdb(tmp_path):
    # Test database creation
    db_path = str(tmp_path / "normanpd.db")
    db = createdb()
    # createdb() should create 'resources/normanpd.db' by default
    assert os.path.exists('./resources/normanpd.db'), "Database file was not created."

def test_populatedb(sample_db):
    # Insert sample data
    incidents = [
        ("11/1/2024 0:00", "INC123", "Location A", "Nature A", "ORI001"),
        ("11/1/2024 1:00", "INC124", "Location B", "Nature B", "ORI002"),
    ]
    count = populatedb(sample_db, incidents)
    assert count == 2, "Not all incidents were inserted."

    # Check data in DB
    conn = sqlite3.connect(sample_db)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM incident;")
    row_count = c.fetchone()[0]
    conn.close()
    assert row_count == 2, "Incident count in the database does not match expected."

def test_extractincidents():
    # Test data extraction from PDF:
    # Provide a sample PDF "sample_incident.pdf" in your tests directory or a known location.
    # This test assumes you have a file with at least one incident.
    # If you don't have a sample PDF, you can skip this test or mock the function.

    # The following is a placeholder. Replace "sample_incident.pdf" with your actual test file path.
    pdf_path = "tests/sample_incident.pdf"
    if not os.path.exists(pdf_path):
        pytest.skip("Sample PDF not available, skipping test_extractincidents.")

    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()

    incidents = extractincidents(pdf_data)
    assert incidents, "No incidents extracted from the PDF."
    # Check the structure of the first incident (Time, Incident_Number, Location, Nature, Incident_ORI)
    assert len(incidents[0]) == 5, "Incident record does not have the correct number of fields."

def test_create_bubble_chart(sample_db):
    # Insert some data to allow bubble chart creation
    incidents = [
        ("11/1/2024 0:00", "INC100", "Loc", "Nature A", "ORI"),
        ("11/1/2024 0:01", "INC101", "Loc", "Nature A", "ORI"),
        ("11/1/2024 0:02", "INC102", "Loc", "Nature B", "ORI"),
    ]
    populatedb(sample_db, incidents)

    chart_path = create_bubble_chart(sample_db)
    assert chart_path is not None, "Bubble chart was not created."
    assert os.path.exists(os.path.join("src", chart_path)), "Bubble chart file does not exist."

def test_create_bar_graph(sample_db):
    # Insert data for bar graph
    incidents = [
        ("11/1/2024 0:00", "INC200", "Loc", "Nature C", "ORI"),
        ("11/1/2024 0:00", "INC201", "Loc", "Nature C", "ORI"),
        ("11/1/2024 0:00", "INC202", "Loc", "Nature D", "ORI"),
    ]
    populatedb(sample_db, incidents)

    bar_path = create_bar_graph(sample_db)
    assert bar_path is not None, "Bar graph was not created."
    assert os.path.exists(os.path.join("src", bar_path)), "Bar graph file does not exist."
