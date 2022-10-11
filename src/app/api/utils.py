import json
from google.cloud import bigquery

def query_to_json(query_job: bigquery.QueryJob) -> list:
    """ function to cast QueryJob object as JSON """
    df = query_job.to_dataframe()
    json_str = df.to_json(orient='records', force_ascii=False)
    return json.loads(json_str)