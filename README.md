# search_buckets_for_keys
* Use elasticsearch to index all version of all keys in all buckets in an AWS account.
* Query elasticsearch for keys of interest.

# Setup
* Elasticsearch docker instance

        mkdir -p esdata
        docker run --name elasticsearch -p 9200:9200 -p 9300:9300 -d -v "$PWD/esdata":/usr/share/elasticsearch/data elasticsearch

* Use s3_walker to walk all versions and write to elasticsearch.

        import s3_walker
        import elasticsearch
        import boto3

        session = boto3.session.Session(profile='sandbox')
        client = session.client('s3')

        es = elasticsearch.Elasticsearch()

        walker = s3_walker.S3Walker(client, 50)
        for version in walker.get_all_versions():
            es.create(index="s3", doc_type="object", id=version['bucket']+'/'+version['version']['Key']+'/'+version['version']['VersionId'], body=version)

# Optimization NOTES
* Use the bulk Api. The initial version used individual index calls. Bulk calls will increase speed. Given that the S3 API can return upto 1000 keys in one call, it may work better to use the bulk API to index all of them at once.
