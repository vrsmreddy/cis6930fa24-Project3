# src/main.py
from flask import Flask, request, render_template
import os
from utils import fetchincidents, extractincidents
from database import createdb, populatedb
from visualizations import create_bar_graph, create_cluster_plot, create_bubble_chart

app = Flask(__name__, template_folder='../templates')
app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DATABASE_NAME = './resources/normanpd.db'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_method = request.form.get('input_method', 'pdf')
        incident_records = []

        if input_method == 'pdf':
            # Handle uploaded files
            files = request.files.getlist('pdf_files')
            for file in files:
                if file and file.filename:
                    filename = file.filename
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    with open(file_path, 'rb') as f:
                        pdf_data = f.read()
                    # Extract incidents
                    incidents = extractincidents(pdf_data)
                    if incidents:
                        incident_records.extend(incidents)

        elif input_method == 'url':
            # Handle PDF URL
            pdf_url = request.form.get('pdf_url')
            if pdf_url and pdf_url.strip():
                try:
                    pdf_data = fetchincidents(pdf_url.strip())
                    incidents = extractincidents(pdf_data)
                    if incidents:
                        incident_records.extend(incidents)
                except Exception as e:
                    return f"Error processing PDF from URL {pdf_url}: {str(e)}"

        if not incident_records:
            return "No incidents extracted. Please provide a valid PDF or URL."

        # Populate database
        try:
            db = createdb()
            populatedb(db, incident_records)
        except Exception as e:
            return f"Error populating database: {str(e)}"

        return render_template('success.html', message="Data processed successfully!")

    return render_template('index.html')

@app.route('/visualize', methods=['GET'])
def visualize():
    if not os.path.exists(DATABASE_NAME):
        return "No database found. Please upload and process PDFs first."

    bar_graph_path = create_bar_graph(DATABASE_NAME)
    cluster_path = create_cluster_plot(DATABASE_NAME)
    bubble_chart_path = create_bubble_chart(DATABASE_NAME)

    return render_template('visualize.html', 
                           bar_graph=bar_graph_path,
                           cluster_plot=cluster_path,
                           bubble_chart=bubble_chart_path)

if __name__ == '__main__':
    app.run(debug=True)
