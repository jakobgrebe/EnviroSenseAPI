import requests

BASE_URL = 'http://127.0.0.1:5000'

def reset_sensors():
    try:
        response = requests.post(f'{BASE_URL}/reset-sensors')

        if response.status_code == 200:
            print("Sensors deleted, and ID sequence reset.")
        else:
            print(f"Failed to reset sensors: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    reset_sensors()
