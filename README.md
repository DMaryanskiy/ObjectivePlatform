# Test task for Objective Platform

## Description

It's a small app consisting of two services: Streamlit dashbord and FastAPI API.
This service uses public BigQuery dataset of crimes commited in Chicago to show their location on map.
User may filter crimes by date and their type.

## Installation

1. Clone repo from GitHub.
2. Create file `src/app/.env` and put there `GOOGLE_APPLICATION_CREDENTIALS="./google_credentials/<path_to_json_with_credentials>"`.
To get credentials, use this [link](https://cloud.google.com/bigquery/docs/reference/libraries#setting_up_authentication).
3. Put JSON with credentials to `src/app/google_credentials`.
4. Go to `src` directory.
5. Enter `docker-compose up`.
6. Open [localhost:8501](localhost:8501)
