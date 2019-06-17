# -*- coding: utf-8 -*-
'''
Beacon for OctoPrint
'''

# Import python libs
from __future__ import absolute_import, generators, print_function, with_statement, unicode_literals
import json
import logging

# Import salt libs
import salt.utils.http

__virtualname__ = 'octoprint_job'

log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load the module if proxy configuration is present
    '''
    if __opts__['pillar'].get('proxy', {}).get('proxytype', '') == 'octoprint':
        return True
    return (False, 'The OctoPrint modules cannot be loaded: proxy is not configured.')


def validate(config):
    '''
    Validate configuration
    '''
    return True, 'Valid beacon configuration'


def beacon(config):
    '''
    Return printer status
    '''
    url = '{0}/api/job'.format(__opts__['pillar']['proxy']['url'])
    data = salt.utils.http.query(
        url,
        'GET',
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']
    return [data]
