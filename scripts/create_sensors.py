import requests
import random

BASE_URL = 'http://127.0.0.1:5000'
NUM_SENSORS = 35  

def generate_sequential_sensor(sensor_id):
    sensor_name = f"Sensor-{sensor_id}"
    sensor_location = f"Location-{random.randint(1, 50)}"
    
    return {
        'name': 'Soil ' + sensor_name,
        'location': sensor_location
    }

def create_sensor(sensor_data):
    try:
        response = requests.post(f'{BASE_URL}/sensors', json=sensor_data)
        if response.status_code == 201:
            print(f"Sensor created: {sensor_data}")
        else:
            print(f"Failed to create sensor: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error creating sensor: {e}")

def create_sequential_sensors():
    for sensor_id in range(1, NUM_SENSORS + 1):  # Loop from 1 to 35
        sensor_data = generate_sequential_sensor(sensor_id)
        create_sensor(sensor_data)

if __name__ == '__main__':
    create_sequential_sensors()
