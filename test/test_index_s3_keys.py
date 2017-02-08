import index_s3_keys
import mock


class TestIndexS3Keys(object):
    def __init__(self):
        self.__elasticsearch_client = None
        self.__elasticsearch = None
        self.__elasticsearch_helpers = None
        self.__expand_action_callback = None
        self.__response_handler = None
        self.__module_patcher = None

    def setup(self):
        self.__elasticsearch_client = mock.Mock()
        self.__response_handler = mock.Mock()
        self.__expand_action_callback = mock.Mock()

        # Inject self.__elasticsearch_helpers as an import of elasticsearch.helpers
        self.__elasticsearch = mock.Mock()
        self.__elasticsearch_helpers = mock.Mock()
        self.__elasticsearch.helpers = self.__elasticsearch_helpers
        patched_modules = {
            'elasticsearch': self.__elasticsearch,
            'elasticsearch.helpers': self.__elasticsearch_helpers
        }

        # NOTE: static analysis may indicate that dict is not available in the following line of code.
        #       It is and this is NOT an issue.
        self.__module_patcher = mock.patch.dict('sys.modules', patched_modules)

        # This will start the patch. The teardown() function will stop the patch.
        self.__module_patcher.start()

    def teardown(self):
        # This stops the patch of the imports that started in the setup.
        self.__module_patcher.stop()

    def test_add_versions_to_index(self):
        # GIVEN
        first_version = '1'
        second_version = '2'
        versions = [first_version, second_version]
        chunk_size = 100

        def return_value_generator(*args, **kwargs):
            yield {'response': first_version}
            yield {'response': second_version}

        self.__elasticsearch_helpers.streaming_bulk.side_effect = return_value_generator

        # WHEN
        index_s3_keys.add_versions_to_index(self.__elasticsearch_client,
                                            versions,
                                            chunk_size,
                                            self.__expand_action_callback,
                                            self.__response_handler)

        # THEN
        self.__elasticsearch_helpers\
            .streaming_bulk.assert_called_once_with(self.__elasticsearch_client,
                                                    versions,
                                                    expand_action_callback = self.__expand_action_callback,
                                                    chunk_size=chunk_size,
                                                    raise_on_error=False,
                                                    raise_on_exception=False)

        calls = [mock.call(response) for response in return_value_generator()]
        self.__response_handler.assert_has_calls(calls, any_order=False)
