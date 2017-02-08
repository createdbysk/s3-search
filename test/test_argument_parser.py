from nose.tools import assert_equal
import argument_parser
import re

class TestArgumentParser(object):
    def __init__(self):
        pass

    def setup(self):
        pass

    def test_argument_parser(self):
        # GIVEN
        application_name = 's3_scrubber'
        expected_help_text = """usage: s3_scrubber [-h] <command> [options]

Delete specified files from s3 with a dry-run option.

positional arguments:
  index              index the s3 keys in elastic search

optional arguments:
  -h, --help         show this help message and exit
  --profile PROFILE  the aws profile to use to run the command
"""

        # WHEN
        parser = argument_parser.create_parser(application_name)
        actual_help_text = parser.format_help()

        # THEN
        # Remove all whitespaces to prevent brittleness in the test from a change in the format.
        assert_equal(re.sub('\s', '', expected_help_text), re.sub('\s', '', actual_help_text))