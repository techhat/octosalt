# -*- coding: utf-8 -*-
'''
This is a simple proxy-minion designed to connect to and communicate with
the OctoPrint 3D printing server.
'''
from __future__ import absolute_import, print_function, unicode_literals

# Import python libs
import logging
import salt.utils.http

HAS_REST_EXAMPLE = True

# This must be present or the Salt loader won't load this module
__proxyenabled__ = ['octoprint']


# Variables are scoped to this module so we can have persistent data
# across calls in here.
GRAINS_CACHE = {}
DETAILS = {}

log = logging.getLogger(__file__)


def __virtual__():
    '''
    Only return if OctoPrint is configured
    '''
    if __opts__['pillar']['proxy']['proxytype'] == 'octoprint':
        return True
    return (False, 'The octoprint modules cannot be loaded: proxy is not configured.')


def init(opts):
    DETAILS['initialized'] = True


def initialized():
    '''
    Since grains are loaded in many different places and some of those
    places occur before the proxy can be initialized, return whether
    our init() function has been called
    '''
    return DETAILS.get('initialized', False)


def alive(opts):
    return False
    try:
        salt.utils.http.query('{0}/api/version'.format(URL), opts=__opts__)['body']
    except KeyError:
        return False
    return True


def grains():
    '''
    Get the grains from the proxied device
    '''
    if not DETAILS.get('grains_cache', {}):
        DETAILS['grains_cache'] = {
            'host': __opts__['pillar']['proxy']['url'].split('://')[1].split('/')[0],
            'kernel': 'OctoPrint',
            'os': 'OctoPrint',
            'os_family': 'OctoPrint',
            'osfullname': 'OctoPrint',
        }
        try:
            version = salt.utils.http.query(
                '{0}/api/version'.format(__opts__['pillar']['proxy']['url']),
                opts=__opts__,
                decode=True,
                decode_type='json',
            )['dict']
            DETAILS['grains_cache'].update({
                'kernelrelease': version['server'],
                'kernelversion': version['server'],
                'osfinger': version['text'].replace(' ', '_'),
                'osmajorrelease': version['server'].split('.')[0],
                'osrelease': version['server'],
                'osrelease_info': version['server'].split('.'),
            })
        except KeyError:
            pass
    return DETAILS['grains_cache']


def grains_refresh():
    '''
    Refresh the grains from the proxied device
    '''
    DETAILS['grains_cache'] = None
    return grains()


def ping():
    '''
    Is the server up?
    '''
    try:
        salt.utils.http.query(
            '{0}/api/version'.format(__opts__['pillar']['proxy']['url']),
            opts=__opts__,
        )['body']
    except KeyError:
        return False
    return True


def shutdown(opts):
    '''
    For this proxy shutdown is a no-op
    '''
    pass
