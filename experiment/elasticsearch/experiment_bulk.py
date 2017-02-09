import elasticsearch
import elasticsearch.helpers

def experiment_bulk(client):
    bulk_commands = [{
        '_op_type': 'create',
        '_index': 'satish_test',
        '_type': 'test_document',
        '_id': 'test1',
        'doc': {'question': 'The life, universe, and everything'}
    },
    {
        '_op_type': 'create',
        '_index': 'satish_test',
        '_type': 'test_document_2',
        '_id': 'test2',
        'doc': {'answer': '42'}
    }]

    response = elasticsearch.helpers.bulk(client, bulk_commands, raise_on_exception=False, raise_on_error=False)
    print response


def experiment_streaming_bulk(client):
    bucket_name = 'test_bucket'
    versions = [
        {
            '_index': 's31', '_type': 'object', '_id': '1', '_op_type': 'create',
            '_source': {
                'version': {
                    'VersionId': 'null',
                    'Key': 'test_document1'
                },
                'bucket_name': bucket_name
            }
        },
        {
            '_index': 's31', '_type': 'object', '_id': '2', '_op_type': 'create',
            '_source': {
                'version': {
                    'VersionId': 'null',
                    'Key': 'test_document2'
                },
                'bucket_name': bucket_name
            }
        },
    ]

    versions_only = [
        {
            'VersionId': 'null',
            'Key': 'test_document1'
        },
        {
            'VersionId': 'null',
            'Key': 'test_document2'
        }
    ]

    def expand_action_callback(version):
        id = '{bucket_name}/{key}/{version_id}'.format(
            bucket_name=bucket_name,
            key=version['Key'],
            version_id=version['VersionId']
        )
        action = {'_create': {'_index': 's3', '_type': 'object', '_id': id}}
        data = {'version': version, 'bucket_name': bucket_name}
        return action, data

    responses = elasticsearch.helpers.streaming_bulk(client,
                                                     versions_only,
                                                     expand_action_callback=expand_action_callback,
                                                     raise_on_exception=False,
                                                     raise_on_error=False)
    for response in responses:
        print response


if __name__ == '__main__':
    elasticsearch_client = elasticsearch.Elasticsearch()
    experiment_streaming_bulk(elasticsearch_client)