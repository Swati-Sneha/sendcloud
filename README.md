# Timer Project

## Overview
This project provides a timer service with a REST API. The service allows setting timers and querying their status. It is designed to be deployed using Docker.

## Setup and Running

### Running in Docker
1. Build the Docker images:
    ```sh
    docker-compose build
    ```

2. Start the Docker containers in detached mode:
    ```sh
    docker-compose up -d
    ```

### Accessing Endpoints

##### POST Timer Request
To set a timer, send a POST request to the `/timer` endpoint with the following curl command:

```sh
curl --location --request POST 'http://localhost:8000/timer' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "https://example.com",
    "hours": 0,
    "minutes": 0,
    "seconds": 30
}'
```

#### GET Timer Status
To get the status of a timer, use the timer ID returned from the POST request:
```sh
curl --location --request GET 'http://localhost:8000/timer/<id from POST request response>'
```

### Running Tests
```sh
sh run_tests.sh
```