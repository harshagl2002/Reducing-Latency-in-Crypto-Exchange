import pandas as pd
import json
import itertools
import time
import os

from ec2_manager.ec2manager import EC2Manager
from s3_manager.s3manager import S3Manager

# This is the config of your user, should store in your local machine
access_info = pd.read_csv("Configs/accessKeys.csv")
with open("Configs/machine_parameters.json") as js_file:
    machine_parameters = json.load(js_file)

# Script to intall necessary packages
with open("Configs/user-data") as f:
    USER_DATA_SCRIPT = f.read()

ACCESS_KEY = access_info["Access key ID"].iloc[0]
SECRET = access_info["Secret access key"].iloc[0]
REGION = "ap-northeast-1"
SUBNET_ID = "subnet-0dcfd56c0520d11a6"
KEY_NAME = "Test"
SECURITY_GROUP_IDS = ["sg-086c202f3c896f32e"]
VOLUME_SIZE = 8


def create_combinations(config):
    # Extract all parameter sets from the configuration
    amis = config['instances']['AMIs']['values']
    instance_types = config["instances"]["instanceType"]["values"]
    
    region_subnet_pairs = []
    # Append region and subnet together, because subnet is associated with the region
    for region, details in config['instances']['regions']['details'].items():
        for subnet in details['subnets']:
            region_subnet_pairs.append((region, subnet))

    all_combinations = list(itertools.product(amis, region_subnet_pairs, instance_types))

    formatted_combinations = [
        {'AMI': ami, 'Region': region_subnet[0], 'Subnet': region_subnet[1], "Instance Type": instance_type} for ami, region_subnet, instance_type in all_combinations
    ]

    return formatted_combinations


def test_paramters():
    key = access_info["Access key ID"].iloc[0]
    secret = access_info["Secret access key"].iloc[0]
    key_name = "Test"
    security_groups_ids = ["sg-086c202f3c896f32e"]
    volume_size = 8
    combinations = create_combinations(machine_parameters)


    for comb in combinations:
        print(comb)
        tags = [{"Key": "Name", "Value": "zone-d-24h"}]
        image_id = comb["AMI"]
        region = comb["Region"]
        subnet = comb["Subnet"]
        instance_type = comb["Instance Type"]
        tags = [{"Key": "Name", "Value": f"{region}-{subnet}-{instance_type}"}]
        ec2_manager = EC2Manager(key, secret, region)
        ec2_manager.create_instance(image_id, instance_type, key_name, security_groups_ids, subnet, user_data_script, volume_size, tags)


def hunt_engines(params):
    ec2_manager = EC2Manager(ACCESS_KEY, SECRET, REGION)
    s3_manager = S3Manager()
    if os.path.exists("Configs/Saved_Instances.csv"):
        os.remove("Configs/Saved_Instances.csv")
    s3_manager.fetch_csv_from_s3("latency-results", "Saved_Instances.csv", None).to_csv("Configs/Saved_Instances.csv", index=False)
    for i in range(params["iterations"]):
        print(f"Start iteration {i}.")
        # Create 3 instances a batch
        tags = [{"Key": "Name", "Value": f"Hunt Engine Instance"}]
        batch_instances = []
        for _ in range(params["num_batches"]):
            instance_id = ec2_manager.create_instance(params["AMI"], params["instance_type"], KEY_NAME, SECURITY_GROUP_IDS, SUBNET_ID, USER_DATA_SCRIPT, VOLUME_SIZE, tags)
            batch_instances.append(instance_id)
        
        time.sleep(180)
        time.sleep(params["test_minutes"]*60) # Sleep 60 seconds for testing
        
        for instance_id in batch_instances:
            result = s3_manager.fetch_csv_from_s3("latency-results", None, instance_id)
            if result is None:
                print(f"Cannot connect to the instance: {instance_id}.")
                ec2_manager.terminate_instance(instance_id)
                continue
            avg_latency = result["latency"].mean()
            print(f"The average latency of the instance {instance_id} is {avg_latency}.")

            saved_instances = pd.read_csv("Configs/Saved_Instances.csv")
            if len(saved_instances) < 5:
                saved_instances.loc[len(saved_instances)] = [instance_id, avg_latency]
            else:
                max_latency_row = saved_instances["average_latency"].idxmax()
                if avg_latency < saved_instances.at[max_latency_row, "average_latency"]:
                    print(f"Terminate the old instancd: {saved_instances.loc[max_latency_row, 'instance_id']}")
                    ec2_manager.terminate_instance(saved_instances.loc[max_latency_row, "instance_id"])
                    saved_instances.at[max_latency_row, "instance_id"] = instance_id
                    saved_instances.at[max_latency_row, "average_latency"] = avg_latency
                    if ec2_manager.get_instance_status(instance_id) == "running":
                        print(f"Stopped the new instance {instance_id} after testing.")
                        ec2_manager.stop_instance(instance_id)
                else:
                    print(f"Terminate the current instance {instance_id}")
                    ec2_manager.terminate_instance(instance_id)
            saved_instances.to_csv("Configs/Saved_Instances.csv", index=False)
            s3_manager.delete_file("latency-results", "Saved_Instances.csv", None)
            s3_manager.upload_to_s3("Configs/Saved_Instances.csv", "latency-results", "Saved_Instances.csv")


def main():
    """
    Could define argument
    """
    params = {
        "num_batches": 1,
        "iterations": 100,
        "AMI": "ami-012261b9035f8f938",
        "instance_type": "t2.micro",
        "test_minutes": 25
    }
    hunt_engines(params)


main()






