from flask import request, jsonify
from app import app, db
from app.models import Sensor, SensorData

@app.route('/sensors', methods=['GET'])
def get_sensors():
    sensors = Sensor.query.all()
    return jsonify([sensor.serialize() for sensor in sensors]), 200

@app.route('/sensors', methods=['POST'])
def create_sensor():
    data = request.json
    new_sensor = Sensor(name=data['name'], location=data.get('location'))
    db.session.add(new_sensor)
    db.session.commit()
    return jsonify(new_sensor.serialize()), 201

@app.route('/sensors/<int:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    return jsonify(sensor.serialize()), 200

@app.route('/sensors/<int:sensor_id>', methods=['PUT'])
def update_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    data = request.get_json()
    sensor.name = data.get('name', sensor.name)
    sensor.location = data.get('location', sensor.location)
    db.session.commit()
    return jsonify(sensor.serialize()), 200

@app.route('/sensors/<int:sensor_id>', methods=['DELETE'])
def delete_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    db.session.delete(sensor)
    db.session.commit()
    return '', 204

@app.route('/sensors/<int:sensor_id>/data', methods=['POST'])
def add_sensor_data(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    data = request.get_json()
    new_data = SensorData(sensor_id=sensor.id, value=data['value'])
    db.session.add(new_data)
    db.session.commit()
    return jsonify(new_data.serialize()), 201

@app.route('/sensors/<int:sensor_id>/data', methods=['GET'])
def get_sensor_data(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    data = SensorData.query.filter_by(sensor_id=sensor.id).all()
    return jsonify([d.serialize() for d in data]), 200
