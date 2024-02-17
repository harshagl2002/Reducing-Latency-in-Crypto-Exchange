import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd
import os

class S3Manager:
    def __init__(self, access_key_file="Configs/accessKeys.csv"):
        access_info = pd.read_csv(access_key_file)
        self.s3 = boto3.client('s3', 
                      aws_access_key_id=access_info["Access key ID"].values[0], 
                      aws_secret_access_key=access_info["Secret access key"].values[0])


    def upload_to_s3(self, file_name, bucket, s3_file_name):
        """
        Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param s3_file_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        try:
            self.s3.upload_file(file_name, bucket, s3_file_name)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    def fetch_csv_from_s3(self, bucket_name, file_name=None, sub_string=None):
        """
        :param file_name: Exact name of the file to fetch.
        :param sub_string: Substring to match files for deletion.
        :return: Will return a dataframe if we have the correct input.
        """
        if file_name is None and sub_string is None:
            print("File name and substring are not given.")
            return None
        
        if file_name is None and sub_string is not None:
            try:
                objects = self.s3.list_objects_v2(Bucket=bucket_name)["Contents"]
                filtered_objects = [obj for obj in objects if sub_string in obj["Key"]]

                if not filtered_objects:
                    print(f"No files found for given subtring: {sub_string}")
                    return None
                dataframes = []
                local_files = []
                for obj in filtered_objects:
                    file_key = obj['Key']
                    local_filename = file_key  # Extract filename from key
                    self.s3.download_file(bucket_name, file_key, local_filename)
                    print(f"Downloaded {file_key}")
                    df = pd.read_csv(local_filename)
                    dataframes.append(df)
                    local_files.append(local_filename)
                
                combined_df = pd.concat(dataframes, ignore_index=True)
                for file in local_files:
                    os.remove(file)
                return combined_df
            except Exception as e:
                print(f"An error occured: {e}")
                return None
        elif file_name is not None:
            try:
                objects = self.s3.list_objects_v2(Bucket=bucket_name)["Contents"]
                filtered_objects = [obj for obj in objects if file_name == obj["Key"]]

                if not filtered_objects:
                    print(f"No files found for given filename: {file_name}")
                    return None
                obj = objects[0]
                file_key = obj["Key"]
                local_filename = file_key
                self.s3.download_file(bucket_name, file_key, local_filename)
                print(f"Downloaded {file_key}")
                df = pd.read_csv(local_filename)
                os.remove(local_filename)
                return df
            except Exception as e:
                print(f"An error occured: {e}")
                return None  
            

    def delete_file(self, bucket_name, file_name=None, sub_string=None):
        """
        Delete file from a bucket.
        """
        if file_name is None and sub_string is None:
            print("File name and substring are not given.")
            return False

        try:
            objects = self.s3.list_objects_v2(Bucket=bucket_name)["Contents"]
            if file_name:
                # Delete specific file
                filtered_objects = [obj for obj in objects if file_name == obj["Key"]]
                if not filtered_objects:
                    print(f"No files found for given filename: {file_name}")
            else:
                # Delete files matching substring
                filtered_objects = [obj for obj in objects if sub_string in obj["Key"]]
                if not filtered_objects:
                    print(f"No files found for given substring: {sub_string}")

            for obj in filtered_objects:
                file_key = obj['Key']
                self.s3.delete_object(Bucket=bucket_name, Key=file_key)
                print(f"Deleted {file_key}")
            return len(filtered_objects) != 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
