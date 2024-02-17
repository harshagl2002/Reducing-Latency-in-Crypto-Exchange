from python_api_tests.urllib_client import UrllibClient
from python_api_tests.requests_client import RequestsClient
from python_api_tests.httpx_client import HttpxClient
from s3_manager.s3manager import S3Manager

import time
import pandas as pd
import os
import json
import argparse
import requests
import random
import psutil
from datetime import datetime, timedelta



def load_config(filename="Configs/binance_configs.json"):
    with open(filename) as js_file:
        config = json.load(js_file)
    return config["apiKey"], config["secret"]

def init_client(client_type, apiKey, secret, alive):
    if client_type == "requests":
        return RequestsClient(apiKey, secret, alive)
    elif client_type == "urllib":
        return UrllibClient(apiKey, secret)
    elif client_type == "httpx":
        return HttpxClient(apiKey, secret)


def latency_test(client, method, *args):
    start_time = time.time()
    if args:
        result = getattr(client, method)(*args)
    else:
        result = getattr(client, method)()
    endtime = time.time()
    return endtime-start_time, result


def get_instance_id():
    # Check documentation for more details: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html
    # IMDSv2 now requires a token
    token_url = "http://169.254.169.254/latest/api/token"
    instance_id_url = "http://169.254.169.254/latest/meta-data/instance-id"
    
    # Request a token with a time to alive of 6 hours
    token_response = requests.put(token_url, headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"})

    # If the request is successful, return the instance ID
    if token_response.status_code == 200:
        token = token_response.text
        instance_id_response = requests.get(instance_id_url, headers={"X-aws-ec2-metadata-token": token})
        if instance_id_response.status_code == 200:
            return instance_id_response.text
        else:
            raise Exception("Error retrieving instance ID")
    else:
        raise Exception("Error obtaining token")


def main(apiKey, secret, client_type, duration, filename):
    if args.keep_alive == "1":
        client = init_client(client_type, apiKey, secret, True)
    else:
        client = init_client(client_type, apiKey, secret, False)

    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration)

    if not os.path.isfile(filename):
        pd.DataFrame(columns=["timestame", "latency", "API type"]).to_csv(filename, index=False)
    
    while datetime.now() < end_time:
        try:
            # Disable the public request, this could be implemented using web socket, which is much faster than rest.
            # Public GET request
            # lat_get, _ = latency_test(client, "get_premium_index", "XRPUSDT")
            # current_time = pd.Timestamp.utcnow().timestamp()
            # new_row = {"timestamp": current_time, "latency": lat_get, "API type": "public get"}
            # with open(filename, "a") as f:
            #     pd.DataFrame([new_row]).to_csv(f, header=False, index=False)

            # POST request
            lat_post, order_id = latency_test(client, "create_order", "XRPUSDT", "BUY", 0.1, 51, "LIMIT")
            current_time = pd.Timestamp.utcnow().timestamp()
            new_row = {"timestamp": current_time, "latency": lat_post, "API type": "create_order"}
            with open(filename, "a") as f:
                pd.DataFrame([new_row]).to_csv(f, header=False, index=False)

            # DELETE request
            lat_delete, _ = latency_test(client, "cancel_order", "XRPUSDT", order_id)
            current_time = pd.Timestamp.utcnow().timestamp()
            new_row = {"timestamp": current_time, "latency": lat_delete, "API type": "cancel_order"}
            with open(filename, "a") as f:
                pd.DataFrame([new_row]).to_csv(f, header=False, index=False)

            sleep_time = random.uniform(0, 2)
            print(f"Sleep {round(sleep_time, 2)} seconds.")
            time.sleep(sleep_time)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", type=str, required=True, help="API client want to test")
    parser.add_argument("--keep_alive", type=str, required=True, help="Whether keeping the api alive")
    parser.add_argument("--process_bind", type=str, required=True, help="Whether binding scrypt to a core")
    parser.add_argument("--time", type=str, required=True, help="Number of minutes for the latency test")
    args = parser.parse_args()
    apiKey, secret = load_config()
    current_time = datetime.now()
    filename = get_instance_id() + "_" + str(time.time()) + ".csv" # Output's filename

    if args.process_bind == "1":
        p = psutil.Process(os.getpid())
        p.cpu_affinity([0])

    main(apiKey, secret, args.client, float(args.time), filename)

    
    with open('Configs/s3.json') as js_file:
        s3_config = json.load(js_file)
    bucket_name = s3_config["bucket_names"]["latency_results"]
    s3_manager = S3Manager()
    s3_manager.upload_to_s3(filename, bucket_name, filename)
    with open('args.json', 'w') as f:
        json.dump(vars(args), f, indent=4)
