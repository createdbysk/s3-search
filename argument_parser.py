import argparse


def create_parser(application_name):
    parser = argparse.ArgumentParser(prog=application_name,
                                     usage="%(prog)s [-h] <command> [options]",
                                     description="Delete specified files from s3 with a dry-run option.")
    parser.add_argument('index', action='store_true', help='index the s3 keys in elastic search')
    parser.add_argument('--profile', action='store', required=True, help='the aws profile to use to run the command')
    return parser
