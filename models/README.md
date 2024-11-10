# Network Intrusion Detection System API

This repository contains a Flask-based RESTful API for predicting network attacks using multiple trained models. The API hosts three models that can detect various types of network intrusions. Users can send JSON payloads to predict the attack category, based on different datasets.

## Features

- **UNSW NB-15 Model**: Predicts attack types from the UNSW NB-15 dataset.
- **CIC IDS 2018 Model**: Predicts attack types from the CIC IDS 2018 dataset.
- **KDD Model**: Binary classifier (Normal or Attack) based on the KDD dataset.
- **Web Interface**: Allows users to test predictions with a simple web form.

## Models and Attack Categories

Each model has specific attack categories, defined as follows:

### UNSW NB-15 Model

- Categories: `analysis`, `backdoor`, `backdoors`, `dos`, `exploits`, `fuzzers`, `generic`, `normal`, `reconnaissance`, `shellcode`, `worms`

### CIC IDS 2018 Model

- Categories: `Benign`, `Bot`, `DDOS attack-HOIC`, `DDoS attacks-LOIC-HTTP`, `DoS attacks-GoldenEye`, `DoS attacks-Hulk`, `DoS attacks-SlowHTTPTest`, `DoS attacks-Slowloris`, `FTP-BruteForce`, `Infiltration`, `SSH-Bruteforce`

### KDD Model

- Categories: `Normal`, `Attack`

## Setup Instructions

### Prerequisites

- Python 3.7+
- Flask
- TensorFlow
- Joblib
- Pandas
- Numpy

### Install Dependencies

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

### Model Files

Place the trained model files in the root directory:

- `lgb_model_unsw_15.pkl`
- `lgb_model_cic_ids_2018.pkl`
- `kdd_model.h5`

### Run the Application

To start the Flask application:

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`.

## API Endpoints

The API exposes three endpoints to interact with each model.

### 1. UNSW NB-15 Model Prediction

- **URL**: `/predict/unsw_15`
- **Method**: `POST`
- **Request Payload**:

  ```json
  {
    "feature1": value1,
    "feature2": value2,
    ...
  }
  ```

- **Response**:

  ```json
  {
    "predicted_class": "attack_category",
    "class_id": category_id
  }
  ```

### 2. CIC IDS 2018 Model Prediction

- **URL**: `/predict/cic_ids_2018`
- **Method**: `POST`
- **Request Payload**:

  ```json
  {
    "feature1": value1,
    "feature2": value2,
    ...
  }
  ```

- **Response**:

  ```json
  {
    "predicted_class": "attack_category",
    "class_id": category_id
  }
  ```

### 3. KDD Model Prediction

- **URL**: `/predict/kdd`
- **Method**: `POST`
- **Request Payload**:

  ```json
  {
    "feature1": value1,
    "feature2": value2,
    ...
  }
  ```

- **Response**:

  ```json
  {
    "predicted_class": "attack_category",
    "class_id": category_id
  }
  ```

## Web Interface

The application includes a simple HTML form for testing the models:

- **URL**: `/`
- **Description**: Users can enter JSON-formatted input data and select the model type (`unsw_15`, `cic_ids_2018`, or `kdd`) for prediction.

## Error Handling

If an error occurs during prediction, the API returns a JSON response with an error message:

```json
{
  "error": "error message"
}
```
