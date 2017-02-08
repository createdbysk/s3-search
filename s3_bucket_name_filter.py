def filter_log_buckets(bucket_names):
    """
    GIVEN a list of bucket names
    WHEN filter_log_buckets runs
    THEN filter_log_buckets returns a list with the names of buckets with substring 'log' in it

    Args:
        bucket_names: the list of bucket names to filter log bucket names from

    Returns: the list of bucket names without the sub-string log in them.
    """

    log_substring = 'log'
    filtered_bucket_names = [bucket_name for bucket_name in bucket_names if log_substring not in bucket_name]

    return filtered_bucket_names
