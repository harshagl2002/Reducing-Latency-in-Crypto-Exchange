import json
import itertools
import boto3
from itertools import product
from typing import List, Dict


class EC2Manager:
    def __init__(self, key, secret, region_name):
        self.ec2 = boto3.resource(
            "ec2",
            aws_access_key_id = key,
            aws_secret_access_key = secret,
            region_name = region_name
        )

    def create_instance(self, image_id: str, instance_type: str, key_name: str, security_groups_ids: List[str],
                         subnetId: str, user_data_script: str, volume_size: int, tags: List[Dict[str, str]]) -> str:
        instance = self.ec2.create_instances(
            ImageId = image_id,
            MinCount = 1,
            MaxCount = 1,
            InstanceType = instance_type,
            KeyName = key_name,
            SecurityGroupIds = security_groups_ids,
            SubnetId = subnetId,
            UserData = user_data_script,
            BlockDeviceMappings = [
                {
                    "DeviceName": "/dev/xvda",
                    "Ebs": {
                        "VolumeSize": volume_size,
                        "VolumeType": "gp3"
                    }
                }
            ],
            TagSpecifications=[
                {
                    "ResourceType": "instance",
                    "Tags": tags
                }
            ],
            IamInstanceProfile={"Name": "S3-Access"}
        )
        return instance[0].id

    def terminate_instance(self, instance_id: str) -> None:
        self.ec2.Instance(instance_id).terminate()

    def stop_instance(self, instance_id: str) -> None:
        self.ec2.Instance(instance_id).stop()
    
    def start_instance(self, instance_id: str) -> None:
        self.ec2.Instance(instance_id).start()

    def get_instance_status(self, instance_id: str) -> str:
        return self.ec2.Instance(instance_id).state["Name"]
    
    def get_all_instances(self) -> List[Dict[str, str]]:
        return [{"instance_id": instance.id, "state": instance.state["Name"]} for instance in self.ec2.instances.all()]


