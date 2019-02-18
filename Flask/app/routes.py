from datetime import datetime
from flask import render_template
import csv
from app import app

@app.route('/')
@app.route('/index')
def index():
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    statistics = []

    with open('PeriodicStatistics.csv') as file:
        reader = csv.reader(file,delimiter=',')
        statistics = [row for row in reader]

    return render_template('index.html', today=today, statistics=statistics)