from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the database (SQLite in this example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the data model
class Insight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    end_year = db.Column(db.String(255))
    intensity = db.Column(db.Integer)
    sector = db.Column(db.String(255))
    topic = db.Column(db.String(255))
    insight = db.Column(db.String(255))
    url = db.Column(db.String(255))
    region = db.Column(db.String(255))
    start_year = db.Column(db.String(255))
    impact = db.Column(db.String(255))
    added = db.Column(db.String(255))
    published = db.Column(db.String(255))
    country = db.Column(db.String(255))
    relevance = db.Column(db.Integer)
    pestle = db.Column(db.String(255))
    source = db.Column(db.String(255))
    title = db.Column(db.String(255))
    likelihood = db.Column(db.Integer)

# Create database tables
with app.app_context():
    db.create_all()

# Insert sample data into the database
with open('jsondata.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)
    with app.app_context():
        for entry in json_data:
            db.session.add(Insight(**entry))
        db.session.commit()

# Define API endpoint to get data
@app.route('/api/data')
def get_data():
    data = Insight.query.all()
    result = [{'id': entry.id, 'intensity': entry.intensity, 'likelihood': entry.likelihood,
               'relevance': entry.relevance, 'year': entry.added.split()[-1],
               'country': entry.country, 'topic': entry.topic, 'region': entry.region,
               'city': entry.impact, 'sector': entry.sector, 'pestle': entry.pestle,
               'source': entry.source}
              for entry in data]
    return jsonify(result)

# Define HTML template for the dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
