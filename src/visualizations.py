# src/visualizations.py
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sqlite3
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
import os
import pandas as pd
import plotly.express as px

def create_bar_graph(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        query = "SELECT Nature, COUNT(*) FROM incident GROUP BY Nature"
        data = cursor.execute(query).fetchall()

    if not data:
        return None

    natures, counts = zip(*data)

    plt.figure(figsize=(12.8, 8))
    plt.bar(natures, counts)
    plt.xlabel("Nature of Incident")
    plt.ylabel("Count of Incidents")
    plt.title("Incident Counts by Nature")
    plt.xticks(rotation=80, ha='right')  # Rotate labels on the X-axis
    plt.tight_layout()
 
    # Save the bar graph
    plt.savefig('src/static/bar_graph.png')
    plt.close()

    return 'static/bar_graph.png'

def create_cluster_plot(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Time, Nature FROM incident")
        data = cursor.fetchall()

    if not data:
        return None

    times = []
    natures = []
    for t, n in data:
        parts = t.split(' ', 1)
        if len(parts) == 2:
            date_part, time_part = parts
            if ':' in time_part:
                hour_str = time_part.split(':')[0]
                if hour_str.isdigit():
                    hour = int(hour_str)
                    times.append(hour)
                    natures.append(n)

    if not times or not natures:
        return None

    encoder = LabelEncoder()
    encoded_natures = encoder.fit_transform(natures)

    features = np.array(list(zip(times, encoded_natures)))
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=3, random_state=0)
    labels = kmeans.fit_predict(scaled_features)

    plt.figure(figsize=(12.8,8))
    plt.scatter(scaled_features[:,0], scaled_features[:,1], c=labels, cmap='viridis')
    plt.title("Cluster Analysis of Incidents by Time and Nature")
    plt.xlabel("Hour of Day (scaled)")
    plt.ylabel("Nature of Incident (encoded & scaled)")
    plt.colorbar(label='Cluster Label')
    plt.tight_layout()

    plt.savefig('src/static/cluster_plot.png')
    plt.close()

    return 'static/cluster_plot.png'

def create_bubble_chart(db_path):
    print("Creating bubble chart...")
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT Time, Nature FROM incident", conn)
    conn.close()

    print("DataFrame length:", len(df))
    print("Sample df:\n", df.head())

    def extract_hour(time_str):
        if ' ' in time_str:
            parts = time_str.split(' ')
            if len(parts) > 1 and ':' in parts[1]:
                hour_str = parts[1].split(':')[0]
                if hour_str.isdigit():
                    return int(hour_str)
        return None

    df['Hour'] = df['Time'].apply(extract_hour)
    print("Checking Hour column:\n", df[['Time','Hour']].head())
    print("Hour null count:", df['Hour'].isnull().sum())

    if df.empty or df['Hour'].isnull().all():
        print("No valid hours found for bubble chart.")
        return None

    nature_unique = df['Nature'].nunique()
    print("Number of unique Nature categories:", nature_unique)
    print("Unique Natures:", df['Nature'].unique())

    if nature_unique == 0:
        print("No unique Natures found.")
        return None

    nature_categories = df['Nature'].unique()
    nature_to_code = {cat: i+1 for i, cat in enumerate(nature_categories)}
    df['Nature_Code'] = df['Nature'].map(nature_to_code)

    agg_df = df.groupby(['Hour','Nature_Code'], as_index=False).size()
    agg_df.rename(columns={'size':'Count'}, inplace=True)

    print("agg_df length:", len(agg_df))
    print(agg_df.head())

    if agg_df.empty:
        print("No aggregated data for bubble chart.")
        return None

    try:
        fig = px.scatter(
            agg_df,
            x='Hour',
            y='Nature_Code',
            size='Count',
            color='Nature_Code',
            hover_data={'Count':True, 'Hour':True, 'Nature_Code':False},
            title="Incidents by Hour and Nature (Bubble Chart)",
            labels={'Hour':'Hour of Day', 'Nature_Code':'Nature'},
            size_max=40
        )
    except Exception as e:
        print("Error creating bubble chart:", e)
        return None

    # Update Y-axis to avoid text collisions:
    # 1. Increase figure height and margins.
    # 2. Rotate labels so they are easier to read.
    # 3. Possibly allow more space with margin.
    fig.update_layout(
        width=1000,
        height=1200,
        margin=dict(l=250, r=50, t=50, b=50)  # more left margin for labels
    )

    fig.update_yaxes(
        ticktext=list(nature_categories),
        tickvals=list(range(1, len(nature_categories)+1)),
        tickangle=0,            # Keep them horizontal since we're increasing margin and height
        automargin=True         # allow automatic margin adjustments
    )

    # If rotation doesn't help, try tickangle=45 or -45:
    # fig.update_yaxes(tickangle=45)

    static_dir = os.path.join('src', 'static')
    os.makedirs(static_dir, exist_ok=True)

    chart_path = os.path.join(static_dir, 'bubble_chart.html')
    fig.write_html(chart_path, full_html=True)

    if not os.path.exists(chart_path):
        print("bubble_chart.html not created.")
        return None
    else:
        print("Bubble chart created successfully:", chart_path)

    return 'static/bubble_chart.html'
