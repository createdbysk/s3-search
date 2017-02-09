def list_all_versions_in_bucket(bucket_name, s3_client, batch_size):
    """
    GIVEN an s3 bucket name
    WHEN list_all_versions_in_bucket runs
    THEN it returns a generator that lists all versions of all objects in the bucket
    AND the generator returns at most batch_size number of versions per iteration.
    """

    list_object_versions_response = s3_client.list_object_versions(Bucket=bucket_name, MaxKeys=batch_size)
    if list_object_versions_response.has_key('Versions'):
        yield list_object_versions_response['Versions']

    while list_object_versions_response['IsTruncated']:
        list_object_versions_response = s3_client.list_object_versions(
                Bucket=bucket_name,
                MaxKeys=batch_size,
                KeyMarker=list_object_versions_response['NextKeyMarker'],
                VersionIdMarker=list_object_versions_response['NextVersionIdMarker'])
        if list_object_versions_response.has_key('Versions'):
            yield list_object_versions_response['Versions']
