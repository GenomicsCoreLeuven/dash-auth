import copy
import os
import plotly
import requests

# API requests get their config from the environment.
# If variables aren't there, then they check the plotly.tools.get_credentials_file

def credential(key):
    if key in os.environ:
        return os.environ[key]
    elif key.upper() in os.environ:
        return os.environ[key.upper()]
    else:
        return plotly.tools.get_credentials_file()[key.replace('plotly_', '')]

def config(key):
    if key in os.environ:
        return os.environ[key]
    elif key.upper() in os.environ:
        return os.environ[key.upper()]
    else:
        return plotly.tools.get_config_file()[key]


HEADERS = {
    'plotly-client-platform': 'dash-auth',
    'content-type': 'application/json'
}

def _modify_request_kwargs(request_kwargs):
    copied_kwargs = copy.deepcopy(request_kwargs)
    if 'headers' in request_kwargs:
        copied_kwargs['headers'].update(HEADERS)
    else:
        copied_kwargs['headers'] = HEADERS

    if 'Authorization' not in copied_kwargs['headers']:
        copied_kwargs['auth'] = (
            credential('plotly_username'),
            credential('plotly_api_key'),)
        print(copied_kwargs['auth'])

    copied_kwargs['verify'] = config('plotly_ssl_verification')
    return copied_kwargs


def _create_method(method_name):
    def request(path, api_key_auth=True, **request_kwargs):
        copied_kwargs = _modify_request_kwargs(request_kwargs)
        return getattr(requests, method_name)(
            '{}{}'.format(config('plotly_api_domain'), path),
            **copied_kwargs
        )
    return request

post = _create_method('post')
patch = _create_method('patch')
get = _create_method('get')
