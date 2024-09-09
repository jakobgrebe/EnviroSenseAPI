### GET /sensors
- **Description**: Retrieves all sensors
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Soil Moisture Sensor",
      "location": "Field A",
      "created_at": "2024-09-01T12:34:56"
    }
  ]
  ```

### POST /sensors
- **Description**: Creates a new sensor
- **Input**: JSON object with sensor details (name, location)
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Soil Moisture Sensor",
    "location": "Field A",
    "created_at": "2024-09-01T12:34:56"
  }
  ```
