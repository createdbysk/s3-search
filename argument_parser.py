import argparse


def create_parser(application_name):
    parser = argparse.ArgumentParser(prog=application_name,
                                     usage="%(prog)s [-h] <command> [options]",
                                     description="Delete specified files from s3 with a dry-run option.")
    parser.add_argument('command', action='store', help='index - index the s3 keys in elastic search')
    parser.add_argument('profile', action='store', help='the aws profile to use to run the command')
    return parser
