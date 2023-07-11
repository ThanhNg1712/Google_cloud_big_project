import pandas as pd
from google.cloud import bigquery
import json
import gcsfs

def hello_gcs(event, context):
  

    lst = []
    file_name = event['name']
    table_name = file_name.split('.')[0]

    dct = {
        'Event_ID': context.event_id,
        'Event_type': context.event_type,
        'Bucket_name': event['bucket'],
        'File_name': event['name'],
        'Created': event['timeCreated'],
        'Updated': event['updated']
    }
    lst.append(dct)
    df_metadata = pd.DataFrame.from_records(lst)
    df_metadata.to_gbq('tiki_product.data_loading_metadata',
                       project_id='tiki-project-390622',
                       if_exists='append',
                       location='us')

  
    fs = gcsfs.GCSFileSystem()
    with fs.open(event['bucket'] + '/' + file_name, 'r') as file:
        json_data = file.readlines()
        data_list = [json.loads(line) for line in json_data]

    df_data = pd.DataFrame.from_records(data_list)

    client = bigquery.Client(project='tiki-project-390622')
    table_ref = client.dataset('tiki_product').table(table_name)
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    client.load_table_from_dataframe(df_data, table_ref, job_config=job_config)
