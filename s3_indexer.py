import s3_walker
import elasticsearch
import boto3

def populate_index():
    session = boto3.session.Session(profile_name='sandbox')
    client = session.client('s3')

    es = elasticsearch.Elasticsearch()

    walker = s3_walker.S3Walker(client, 50)
    for version in walker.get_all_versions():
        print es.index(index="s3", doc_type="object",
            id=version['bucket']+'/'+version['version']['Key']+'/'+version['version']['VersionId'],
            body=version)

if __name__=="__main__":
    populate_index()
