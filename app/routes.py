from flask import request, jsonify
from app import app, db
from app.models import Sensor, SensorData

@app.route('/sensors', methods=['GET'])
def get_sensors():
    sensors = Sensor.query.all()
    return jsonify([sensor.serialize() for sensor in sensors])

@app.route('/sensors', methods=['POST'])
def create_sensor():
    data = request.json
    new_sensor = Sensor(name=data['name'], location=data['location'])
    db.session.add(new_sensor)
    db.session.commit()
    return jsonify(new_sensor.serialize()), 201
