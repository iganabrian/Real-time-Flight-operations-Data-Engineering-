import json
from datetime import datetime
import pathlib
from urllib.request import urlopen

URL = "https://opensky-network.org/api/states/all"

def run_bronze_ingest(**context):
    with urlopen(URL) as response:
        data = json.load(response)

    # Save the data to a JSON file with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = pathlib.Path(f"/opt/airflow/data/bronze/flights_{timestamp}.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w") as f:
        json.dump(data, f)

    context["ti"].xcom_push(key="bronze_file", value=str(output_path))
    
