import mock
import index_s3_keys

class TestIndexS3Keys(object):
    def __init__(self):
        self.__elasticsearch_client = None
        self.__elasticsearch_helpers = None
        self.__response_handler = None

    def setup(self):
        self.__elasticsearch_client = mock.Mock()
        self.__elasticsearch_helpers = mock.Mock()
        self.__response_handler = mock.Mock()

    def test_add_versions_to_index(self):
        # GIVEN
        first_version = '1'
        second_version = '2'
        versions = [first_version, second_version]
        chunk_size = 100

        def return_value_generator():
            yield {'response': first_version}
            yield {'response': second_version}

        self.__elasticsearch_helpers.streaming_bulk.return_value = return_value_generator()

        # WHEN
        index_s3_keys.add_versions_to_index(self.__elasticsearch_client,
                                            versions,
                                            chunk_size,
                                            self.__response_handler)

        # THEN
        self.__elasticsearch_helpers.streaming_bulk.assert_called_once_with(self.__elasticsearch_client,
                                                                            versions,
                                                                            chunk_size=chunk_size,
                                                                            raise_on_error=False,
                                                                            raise_on_exception=False)

        calls = [mock.call(response) for response in return_value_generator()]
        self.__response_handler.assert_has_calls(calls, any_order=False)
