from nose.tools import assert_equal

import s3_bucket_name_filter

class TestS3BucketNameFilter(object):
    def __init__(self):
        pass

    def setup(self):
        pass

    @staticmethod
    def test_filter_log_buckets_given_no_log_buckets_does_not_filter():
        # GIVEN
        bucket_names = ['do_not_filter_this_bucket_name']
        expected_filtered_bucket_names = bucket_names

        # WHEN
        actual_filtered_bucket_names = s3_bucket_name_filter.filter_log_buckets(bucket_names)

        # THEN
        assert_equal(expected_filtered_bucket_names, actual_filtered_bucket_names)

    @staticmethod
    def test_filter_log_buckets_given_log_buckets_in_list_returns_buckets_without_log_buckets():
        # GIVEN
        bucket_names = ['do_not_filter_this_bucket_name', 'filter_this_log_bucket']
        expected_filtered_bucket_names = ['do_not_filter_this_bucket_name']

        # WHEN
        actual_filtered_bucket_names = s3_bucket_name_filter.filter_log_buckets(bucket_names)

        # THEN
        assert_equal(expected_filtered_bucket_names, actual_filtered_bucket_names)
