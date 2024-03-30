import json

import boto3
from flask import request

import config


def get_session():
    try:
        aws_access_key_id = config.AWS_ACCESS_KEY_ID
        aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY
        session = boto3.session.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        return session
    except Exception as ex:
        return  {'error': str(ex)}


def s3_upload(cif, doc_name, doc_content, doc_format=None):
    try:
        s3 = get_session().resource('s3')
        bucket = s3.Bucket(config.AWS_BUCKET)
        # if 'upload-document' in request.url:
        #     is_decoded, decoded_doc = base64_decode(doc_content,)
        #     if is_decoded:
        #         file_path = str(cif[0]) + '/' + doc_name + '.' + doc_format  # using doc name set the file path
        #     else:
        #         return False, None
        # else:
        decoded_doc = json.dumps(doc_content)
        file_path = cif + '/' + doc_name + '.' + doc_format

        obj = s3.Object(bucket.name, file_path)
        response = obj.put(Body=decoded_doc)

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True, file_path
    except Exception as ex:
        return  {'error': str(ex)}


def s3_check_exists(file_path):
    try:
        s3 = get_session().resource('s3')
        bucket = s3.Bucket(config.AWS_BUCKET)
        return s3.meta.client.head_object(Bucket=bucket.name, Key=file_path)
    except Exception as ex:
        return  {'error': str(ex)}


def s3_read_file(file_path):
    try:
        s3 = get_session().resource('s3')
        bucket = s3.Bucket(config.AWS_BUCKET)
        data = s3.meta.client.get_object(Bucket=bucket.name, Key=file_path)
        body = data['Body'].read().decode('utf-8')
        return body
    except Exception as ex:
        return  {'error': str(ex)}

