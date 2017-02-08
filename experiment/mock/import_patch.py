from nose.tools import assert_equal

import mock

my_boto3 = mock.Mock()
my_session = mock.Mock()
my_session.test.return_value = 42
my_boto3.session = my_session
module_patcher = mock.patch.dict('sys.modules', {'boto3': my_boto3, 'boto3.session': my_boto3.session})

def my_test():
    import boto3.session
    return boto3.session.test()

with module_patcher:
    assert_equal(42, my_test())
