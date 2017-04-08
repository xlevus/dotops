import os
import pytest

from devtops.context import Context


@pytest.fixture
def context():
    return Context(prefix='TEST_')


def test_set(context):
    context.test = 'test'

    assert context.context['test'] == 'test'
    assert os.environ['TEST_TEST'] == 'test'


def test_get_not_set(context):
    with pytest.raises(AttributeError):
        foo = context.does_not_exist


def test_set_in_env(context):
    os.environ['TEST_SET_IN_ENV'] = 'true'

    assert context.set_in_env == 'true'


@pytest.mark.parametrize('local,env,expected', [
    (None, None, 'default'),
    ('local', None, 'local'),
    (None, 'env', 'env'),
])
def test_get(context, local, env, expected):
    if local:
        context.context['value'] = local

    if env:
        context.set_environ('value', env)

    assert context.get('value', default='default') == expected
