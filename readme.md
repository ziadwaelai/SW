# SWTask Project

This project is a Django application designed for KPI management and data processing. It includes a structured data pipeline for ingesting sensor messages, processing them based on customizable equations, and storing the processed results. The application also provides an API for creating and linking KPIs.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)

## Overview

The SWTask project reads data from sensors, processes it using user-defined equations, and stores the results in a database. It’s designed to be easily extensible, following SOLID principles and best practices in software design.

### Key Components
1. **Data Ingestor**: Reads sensor messages from a text file at a specified frequency.
2. **Processing Engine**: Interprets and applies arithmetic or regex-based equations to the ingested data.
3. **Message Producer**: Stores the processed message results in a relational database.
4. **Django API**: Provides endpoints for managing KPIs and linking assets to them.

## Features

- Real-time data ingestion from text files
- Equation processing with arithmetic and regex support
- API for managing KPIs and linking assets
- Automated testing and Swagger documentation for endpoints

## Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/ziadwaelai/SW.git
   cd swTask
   ```

2. **Create and Activate a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**:

   ```bash
   python manage.py runserver
   ```

6. **Access Swagger Documentation** (if enabled):

   Visit [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) to view and test the API documentation.

## Usage

### Running the Data Pipeline

You can start the data ingestion and processing pipeline by using the custom Django management command:

```bash
python manage.py run_pipeline --file_path="messages.txt" --equation="ATTR+50*(ATTR/10)" --kpi_id=1
```

This command will:
- Read sensor messages from `messages.txt`.
- Process each message using the equation `ATTR+50*(ATTR/10)`.
- Store the processed result in the database linked to the specified KPI.

## API Endpoints

The API allows for creating, retrieving, updating, and linking KPIs. Here’s an overview of the main endpoints:

### 1. **List KPIs**
   - **Endpoint**: `/api/kpi/`
   - **Method**: `GET`
   - **Description**: Retrieves a list of all KPIs.
   - **Response**:
     ```json
     [
       {
         "id": 1,
         "name": "Sample KPI",
         "expression": "ATTR+10",
         "description": "Sample description"
       }
     ]
     ```

### 2. **Create a KPI**
   - **Endpoint**: `/api/kpi/`
   - **Method**: `POST`
   - **Description**: Creates a new KPI.
   - **Request Body**:
     ```json
     {
       "name": "Test KPI",
       "expression": "ATTR + 10",
       "description": "Optional description"
     }
     ```
   - **Response**:
     ```json
     {
       "id": 2,
       "name": "Test KPI",
       "expression": "ATTR + 10",
       "description": "Optional description"
     }
     ```

### 3. **Link an Asset to a KPI**
   - **Endpoint**: `/api/kpi/<kpi_id>/link_asset/`
   - **Method**: `POST`
   - **Description**: Links an asset to a specific KPI and stores the processed result.
   - **Request Body**:
     ```json
     {
       "asset_id": "123",
       "value": "15"
     }
     ```
   - **Response**:
     ```json
     {
       "id": 1,
       "asset_id": "123",
       "kpi": 2,
       "timestamp": "2023-07-31T23:28:37Z",
       "value": "15"
     }
     ```

## Testing

To run automated tests, use the following command:

```bash
python manage.py test KPI
```

The tests cover the following functionalities:
- **Model Testing**: Ensures that KPI and AssetKPI models are created and linked properly.
- **API Testing**: Tests KPI creation, listing, and linking of assets to KPIs.

Sample test cases in `KPI/tests.py`:
```python
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import KPI

class KPIAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.kpi_data = {"name": "Test KPI", "expression": "ATTR + 10"}
        self.kpi = KPI.objects.create(**self.kpi_data)

    def test_create_kpi(self):
        response = self.client.post('/api/kpi/', self.kpi_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_kpis(self):
        response = self.client.get('/api/kpi/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_link_asset_to_kpi(self):
        response = self.client.post(f'/api/kpi/{self.kpi.id}/link_asset/', {"asset_id": "123", "value": "15"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```