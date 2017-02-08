def create_logger(log_level = 'INFO', file_handler = False, log_path = '.', log_name = 'log.txt'):
    import logging
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                        datefmt='%Y-%m-%d,%H:%M:%S')
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    if file_handler:
        handler = logging.FileHandler('{path}/{name}'.format(path=log_path, name=log_name))
    else:
        handler = logging.StreamHandler()
    root_logger.addHandler(handler)
    return root_logger
