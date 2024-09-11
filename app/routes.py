from flask import request, jsonify
from app import app, db
from app.models import Sensor, SensorData
from datetime import datetime
from sqlalchemy import text

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

    if not data or 'value' not in data or 'timestamp' not in data:
        return jsonify({"error": "Missing 'value' or 'timestamp' in request data"}), 400

    try:
        value = float(data['value'])
        timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')  # Ensure correct format

        soil_moisture = float(data.get('soil_moisture', 0.0))
        soil_ph = float(data.get('soil_ph', 0.0))
        nutrient_n = float(data.get('nutrient_n', 0.0))
        nutrient_p = float(data.get('nutrient_p', 0.0))
        nutrient_k = float(data.get('nutrient_k', 0.0))
        soil_temperature = float(data.get('soil_temperature', 0.0))

        new_data = SensorData(
            sensor_id=sensor.id,
            timestamp=timestamp,
            soil_moisture=soil_moisture,
            soil_ph=soil_ph,
            nutrient_n=nutrient_n,
            nutrient_p=nutrient_p,
            nutrient_k=nutrient_k,
            soil_temperature=soil_temperature,
            value=value
        )

        db.session.add(new_data)
        db.session.commit()

        return jsonify(new_data.serialize()), 201

    except ValueError as e:
        return jsonify({"error": f"Invalid data format: {e}"}), 400

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/sensors/<int:sensor_id>/data', methods=['GET'])
def get_sensor_data(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Paginate sensor data for the given sensor
    data = SensorData.query.filter_by(sensor_id=sensor.id).paginate(page=page, per_page=per_page)

    return jsonify({
        "sensor_data": [d.serialize() for d in data.items],
        "total": data.total,
        "pages": data.pages,
        "current_page": data.page
    }), 200
    

@app.route('/reset-sensors', methods=['POST'])
def reset_sensors():
    try:
        db.session.query(SensorData).delete()

        db.session.query(Sensor).delete()

        db.session.execute(text("ALTER SEQUENCE sensor_id_seq RESTART WITH 1"))
        db.session.execute(text("ALTER SEQUENCE sensor_data_id_seq RESTART WITH 1"))

        db.session.commit()

        return jsonify({"message": "All sensors and sensor data deleted, and ID sequences reset."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

