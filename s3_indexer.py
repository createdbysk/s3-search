import s3_walker
import elasticsearch
import boto3

def populate_index():
    session = boto3.session.Session(profile_name='sandbox')
    s3_client = session.client('s3')
    batch_size = 50

    es = elasticsearch.Elasticsearch()

    list_buckets_response = s3_client.list_buckets()
    buckets = list_buckets_response['Buckets']
    for bucket in buckets:
        bucket_name = bucket['Name']
        s3_walker.list_all_versions_in_bucket(bucket_name, s3_client, batch_size)

    walker = s3_walker.S3Walker(s3_client, 50)
    for version in walker.get_all_versions():
        print es.index(index="s3",
                       doc_type="object",
                       id=version['bucket']+'/'+version['version']['Key']+'/'+version['version']['VersionId'],
                       body=version)

if __name__=="__main__":
    populate_index()
