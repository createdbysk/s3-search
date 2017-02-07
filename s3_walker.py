def list_all_versions_in_bucket(bucket_name, s3_client, batch_size):
    list_object_versions_response = s3_client.list_object_versions(Bucket=bucket_name, MaxKeys=batch_size)
    if list_object_versions_response.has_key('Versions'):
        yield {'bucket': bucket_name, 'version': list_object_versions_response['Versions']}

    while list_object_versions_response['IsTruncated']:
        list_object_versions_response = s3_client.list_object_versions(
                Bucket=bucket_name,
                MaxKeys=batch_size,
                KeyMarker=list_object_versions_response['NextKeyMarker'],
                VersionIdMarker=list_object_versions_response['NextVersionIdMarker'])
        if list_object_versions_response.has_key('Versions'):
            yield {'bucket': bucket_name, 'version': list_object_versions_response['Versions']}


class S3Walker(object):
    def __init__(self, s3client, batch_size):
        """
        s3_client -- An instance of the s3 client object
        batch_size -- The number of keys to fetch per request.
        """
        self.__s3_client = s3client
        self.__batch_size = batch_size

    def get_all_versions(self):
        list_buckets_response = self.__s3_client.list_buckets()
        buckets = list_buckets_response['Buckets']
        for bucket in buckets:
            bucket_name = bucket['Name']
            get_all_versions_in_bucket(bucket_name)

    def get_all_versions_in_bucket(self, bucket_name):
        list_object_versions_response = self.__s3_client.list_object_versions(Bucket=bucket_name, MaxKeys=self.__batch_size)
        if list_object_versions_response.has_key('Versions'):
            for version in list_object_versions_response['Versions']:
                yield {'bucket':bucket_name, 'version':version}
        while list_object_versions_response['IsTruncated']:
            list_object_versions_response = self.__s3_client.list_object_versions(
                Bucket=bucket_name,
                MaxKeys=self.__batch_size,
                KeyMarker=list_object_versions_response['NextKeyMarker'],
                VersionIdMarker=list_object_versions_response['NextVersionIdMarker'])
            if list_object_versions_response.has_key('Versions'):
                for version in list_object_versions_response['Versions']:
                    yield {'bucket':bucket_name, 'version':version}
