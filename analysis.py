import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Needed for generating plots without a GUI
import matplotlib.pyplot as plt
import io
import base64
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_data(csv_filename='student_performance.csv'):
    # Construct the absolute path to the CSV file
    csv_file = os.path.join(BASE_DIR, csv_filename)
    # Load the student performance CSV
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        df = pd.DataFrame()
    return df

def get_metrics(df):
    if df.empty:
        return {'avg_maths': 0, 'avg_science': 0, 'avg_english': 0}
        
    return {
        'avg_maths': float(df['Maths'].mean()),
        'avg_science': float(df['Science'].mean()),
        'avg_english': float(df['English'].mean())
    }

def get_raw_data(df):
    if df.empty:
        return []
    # Fill NaN with None so it converts to JSON null properly if any
    return df.where(pd.notnull(df), None).to_dict(orient='records')

def get_plot_base64():
    df = load_data()
    if df.empty:
        return ""
        
    # Calculate Average Marks across the three subjects for scatter plot
    df['Average_Marks'] = df[['Maths', 'Science', 'English']].mean(axis=1)

    plt.style.use('ggplot')
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # A. Bar Chart: Average Marks by Subject
    subjects = ['Maths', 'Science', 'English']
    avg_marks = [df[sub].mean() for sub in subjects]
    axes[0].bar(subjects, avg_marks, color=['skyblue', 'lightgreen', 'coral'])
    axes[0].set_title('Average Marks by Subject')
    axes[0].set_ylabel('Marks (Out of 100)')
    axes[0].set_ylim(0, 100)

    # B. Scatter Plot: Study Hours vs Average Marks
    axes[1].scatter(df['Study_Hours_Per_Week'], df['Average_Marks'], color='purple', alpha=0.7)
    axes[1].set_title('Study Hours vs Average Marks')
    axes[1].set_xlabel('Study Hours Per Week')
    axes[1].set_ylabel('Average Marks')

    # C. Heatmap: Correlation Matrix
    numerical_df = df[['Maths', 'Science', 'English', 'Attendance_Percent', 'Study_Hours_Per_Week']]
    corr = numerical_df.corr()
    cax = axes[2].matshow(corr, cmap='coolwarm')
    fig.colorbar(cax, ax=axes[2])

    for (i, j), z in np.ndenumerate(corr):
        axes[2].text(j, i, f'{z:0.2f}', ha='center', va='center', color='black' if abs(z) < 0.5 else 'white')

    axes[2].set_xticks(range(len(corr.columns)))
    axes[2].set_yticks(range(len(corr.columns)))
    
    # Use shorter labels to fit well
    labels = ['Maths', 'Science', 'English', 'Attendance', 'Study Hrs']
    axes[2].set_xticklabels(labels, rotation=45, ha='left')
    axes[2].set_yticklabels(labels)
    axes[2].set_title('Subject & Metric Correlation', pad=20)
    axes[2].xaxis.set_ticks_position('bottom')

    plt.tight_layout()
    
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=150)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    return plot_url
