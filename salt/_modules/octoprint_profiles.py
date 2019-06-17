# -*- coding: utf-8 -*-
'''
Module for OctoPrint Printer Profiles
'''

# Import python libs
from __future__ import absolute_import, generators, print_function, with_statement, unicode_literals
import json
import logging

# Import salt libs
import salt.utils.http

log = logging.getLogger(__name__)

__virtualname__ = 'octo_printer'
__func_alias__ = {
    'list_': 'list'
}


def __virtual__():
    '''
    Only load the module if proxy configuration is present
    '''
    if __opts__['pillar'].get('proxy', {}).get('proxytype', '') == 'octoprint':
        return True
    return (False, 'The OctoPrint modules cannot be loaded: proxy is not configured.')


def list_():
    '''
    List OctoPrint printer profiles

    CLI Example:

    .. code-block:: bash

        salt octominion octo_printer.list
    '''
    url = '{0}/api/printerprofiles'.format(__opts__['pillar']['proxy']['url'])
    return salt.utils.http.query(
        url,
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']


def add_profile(data):
    '''
    Add a new printer profile.

    CLI Example:

    .. code-block:: bash

        salt octominion octo_printer.add_profile \
            '{"profile": {"id": "myprinter", "name": "my printer" \
            "model": "my cool printer"}}'
    '''
    url = '{0}/api/printerprofiles'.format(__opts__['pillar']['proxy']['url'])
    return salt.utils.http.query(
        url,
        'POST',
        header_dict={
            'X-Api-Key': __opts__['pillar']['proxy']['apikey'],
            'Content-type': 'application/json',
        },
        data=json.dumps(data),
        opts=__opts__,
        decode=True,
        decode_type='json',
    )


def update_profile(profile, data):
    '''
    Update an existing printer profile.

    CLI Example:

    .. code-block:: bash

        salt octominion octo_printer.update_profile myprinter \
            '{"profile": {"name": "my other printer"}}'
    '''
    url = '{0}/api/printerprofiles/{1}'.format(
        __opts__['pillar']['proxy']['url'],
        profile,
    )
    return salt.utils.http.query(
        url,
        'PATCH',
        header_dict={
            'X-Api-Key': __opts__['pillar']['proxy']['apikey'],
            'Content-type': 'application/json',
        },
        data=json.dumps(data),
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']


def delete_profile(profile):
    '''
    Delete a printer profile.

    CLI Example:

    .. code-block:: bash

        salt octominion octo_printer.delete_profile myprinter
    '''
    url = '{0}/api/printerprofiles/{1}'.format(
        __opts__['pillar']['proxy']['url'],
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
