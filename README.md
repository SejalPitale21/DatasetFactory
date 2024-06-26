# Dataset Factory

This project provides a FastAPI-based application to handle file uploads, generate summary statistics, perform data transformations, and visualize data from CSV files.

## Features

- Upload CSV files
- Get summary statistics for the uploaded files
- Apply data transformations (e.g., normalization, filling missing values)
- Visualize data (histograms, scatter plots)

## Prerequisites

- Python 3.7+
- pip (Python package installer)
- git (to clone the repository)

## Installation

1. **Clone the repository:**

    ```sh
    git clone <repo>
    cd dataset-factory
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the FastAPI server:**

    ```sh
    uvicorn main:app --host 127.0.0.1 --port 5049 --reload
    ```

2. **Access the API documentation:**

    Open your browser and go to `http://127.0.0.1:5049/docs` to view the automatically generated API documentation.

## API Endpoints

### Upload a CSV File

- **URL:** `/upload`
- **Method:** `POST`
- **Request:** `csv file path`
- **Response:** JSON with `message` and `file_id`

    ```sh
    curl -X POST "http://127.0.0.1:5049/upload" -F "file=@/path/to/yourfile.csv"
    ```

### Get Summary Statistics

- **URL:** `/summary/{file_id}`
- **Method:** `GET`
- **Response:** JSON with summary statistics

    ```sh
    curl -X GET "http://127.0.0.1:5049/summary/{file_id}"
    ```

### Transform Data

- **URL:** `/transform/{file_id}`
- **Method:** `POST`
- **Request:** JSON with transformation rules
- **Response:** JSON with `message` and `file_id` of the transformed file

    ```sh
    curl -X POST "http://127.0.0.1:5049/transform/{file_id}" -H "Content-Type: application/json" -d '{
        "transformations": {
            "normalize": ["columnName"],
            "fill_missing": {"columnName": 0}
        }
    }'
    ```

### Visualize Data

- **URL:** `/visualize/{file_id}`
- **Method:** `GET`
- **Response:** JSON with `message`, `plot_url`, and `file_path`

    ```sh
    curl -X GET "http://127.0.0.1:5049/visualize/{file_id}?chart_type=histogram&columns=columnName"
    ```

### Static Files

- **URL:** `/files/{path}`
- **Method:** `GET`
- **Response:** Serves static files from the `uploads` directory

## Running Tests

1. **Install test dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

2. **Run the tests using pytest:**

    ```sh
    pytest
    ```

## Project Structure

- `main.py`: Contains FastAPI endpoints.
- `fileService.py`: Contains the implementation of the service functions.
- `requirements.txt`: Lists the dependencies required to run the application.
