import requests
import random

BASE_URL = 'http://127.0.0.1:5000'
NUM_SENSORS = 35  

def generate_random_sensor():
    sensor_id = random.randint(1, 99)
    sensor_name = f"Sensor-{sensor_id}"
    sensor_location = f"Location-{random.randint(1, 50)}"
    
    return {
        'name': sensor_name,
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

def create_random_sensors():
    for _ in range(NUM_SENSORS):
        sensor_data = generate_random_sensor()
        create_sensor(sensor_data)

if __name__ == '__main__':
    create_random_sensors()
