from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize the Flask app
app = Flask(__name__)

# Configure the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define the Routine model
class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    description = db.Column(db.String(200))
    time = db.Column(db.String(10))

    def __init__(self, title, description, time):
        self.title = title
        self.description = description
        self.time = time

# Define the Routine schema
class RoutineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Routine

# Initialize the Routine schema
routine_schema = RoutineSchema()
routines_schema = RoutineSchema(many=True)

# Create the database tables
db.create_all()

# Add a test routine
test_routine = Routine(title="Test Routine", description="This is a test routine", time="12:00")
db.session.add(test_routine)
db.session.commit()

# Define the routes
@app.route('/')
def index():
    return "Welcome to the Daily Routine Management API!"

@app.route('/routines', methods=['GET'])
def get_routines():
    routines = Routine.query.all()
    return routines_schema.jsonify(routines)

@app.route('/routines/<id>', methods=['GET'])
def get_routine(id):
    routine = Routine.query.get(id)
    if routine:
        return routine_schema.jsonify(routine)
    else:
        return {"error": "Routine not found"}, 404

@app.route('/routines', methods=['POST'])
def add_routine():
    title = request.json['title']
    description = request.json['description']
    time = request.json['time']

    new_routine = Routine(title, description, time)
    db.session.add(new_routine)
    db.session.commit()

    return routine_schema.jsonify(new_routine)

@app.route('/routines/<id>', methods=['PUT'])
def update_routine(id):
    routine = Routine.query.get(id)
    if routine:
        title = request.json['title']
        description = request.json['description']
        time = request.json['time']

        routine.title = title
        routine.description = description
        routine.time = time

        db.session.commit()

        return routine_schema.jsonify(routine)
    else:
        return {"error": "Routine not found"}, 404

@app.route('/routines/<id>', methods=['DELETE'])
def delete_routine(id):
    routine = Routine.query.get(id)
    if routine:
        db.session.delete(