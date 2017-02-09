import mock
import s3_walker
from nose.tools import assert_equal

class TestS3Walker(object):
    def __init__(self):
        self.__client = None

    def setup(self):
        self.__client = mock.MagicMock()

    def test_list_all_versions_in_bucket_when_no_versions_returns_empty(self):
        # Given
        bucket_name = 'empty'
        batch_size = 2

        # noinspection PyUnusedLocal
        def side_effect(**kwargs):
            if 'Bucket' in kwargs and kwargs['Bucket'] == bucket_name:
                return {'IsTruncated': False}
            else:
                raise NotImplementedError

        self.__client.list_object_versions.side_effect = side_effect
        expected_versions = []

        # When
        actual_versions = list(s3_walker.list_all_versions_in_bucket(bucket_name, self.__client, batch_size))

        # Then
        assert_equal(expected_versions, actual_versions)
        self.__client.list_object_versions.assert_called_once_with(Bucket=bucket_name,
                                                                   MaxKeys=2)

    def test_list_all_versions_in_bucket_when_one_version_returns_one_version(self):
        # Given
        bucket_name = 'one-object'
        batch_size = 2

        # noinspection PyUnusedLocal
        def side_effect(**kwargs):
            if 'Bucket' in kwargs and kwargs['Bucket'] == bucket_name:
                return {'Versions': '1', 'IsTruncated': False}
            else:
                raise NotImplementedError

        self.__client.list_object_versions.side_effect = side_effect
        expected_versions = ['1']

        # When
        actual_versions = list(s3_walker.list_all_versions_in_bucket(bucket_name, self.__client, batch_size))

        # Then
        assert_equal(expected_versions, actual_versions)
        self.__client.list_object_versions.assert_called_once_with(Bucket=bucket_name,
                                                                   MaxKeys=2)

    def test_list_all_versions_in_bucket_when_three_version_returns_one_batch_of_2_and_one_batch_of_1(self):
        # Given
        bucket_name = 'three-objects'
        batch_size = 2
        next_key_marker = 'key_marker'
        next_version_id_marker = 'version_id_marker'

        # noinspection PyUnusedLocal
        def side_effect(**kwargs):
            if 'Bucket' in kwargs and kwargs['Bucket'] == bucket_name:
                # For the first call without a KeyMarker or VersionIdMarker, return the
                # NextKeyMarker and NextVersionIdMarker.
                if not kwargs.has_key('KeyMarker') or not kwargs.has_key('VersionIdMarker'):
                    return {
                        'Versions': ['1', '2'],
                        'IsTruncated': True,
                        'NextKeyMarker': next_key_marker,
                        'NextVersionIdMarker': next_version_id_marker
                    }
                elif kwargs['KeyMarker'] == next_key_marker and kwargs['VersionIdMarker'] == next_version_id_marker:
                    return {
                        'Versions': ['3'],
                        'IsTruncated': False
                    }
            else:
                raise NotImplementedError

        self.__client.list_object_versions.side_effect = side_effect
        expected_versions = [
            ['1', '2'],
            ['3']
        ]

        # When
        actual_versions = list(s3_walker.list_all_versions_in_bucket(bucket_name, self.__client, batch_size))

        # Then
        assert_equal(expected_versions, actual_versions)
        calls = [
            mock.call(Bucket=bucket_name, MaxKeys=2),
            mock.call(Bucket=bucket_name, MaxKeys=2, KeyMarker=next_key_marker, VersionIdMarker=next_version_id_marker)
        ]
        self.__client.list_object_versions.assert_has_calls(calls, any_order=False)
