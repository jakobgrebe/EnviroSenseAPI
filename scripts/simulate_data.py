import requests
import random
from datetime import datetime, timedelta

BASE_URL = 'http://127.0.0.1:5000'
NUM_ENTRIES = 100  

def get_sensors():
    """Fetch the list of available sensors from the API."""
    response = requests.get(f'{BASE_URL}/sensors')
    
    if response.status_code == 200:
        sensors = response.json()
        return [sensor['id'] for sensor in sensors]  
    else:
        print(f"Error fetching sensors: {response.status_code}")
        return []

def generate_soil_health_data(sensor_id):
    """Simulate a single sensor data entry for soil health."""
    soil_moisture = round(random.uniform(10.0, 60.0), 2)  
    soil_ph = round(random.uniform(5.0, 7.5), 2)  
    nutrient_n = round(random.uniform(1.0, 10.0), 2)  
    nutrient_p = round(random.uniform(1.0, 10.0), 2)  
    nutrient_k = round(random.uniform(1.0, 10.0), 2)  
    soil_temperature = round(random.uniform(15.0, 30.0), 2)  
    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 60))  

    value = soil_moisture

    return {
        'sensor_id': sensor_id,
        'soil_moisture': soil_moisture,
        'soil_ph': soil_ph,
        'nutrient_n': nutrient_n,
        'nutrient_p': nutrient_p,
        'nutrient_k': nutrient_k,
        'soil_temperature': soil_temperature,
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'value': value  
    }


def simulate_large_soil_data_submission():
    sensors = get_sensors()  
    
    if not sensors:
        print("No sensors available to add data.")
        return

    for _ in range(NUM_ENTRIES):
        sensor_id = random.choice(sensors)  
        data = generate_soil_health_data(sensor_id)

        try:
            response = requests.post(f'{BASE_URL}/sensors/{sensor_id}/data', json=data)
            if response.status_code == 201:
                print(f"Successfully sent data for sensor {sensor_id}: {data}")
            else:
                print(f"Failed to send data for sensor {sensor_id}: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error sending data: {e}")

if __name__ == '__main__':
    simulate_large_soil_data_submission()
