# EnviroSenseAPI

## Overview

EnviroSenseAPI is a Flask-based API designed to collect, store, and manage real-time environmental data from IoT sensors. It is focused on tracking data such as soil moisture, pH levels, and nutrient values, which are crucial for agricultural purposes. The API is backed by a PostgreSQL database and can handle real-time sensor data simulation.

The API allows for managing sensors, adding new data, retrieving sensor data, and resetting sensor and data records.

## Features
- Create and manage IoT sensors
- Add real-time environmental data for each sensor
- Retrieve and view sensor data with pagination support
- Simulate sensor data using a Python script
- Reset sensors and sensor data, resetting ID sequences

## Requirements

Before using the API, ensure that you have the following installed:

1. **Python 3.8+**
   - [Download Python](https://www.python.org/downloads/)
2. **PostgreSQL**
   - [Install PostgreSQL](https://www.postgresql.org/download/)
3. **pgAdmin** (Optional for database management)
   - [Download pgAdmin](https://www.pgadmin.org/download/)
4. **Flask** (Web framework)
   ```bash
   pip install Flask
   ```
5. **psycopg2** (PostgreSQL integration for Python)
   ```bash
   pip install psycopg2-binary
   ```

## Installation & Setup

### Step 1: Clone the Repository
Clone the EnviroSenseAPI repository from GitHub:

```bash
git clone https://github.com/yourusername/EnviroSenseAPI.git
cd EnviroSenseAPI
```

### Step 2: Set Up Virtual Environment
It is recommended to create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: `venv\Scripts\activate`
```

### Step 3: Install Dependencies
Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 4: Set Up PostgreSQL Database
1. Use `pgAdmin` to create a new PostgreSQL database (e.g., `envirodb`).
2. The `Sensor` and `SensorData` tables are created when running Flask.

3. Run the Flask API:

```bash
flask run
```

4. Use `pgAdmin` or SQL queries to manage and view the tables.

### Step 5: Configure Environment Variables
Configure your PostgreSQL credentials in a `.env` file in the project root:

```bash
DATABASE_URL=postgresql://<username>:<password>@localhost/envirodb
```

### Step 6: Run the API
Start the Flask API:

```bash
flask run
```

The API will be running locally on `http://127.0.0.1:5000` (update the URL if your setup differs).

### Step 7: Create and Simulate Sensor Data
In order to run these Python scripts you will need to open a new terminal as the Flask API will be running in the current terminal. Sensors first need to be created in order for data to be added. 10 data sensors will be created once running this Python script:

```bash
python create_sensors.py
```

Simulate sensor data using the Python script. The script will run continuosly updating the data every 30 seconds or until closed using "CTRL - C" :

```bash
python simulate_data.py
```

Once done with the sensors and the simulation the sensors and data can be removed using this Python script. This will delete all sensors and data, clearing the database.

```bash
python reset_sensors.py
```


## Usage

### Available API Endpoints

1. **Get All Sensors**
   - `GET /sensors`
   - Retrieve a list of all sensors.

2. **Create a Sensor**
   - `POST /sensors`
   - Create a new sensor for tracking environmental data.
   - Example request:
     ```json
     {
       "name": "Soil Sensor A",
       "location": "Field 1"
     }
     ```

3. **Get a Specific Sensor**
   - `GET /sensors/{sensor_id}`
   - Retrieve a specific sensor by its ID.

4. **Update a Sensor**
   - `PUT /sensors/{sensor_id}`
   - Update the name or location of a specific sensor.

5. **Delete a Sensor**
   - `DELETE /sensors/{sensor_id}`
   - Remove a sensor and all related sensor data.
   - Example:
     ```bash
     curl -X DELETE http://127.0.0.1:5000/sensors/1
     ```
   - Example response:
     ```json
     {
       "message": "Sensor and associated data deleted successfully"
     }
     ```

6. **Add Sensor Data**
   - `POST /sensors/{sensor_id}/data`
   - Add environmental data to a specific sensor.
   - Example request:
     ```json
     {
       "value": 23.4,
       "timestamp": "2024-09-11 12:45:00",
       "soil_moisture": 0.5,
       "soil_ph": 6.8,
       "nutrient_n": 1.2,
       "nutrient_p": 0.3,
       "nutrient_k": 0.4,
       "soil_temperature": 20.0
     }
     ```

7. **Get Sensor Data**
   - `GET /sensors/{sensor_id}/data?page={page}&per_page={per_page}`
   - Retrieve paginated data for a specific sensor.
   - Example response:
     ```json
     {
       "sensor_data": [
         {
           "id": 1,
           "sensor_id": 1,
           "timestamp": "2024-09-11 12:45:00",
           "soil_moisture": 0.5,
           "soil_ph": 6.8,
           "nutrient_n": 1.2,
           "nutrient_p": 0.3,
           "nutrient_k": 0.4,
           "soil_temperature": 20.0,
           "value": 23.4
         }
       ],
       "total": 10,
       "pages": 1,
       "current_page": 1
     }
     ```

8. **Reset Sensors**
   - `POST /reset-sensors`
   - Deletes all sensors and their data, resetting the ID sequences for both the `Sensor` and `SensorData` tables.
   - Example response:
     ```json
     {
       "message": "All sensors and sensor data deleted, and ID sequences reset."
     }
     ```

## Database Structure

- **Sensor Table**: Stores sensor information (ID, name, location, created_at).
- **SensorData Table**: Stores environmental data collected by each sensor (timestamp, soil moisture, pH, nutrients, etc.).

## Future Enhancements

- Real-time data streaming via WebSocket or MQTT.
- Integration with a live web dashboard to visualize sensor data.
- Support for additional sensor types and custom data fields.
