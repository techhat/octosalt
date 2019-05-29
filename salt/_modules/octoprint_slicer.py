# -*- coding: utf-8 -*-
'''
Module for OctoPrint Slicers
'''

# Import python libs
from __future__ import absolute_import, generators, print_function, with_statement, unicode_literals
import json
import logging

# Import salt libs
import salt.utils.http

log = logging.getLogger(__name__)

__virtualname__ = 'slicer'
__func_alias__ = {
    'list_': 'list'
}


def __virtual__():
    '''
    Only load the module if OctoPrint is installed
    '''
    if __opts__['pillar']['proxy']['proxytype'] == 'octoprint':
        return True
    return (False, 'The OctoPrint modules cannot be loaded: proxy is not configured.')


def list_():
    '''
    List OctoPrint slicers and slicing profiles

    CLI Example:

    .. code-block:: bash

        salt octominion slicer.list
    '''
    url = '{0}/api/slicing'.format(__opts__['pillar']['proxy']['url'])
    return salt.utils.http.query(
        url,
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']


def get_profile(slicer, profile):
    '''
    Show a specific slicing profile

    CLI Example:

    .. code-block:: bash

        salt octominion slicer.get_profile curalegacy spiralize
    '''
    url = '{0}/api/slicing/{1}/profiles/{2}'.format(
        __opts__['pillar']['proxy']['url'],
        slicer,
        profile,
    )
    data = salt.utils.http.query(
        url,
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        decode=True,
        decode_type='json',
        status=True,
    )
    if int(data['status']) == 404:
        return 'Either the slicer or the profile was not found'
    return data['dict']


def save_profile(slicer, profile, data):
    '''
    Save a slicing profile. If the profile already exists, it will be
    overwritten. Data is expected using OctoPrint slicing profile format.

    CLI Example:

    .. code-block:: bash

        salt octominion slicer.save_profile curalegacy example \
            '{"displayName": "example", "data": {"layer_height": 0.2}}'
    '''
    url = '{0}/api/slicing/{1}/profiles/{2}'.format(
        __opts__['pillar']['proxy']['url'],
        slicer,
        profile,
    )
    return salt.utils.http.query(
        url,
        'PUT',
        header_dict={
            'X-Api-Key': __opts__['pillar']['proxy']['apikey'],
            'Content-type': 'application/json',
        },
        data=json.dumps(data),
        opts=__opts__,
        decode=True,
        decode_type='json',
    )


def delete_profile(slicer, profile):
    '''
    Delete a slicing profile.

    CLI Example:

    .. code-block:: bash

        salt octominion slicer.delete_profile curalegacy spiralize
    '''
    url = '{0}/api/slicing/{1}/profiles/{2}'.format(
        __opts__['pillar']['proxy']['url'],
        slicer,
        profile,
    )
    data = salt.utils.http.query(
        url,
        'DELETE',
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        status=True,
    )
    if int(data['status']) == 204:
        return True
    return False
