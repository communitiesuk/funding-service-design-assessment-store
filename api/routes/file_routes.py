import boto3


def download_file(filename: str):
    url = boto3.client('s3').generate_presigned_url(
    ClientMethod='get_object', 
    Params={'Bucket': 'BUCKET_NAME', 'Key': 'OBJECT_KEY'},
    ExpiresIn=3600)