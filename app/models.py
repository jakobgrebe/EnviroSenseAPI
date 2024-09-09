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
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id', ondelete='CASCADE'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    value = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'timestamp': self.timestamp,
            'value': self.value
        }
