from flask import request, jsonify
from app import app, db
from app.models import Sensor, SensorData

@app.route('/sensors', methods=['GET'])
def get_sensors():
    sensors = Sensor.query.all()
    return jsonify([sensor.serialize() for sensor in sensors]), 200

@app.route('/sensors', methods=['POST'])
def create_sensor():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({"error": "Missing 'name' in request data"}), 400
    
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

    if not data:
        return jsonify({"error": "No data provided for update"}), 400
    
    sensor.name = data.get('name', sensor.name)
    sensor.location = data.get('location', sensor.location)

    db.session.commit()
    return jsonify(sensor.serialize()), 200

@app.route('/sensors/<int:sensor_id>', methods=['DELETE'])
def delete_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)

    sensor_data_exists = SensorData.query.filter_by(sensor_id=sensor.id).first()
    if sensor_data_exists:
        return jsonify({"error": "Cannot delete sensor while related sensor data exists"}), 400

    db.session.delete(sensor)
    db.session.commit()
    
    return '', 204

@app.route('/sensors/<int:sensor_id>/data', methods=['POST'])
def add_sensor_data(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    data = request.get_json()

    if not data or 'value' not in data:
        return jsonify({"error": "Missing 'value' in request data"}), 400

    try:
        value = float(data['value'])
    except ValueError:
        return jsonify({"error": "'value' must be a number"}), 400

    new_data = SensorData(sensor_id=sensor.id, value=value)
    db.session.add(new_data)
    db.session.commit()

    return jsonify(new_data.serialize()), 201

@app.route('/sensors/<int:sensor_id>/data', methods=['GET'])
def get_sensor_data(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    data = SensorData.query.filter_by(sensor_id=sensor.id).paginate(page=page, per_page=per_page)
    
    return jsonify({
        "sensor_data": [d.serialize() for d in data.items],
        "total": data.total,
        "pages": data.pages,
        "current_page": data.page
    }), 200
