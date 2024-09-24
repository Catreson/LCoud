import boto3
import json
import os
import re


passy = {}
with open('pass.json', 'r') as file:
    passy = json.load(file)
os.environ["AWS_DEFAULT_REGION"] = 'eu-central-1'
os.environ["AWS_ACCESS_KEY_ID"] = passy['AWS_ACCESS_KEY_ID']
os.environ["AWS_SECRET_ACCESS_KEY"] = passy['AWS_SECRET_ACCESS_KEY']

def print_files(bucket) -> None:
    print(f'Content of bucket {bucket.name}/a-wing')
    for obj in bucket.objects.filter(Prefix="a-wing/"):
        print(obj.key)
    print('Successfully printed content\n')

def upload_file(bucket) -> None:
    inp = input("Path to local file:\t")
    local_path = os.path.normpath(inp)
    if not os.path.isfile(local_path):
        print('File does not exist\n')
        return
    dest_path = input("Destination:\t")
    if not dest_path:
        dest_path = os.path.basename(local_path)
    if not dest_path.startswith('a-wing'):
        dest_path = 'a-wing/' + dest_path
    bucket.upload_file(local_path, dest_path)
    print('Successfully uploaded file\n')

if __name__ == "__main__":
    s3 = boto3.resource(service_name='s3')
    bucket = s3.Bucket(passy['bucket'])
    
    print_files(bucket)

    upload_file(bucket)

