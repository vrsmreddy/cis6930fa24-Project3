

# CIS 6930, Fall 2024 Project 3 - End Pipeline

## Introduction
This project is part of the data pipeline developed throughout the semester. It focuses on creating an interactive interface to display the data collected in Project 0. This represents one of the final stages of the data pipeline, where we visualize data for end users and provide a feedback mechanism. The interface showcases key statistics and visualizations derived from the data.

## Project Description
In Project 0, we developed a module to scrape and extract data from the Norman Police Department website. This project extends that work by adding:

- **Web Interface**: A web application to upload NormanPD-style incident PDFs via file or URL.
- **Data Visualizations**:
  1. **Cluster Plot**: Clustering of records to identify patterns.
  2. **Bar Graph**: Comparison of incident counts by type.
  3. **Bubble Chart**: Incidents visualized by time and nature.

## Features
- **PDF Upload**: Supports uploading multiple PDF files or providing a URL.
- **Database Integration**: Stores extracted incident data in an SQLite database.
- **Interactive Visualizations**: Displays cluster plots, bar graphs, and bubble charts using Matplotlib and Plotly.
- **Error Handling**: Handles invalid file uploads and provides feedback.

## Installation and Usage

### Prerequisites
- Python 3.12 or higher
- Pipenv for managing dependencies
## Directory Structure
```
CIS6930FA24-PROJECT3/
├── COLLABORATORS
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── setup.cfg
├── setup.py
├── src/
│   ├── main.py
│   ├── utils.py
│   ├── visualizations.py
│   ├── resources/
│   │   └── normanpd.db
│   ├── static/
│   │   ├── bar_graph.png
│   │   ├── bubble_chart.html
│   │   ├── cluster_plot.png
│   │   ├── script.js
│   │   └── style.css
│   ├── templates/
│   │   ├── index.html
│   │   ├── success.html
│   │   └── visualize.html
│   ├── tests/
│   │   ├── sample_incident.pdf
│   │   └── test_main.py
│   └── uploads/
│       ├── 2024-11-01_daily_incident_sum...
│       └── 2024-11-02_daily_incident_sum...
└── video/

```

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/username/cis6930fa24-project3.git
   ```
2. Navigate to the project directory:
   ```bash
   cd cis6930fa24-project3
   ```
3. Install dependencies:
   ```bash
   pipenv install
   ```
4. Activate the virtual environment:
   ```bash
   pipenv shell
   ```
5. Run the Flask application:
   ```bash
   pipenv run python src/main.py
   ```
6. Open your browser and navigate to `http://localhost:5000` to use the web interface.


## Usage Guide
1. Upload one or more NormanPD-style incident PDFs through the web interface by selecting a file or providing a URL.
2. Process the data and view success or error messages.
3. Navigate to the visualization page to view:
   - Cluster Plot of incidents
   - Bar Graph comparing incident types
   - Bubble Chart showing incidents by time and nature

## Visualizations
Sample visualizations include:
- Cluster Plot: Groups incidents based on time and nature.
- Bar Graph: Displays the frequency of incident types.
- Bubble Chart: Visualizes the relationship between time, nature, and incident counts.

# Visualizations and Functions Overview

## Visualizations

### 1. **Cluster Plot**
- **Description**: The cluster plot groups incidents based on the hour of the day and their nature. It uses K-Means clustering to create meaningful clusters.
- **Purpose**: Identifies patterns in the incident data, such as correlations between time and nature of incidents.
- **Generated Using**: Matplotlib and Scikit-learn.
- **File Path**: `src/static/cluster_plot.png`

### 2. **Bar Graph**
- **Description**: A bar graph comparing the count of incidents by their nature.
- **Purpose**: Provides a clear comparison of the frequency of different incident types.
- **Generated Using**: Matplotlib.
- **File Path**: `src/static/bar_graph.png`

### 3. **Bubble Chart**
- **Description**: Displays incidents by hour and nature using bubble sizes to represent the count of incidents.
- **Purpose**: Highlights the distribution of incidents across time and categories.
- **Generated Using**: Plotly.
- **File Path**: `src/static/bubble_chart.html`

---

## Functions in `main.py`

### 1. **`index()`**
- **Purpose**: Handles the main upload interface for the application.
- **Key Steps**:
  1. Accepts input via file upload or URL submission.
  2. Extracts incident data using the `extractincidents` function.
  3. Stores extracted data in the SQLite database using `createdb` and `populatedb`.
  4. Returns a success message upon successful data processing.

### 2. **`visualize()`**
- **Purpose**: Handles the visualization page.
- **Key Steps**:
  1. Checks if the database exists.
  2. Generates three visualizations:
     - Bar graph using `create_bar_graph`.
     - Cluster plot using `create_cluster_plot`.
     - Bubble chart using `create_bubble_chart`.
  3. Displays the visualizations on a webpage.

---

## Functions in `utils.py`

### 1. **`fetchincidents(url)`**
- **Purpose**: Downloads a PDF file from the provided URL.
- **Key Steps**:
  1. Sends an HTTP request to the URL.
  2. Verifies SSL certificates using `certifi`.
  3. Returns the raw PDF data.

### 2. **`extractincidents(pdf_data)`**
- **Purpose**: Extracts incident data from a PDF file.
- **Key Steps**:
  1. Reads the PDF using PyPDF2.
  2. Cleans and preprocesses the text to extract relevant fields.
  3. Returns a list of incidents, each with 5 fields: `Time`, `Incident Number`, `Location`, `Nature`, and `Incident ORI`.

---

## Functions in `visualizations.py`

### 1. **`create_bar_graph(db_path)`**
- **Purpose**: Generates a bar graph of incident counts by their nature.
- **Key Steps**:
  1. Queries the database to count incidents grouped by nature.
  2. Plots a bar graph using Matplotlib.
  3. Saves the graph as `bar_graph.png` in the static directory.

### 2. **`create_cluster_plot(db_path)`**
- **Purpose**: Generates a cluster plot of incidents based on time and nature.
- **Key Steps**:
  1. Queries the database to extract incident time and nature.
  2. Encodes the nature field and scales the features.
  3. Uses K-Means clustering to group incidents.
  4. Plots the clusters and saves the plot as `cluster_plot.png`.

### 3. **`create_bubble_chart(db_path)`**
- **Purpose**: Generates a bubble chart of incidents by time and nature.
- **Key Steps**:
  1. Queries the database to extract incident time and nature.
  2. Groups the data by hour and nature, calculating incident counts.
  3. Creates an interactive bubble chart using Plotly.
  4. Saves the chart as `bubble_chart.html` in the static directory.

---

## Data Flow Summary
1. **Upload or URL Input**: User provides incident PDFs via file or URL.
2. **Data Extraction**: The `extractincidents` function processes the PDF and extracts structured data.
3. **Database Storage**: Data is saved to an SQLite database using `createdb` and `populatedb`.
4. **Visualization**: Three visualizations are generated based on the stored data and displayed in the interface.



## Bugs and Assumptions
### Known Bugs
- Limited error handling for edge cases in PDF parsing.
- The clustering algorithm may not generalize well for diverse datasets.

### Assumptions
- The PDFs follow the NormanPD format.
- Data extracted is clean and does not require extensive preprocessing.

## External Resources and Credits
- **Libraries Used**:
  - Flask
  - PyPDF2
  - Matplotlib
  - Pandas
  - Plotly
  - Scikit-learn
  - Certifi
- **External Help**:
  - Stack Overflow for troubleshooting Python issues.
  - Official documentation for Flask and Matplotlib.

## Collaboration
Collaborators:

Plotly - https://plotly.com/python/bubble-charts/ - Provided guidance on creating bubble charts in Python using Plotly, essential for visualizing large datasets with various dimensions.
StackOverflow - https://stackoverflow.com/questions/71944846/plot-big-dataset-clusters-in-python - Offered advice on methods to visualize large clusters in datasets, crucial for understanding the distribution and grouping in data analysis.
Refer to the `COLLABORATORS` file for detailed information on team contributions.



## Video Demonstration
A narrated demonstration of the project is available:
- [YouTube Link](https://youtu.be/dFO8EbnhvEA)



# Explanation of Tests and Pipfile

## Test Functions
The project includes a set of tests to ensure the correctness and reliability of the implemented functionality. Below is an explanation of each test function:

### Test Functions in `test_main.py`

1. **`test_createdb`**
   - **Purpose**: Verifies that the database is successfully created.
   - **Steps**:
     - Calls the `createdb` function from `database.py`.
     - Checks if the database file (`resources/normanpd.db`) exists.
   - **Expected Outcome**: The database file is created at the specified location.

2. **`test_populatedb`**
   - **Purpose**: Ensures that data is correctly inserted into the database.
   - **Steps**:
     - Inserts sample incident data into a temporary database using `populatedb`.
     - Queries the database to confirm the data has been inserted.
   - **Expected Outcome**: The database contains the expected number of records.

3. **`test_extractincidents`**
   - **Purpose**: Tests the extraction of incidents from a sample PDF file.
   - **Steps**:
     - Loads a sample PDF file (`sample_incident.pdf`).
     - Extracts incidents using the `extractincidents` function from `utils.py`.
     - Verifies that the extracted data matches the expected format (5 fields per incident).
   - **Expected Outcome**: The function correctly extracts and structures incident data.

4. **`test_create_bubble_chart`**
   - **Purpose**: Ensures the bubble chart is generated successfully.
   - **Steps**:
     - Populates a temporary database with sample data.
     - Calls the `create_bubble_chart` function from `visualizations.py`.
     - Verifies the output file (`bubble_chart.html`) is created and exists.
   - **Expected Outcome**: The bubble chart file is generated without errors.

5. **`test_create_bar_graph`**
   - **Purpose**: Tests the creation of the bar graph visualization.
   - **Steps**:
     - Populates a temporary database with sample data.
     - Calls the `create_bar_graph` function from `visualizations.py`.
     - Verifies the output file (`bar_graph.png`) is created and exists.
   - **Expected Outcome**: The bar graph image file is generated successfully.
## How to Run Tests
To execute the test suite, run the following command from the project directory:
```bash
pipenv run python -m pytest -v

```
This will automatically discover and run all test functions in the `tests/` directory.

## Pipfile Explanation
The `Pipfile` defines the project’s dependencies and environment requirements. Below is a detailed explanation of each section and package:

### `[source]`
- **`url`**: Specifies the Python Package Index (PyPI) as the source for packages.
- **`verify_ssl`**: Ensures secure package downloads by verifying SSL certificates.

### `[packages]`
Contains the main dependencies required for the project:

1. **`flask`**: A lightweight web framework used to create the web interface.
2. **`pypdf2`**: Library for extracting text and data from PDF files.
3. **`matplotlib`**: Used for generating bar graphs and cluster plots.
4. **`pandas`**: Provides data manipulation and analysis tools.
5. **`scikit-learn`**: Implements clustering algorithms for data analysis.
6. **`folium`**: Optional for geographic visualizations (not actively used).
7. **`numpy`**: Fundamental library for numerical computations.
8. **`certifi`**: Ensures secure HTTP requests by providing a CA certificate bundle.
9. **`plotly`**: Creates interactive visualizations, such as the bubble chart.

### `[dev-packages]`
Contains development dependencies for testing and code formatting:

1. **`pytest`**: A testing framework for running unit tests.
2. **`black`**: A code formatter that ensures consistent coding style.

### `[requires]`
Specifies the required Python version:
- **`python_version = "3.12"`**: Ensures compatibility with Python 3.12.



## How to Manage Dependencies
To install the required dependencies, use Pipenv:
1. Install dependencies:
   ```bash
   pipenv install
   ```
2. Activate the virtual environment:
   ```bash
   pipenv shell
   ```














