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
    bulk_commands = [{
        '_op_type': 'create',
        '_index': 'satish_test',
        '_type': 'test_document',
        '_id': 'test_streaming_1',
        'question': 'The life, universe, and everything'
    }, {
        '_op_type': 'create',
        '_index': 'satish_test',
        '_type': 'test_document_2',
        '_id': 'test_streaming_2',
        'answer': '42',
        'another_answer': 'is'
    }]

    responses = elasticsearch.helpers.streaming_bulk(client,
                                                     bulk_commands,
                                                     raise_on_exception=False,
                                                     raise_on_error=False)
    for response in responses:
        print response


if __name__ == '__main__':
    elasticsearch_client = elasticsearch.Elasticsearch()
    experiment_streaming_bulk(elasticsearch_client)