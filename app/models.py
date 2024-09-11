from app import db

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'created_at': self.created_at
        }

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    soil_moisture = db.Column(db.Float, nullable=True)
    soil_ph = db.Column(db.Float, nullable=True)
    nutrient_n = db.Column(db.Float, nullable=True)
    nutrient_p = db.Column(db.Float, nullable=True)
    nutrient_k = db.Column(db.Float, nullable=True)
    soil_temperature = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)


    def serialize(self):
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'timestamp': self.timestamp,
            'soil_moisture': self.soil_moisture,
            'soil_ph': self.soil_ph,
            'nutrient_n': self.nutrient_n,
            'nutrient_p': self.nutrient_p,
            'nutrient_k': self.nutrient_k,
            'soil_temperature': self.soil_temperature,
            'value': self.value
        }
