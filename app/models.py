from app import db

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    value = db.Column(db.Float, nullable=False)
