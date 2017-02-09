import sys
import argument_parser
import boto3.session
import s3_walker
import s3_bucket_name_filter
import s3_version_indexer
import elasticsearch
import logger

def index(s3_client, batch_size):
    elasticsearch_client = elasticsearch.Elasticsearch()

    buckets = s3_client.list_buckets()['Buckets']
    bucket_names = [bucket['Name'] for bucket in buckets]
    bucket_names_without_logs = s3_bucket_name_filter.filter_log_buckets(bucket_names)
    log = logger.create_logger(log_level='INFO')

    for bucket_name in bucket_names_without_logs:
        all_versions = s3_walker.list_all_versions_in_bucket(bucket_name, s3_client, batch_size)

        def expand_action_callback(version):
            id = '{bucket_name}/{key}/{version_id}'.format(
                bucket_name=bucket_name,
                key=version['Key'],
                version_id=version['VersionId']
            )
            action = {'_create': {'_index': 's3_2', '_type': 'object', '_id': id}}
            data = {'version': '5', 'bucket_name': bucket_name}
            return action, data

        def response_handler(response):
            print response

        for versions in all_versions:
            s3_version_indexer.add_versions_to_index(elasticsearch_client, versions, 1000, expand_action_callback,
                                                     response_handler)


def main(arguments):
    parser = argument_parser.create_parser(arguments[0])
    namespace = parser.parse_args()

    profile = namespace.profile
    boto_session = boto3.session.Session(profile_name=profile)
    s3_client = boto_session.client('s3')

    if namespace.command == 'index':
        index(s3_client, 1000)

if __name__ == "__main__":
    main(sys.argv)