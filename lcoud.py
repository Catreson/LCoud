import boto3
import json
import os
import re


if os.path.isfile('pass.json'):
    with open('pass.json', 'r') as file:
        passy = json.load(file)
    os.environ["AWS_DEFAULT_REGION"] = 'eu-central-1'
    os.environ["AWS_ACCESS_KEY_ID"] = passy['AWS_ACCESS_KEY_ID']
    os.environ["AWS_SECRET_ACCESS_KEY"] = passy['AWS_SECRET_ACCESS_KEY']

if not (os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY")):
    raise Exception("Missing ENV")


def upload_file(bucket, l_path : str, d_path : str) -> None:
    local_path = os.path.normpath(l_path)
    if not os.path.isfile(local_path):
        print('File does not exist\n')
        return
    
    dest_path = d_path
    if not dest_path:
        dest_path = os.path.basename(local_path)
    if not dest_path.startswith('a-wing'):
        dest_path = 'a-wing/' + dest_path

    bucket.upload_file(local_path, dest_path)

    print('Successfully uploaded file\n')


def get_filtered_files(bucket, filter : str, dir : str) -> list:
    return [obj for obj in bucket.objects.filter(Prefix=dir) if re.search(filter, obj.key)]


def print_files(bucket, dir : str) -> None:
    print(f'Content of bucket {bucket.name}/{dir}')
    files = get_filtered_files(bucket, '', dir)
    for obj in bucket.objects.filter(Prefix=dir):
        print(obj.key)
    print('Successfully printed content\n')


def print_filtered_files(bucket, filter : str, dir : str) -> None:
    print(f'Content of bucket {bucket.name}/{dir} filtered using {filter}')
    files = get_filtered_files(bucket, filter, dir)
    for file in files:
        print(file.key)
    print('Successfully printed filtered content\n')


def delete_matching_files(bucket, filter : str, dir : str) -> None:
    files = get_filtered_files(bucket, filter, dir)
    decision = ''
    for file in files:
        decision = 'YES' if decision == 'YES' else input(f'Delete {file.key}? (y if yes, YES if yes for all):\t')
        if decision == 'y' or decision == 'YES':
            file.delete()
    print('Successfully deleted filtered files\n')


if __name__ == "__main__":
    s3 = boto3.resource(service_name='s3')
    bucket = s3.Bucket('developer-task')
    
    print_files(bucket, 'a-wing/')

    local_path = input('Path to local file:\t')
    dest_path = input('Destination:\t')
    upload_file(bucket, local_path, dest_path)

    re_filter = input('Provide regex filter for printing:\t')
    print_filtered_files(bucket, re_filter, 'a-wing/')

    re_filter = input('Provide regex filter for deletion:\t')
    delete_matching_files(bucket, re_filter, 'a-wing/')

