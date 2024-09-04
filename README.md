# Port-to-Port Pricing API

## Overview

This project provides an HTTP-based API for retrieving average daily prices for shipping routes between ports or regions. It's built with Flask and PostgreSQL, containerized with Docker for easy deployment and testing.

## Features

- Retrieves average prices for shipping routes between ports or regions
- Supports date ranges up to 365 days
- Handles both specific port codes and region slugs
- Provides detailed error messages for invalid inputs
- Containerized with Docker for easy setup and deployment

## Prerequisites

- Docker
- Docker Compose

## Setup and Running

1. Clone the repository:
   ```
   git clone https://github.com/nolliia/ratestask-kacem.git
   cd ratestask-kacem
   ```

2. Build and start the containers:
   ```
   docker-compose up -d --build
   ```

This will start two containers:
- A PostgreSQL database initialized with the necessary data
- A Flask application serving the API

The API will be available at `http://localhost:5000`.

## API Usage

### Endpoint

`GET /rates`

### Query Parameters

- `date_from`: Start date (inclusive) in YYYY-MM-DD format
- `date_to`: End date (inclusive) in YYYY-MM-DD format
- `origin`: Origin port code or region slug
- `destination`: Destination port code or region slug

### Example Request

```
curl "http://localhost:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"
```

### Example Response

```json
[
    {
        "day": "2016-01-01",
        "average_price": 1112
    },
    {
        "day": "2016-01-02",
        "average_price": 1112
    },
    {
        "day": "2016-01-03",
        "average_price": null
    },
    ...
]
```

## Error Handling

The API provides detailed error messages for various scenarios:

- Missing query parameters
- Invalid date formats
- Invalid date ranges
- Non-existent port codes or region slugs
- Date ranges exceeding 365 days

## Testing

To run the automated tests:

```
docker-compose run --rm ratesapp pytest
```

## Project Structure

```
project_root/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── services.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_routes.py
├── config.py
├── run.py
├── Dockerfile
├── docker-compose.yml
├── rates.sql
├── requirements.txt
└── README.md
```

