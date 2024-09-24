import boto3
import json
import os


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

if __name__ == "__main__":
    s3 = boto3.resource(service_name='s3')
    bucket = s3.Bucket(passy['bucket'])
    
    print_files(bucket)

    
