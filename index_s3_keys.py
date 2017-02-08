

def add_versions_to_index(elasticsearch_client, versions, chunk_size, expand_action_callback, response_handler):
    """
    Add the versions to the Elasticsearch index
    Args:
        elasticsearch_client:
        versions:
        chunk_size:
        expand_action_callback:
        response_handler:

    Returns:
        None
    """
    # Import here so tests can patch this import.
    import elasticsearch.helpers
    responses = elasticsearch.helpers.streaming_bulk(elasticsearch_client,
                                                     versions,
                                                     chunk_size=chunk_size,
                                                     expand_action_callback=expand_action_callback,
                                                     raise_on_error=False,
                                                     raise_on_exception=False)

    for response in responses:
        response_handler(response)
