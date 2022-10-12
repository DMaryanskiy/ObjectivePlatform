from google.cloud import bigquery
from fastapi import APIRouter
from dotenv import load_dotenv
from ruamel.yaml import YAML

from .models import Crime
from .utils import query_to_json

load_dotenv() # loading google credentials

yaml = YAML(typ='safe')
properties = yaml.load(open('config.yml')) # loading querys from configs

client = bigquery.Client() # binding connection with BigQuery

router = APIRouter() # creating router


@router.get('/', status_code=200, response_model=list[Crime])
def get_all_crimes():
    """
    Endpoint to get all crimes in Chicago.
    Returns: JSON object with coordinates of crimes.
    """
    query_job = client.query(query=properties['GET_ALL_CRIMES'])
    crimes_json = query_to_json(query_job)
    return crimes_json

@router.get('/type', status_code=200, response_model=list[Crime])
def get_crimes_by_type(primary_type: str):
    """
    Endpoint to get crimes in Chicago by their type.
    Args:
        primary_type: type of crime.
    Returns: JSON object with coordinates of crimes.
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('primary_type', 'STRING', primary_type)
        ]
    )
    query_job = client.query(query=properties['GET_CRIMES_BY_TYPE'], job_config=job_config)
    crimes_json = query_to_json(query_job)
    return crimes_json

@router.get('/date', status_code=200, response_model=list[Crime])
def get_crimes_by_type(date: str):
    """
    Endpoint to get crimes in Chicago by their date.
    Args:
        date: date of crime.
    Returns: JSON object with coordinates of crimes.
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('date', 'TIMESTAMP', date)
        ]
    )
    query_job = client.query(query=properties['GET_CRIMES_BY_DATE'], job_config=job_config)
    crimes_json = query_to_json(query_job)
    return crimes_json
