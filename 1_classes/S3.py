from datetime import datetime
import boto3
import json
import pandas as pd

class S3_Handler:
    def __init__(self, bucketName="sdd-s3-bucket"):
        self.s3_client = boto3.client('s3')
        self.bucketName = bucketName
    def listFromAWS(self, base, date_obj):
        object_list = []
        # List data
        s3_objects = self.s3_client.list_objects_v2(
            Bucket=self.bucketName,
            Prefix='{}/{}/{}/{}/'.format(
                base,
                str(date_obj.year).zfill(4),
                str(date_obj.month).zfill(2),
                str(date_obj.day).zfill(2)))
        # if 'Contents' in s3_objects:
        #     print("Objects: Found " + str(len(s3_objects['Contents'])) + " elements")
        if 'Contents' not in s3_objects:
            print("Objects: Found 0 elements, skip:", date_obj)
            return False
        for key in s3_objects['Contents']:
            object_list.append(key['Key'])
        return object_list
    def readFromAWS(self, path):
        # List data
        s3_objects = self.s3_client.list_objects_v2(
            Bucket=self.bucketName,
            Prefix=path)
        # if 'Contents' in s3_objects:
            # print("Objects: Found " + str(len(s3_objects['Contents'])) + " elements")
        # else:

        if 'Contents' not in s3_objects:
            print("Objects: Found 0 elements, skip")
            return False
        # Extract data
        dataObject = self.s3_client.get_object(Bucket=self.bucketName, Key=path)
        object_body = str(dataObject["Body"].read(), 'utf-8')
        object_json = json.loads(object_body)
        return object_json
    def writeToAWS(self, base, bucket, date=datetime.now()):
        if len(bucket) > 0:
            response = self.s3_client.put_object(
                Body=json.dumps(bucket), 
                Bucket=self.bucketName,
                Key='{}/{}/{}/{}/{}'.format(
                    base,
                    str(date.year).zfill(4),
                    str(date.month).zfill(2),
                    str(date.day).zfill(2),
                    str(date.hour).zfill(2)))
            print("Response: " + str(response))
        return False
