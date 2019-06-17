# -*- coding: utf-8 -*-
'''
Support for Octoprint
'''

# Import python libs
from __future__ import absolute_import, generators, print_function, with_statement, unicode_literals
import json
import logging

# Import salt libs
import salt.utils.http

log = logging.getLogger(__name__)

__virtualname__ = 'user'


def __virtual__():
    '''
    Only load the module if Octoprint is installed
    '''
    if __opts__['pillar']['proxy']['proxytype'] == 'octoprint':
        return True
    return (False, 'The octoprint modules cannot be loaded: proxy is not configured.')


def list_users():
    '''
    Return Octoprint users

    CLI Example:

    .. code-block:: bash

        salt octominion user.list_users
    '''
    url = '{0}/api/users'.format(__opts__['pillar']['proxy']['url'])
    ret = []
    data = salt.utils.http.query(
        url,
        'GET',
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']['users']
    for user in data:
        if user['user'] is True:
            ret.append(user['name'])
    return ret


def add(name,
        password='',
        active=False,
        admin=False):
    '''
    Add a user to the printer. ``active`` and ``admin`` default to False.

    CLI Example:

    .. code-block:: bash

        salt octominion user.add <name> <password> <active> <admin>
    '''
    url = '{0}/api/users'.format(__opts__['pillar']['proxy']['url'])
    
    data = salt.utils.http.query(
        url,
        'POST',
        data=json.dumps({
            'name': name,
            'password': password,
            'active': active,
            'admin': admin,
        }),
        header_dict={
            'X-Api-Key': __opts__['pillar']['proxy']['apikey'],
            'Content-type': 'application/json',
        },
        status=True,
        opts=__opts__,
    )
    if int(data['status']) != 200:
        return False
    return True


def delete(name):
    '''
    Remove a user from the minion

    CLI Example:

    .. code-block:: bash

        salt octominion user.delete name remove=True force=True
    '''
    url = '{0}/api/users/{1}'.format(__opts__['pillar']['proxy']['url'], name)
    data = salt.utils.http.query(
        url,
        'DELETE',
        header_dict={
            'X-Api-Key': __opts__['pillar']['proxy']['apikey'],
            'Content-type': 'application/json',
        },
        status=True,
        opts=__opts__,
    )
    if int(data['status']) != 200:
        return False
    return True


def getent(refresh=False):
    '''
    Return the list of all info for all users

    CLI Example:

    .. code-block:: bash

        salt octominion user.getent
    '''
    url = '{0}/api/users'.format(__opts__['pillar']['proxy']['url'])
    return salt.utils.http.query(
        url,
        'GET',
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']['users']


def info(name):
    '''
    Return user information

    CLI Example:

    .. code-block:: bash

        salt octominion user.info root
    '''
    try:
        url = '{0}/api/users/{1}'.format(__opts__['pillar']['proxy']['url'], name)
        data = salt.utils.http.query(
            url,
            'GET',
            header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
            opts=__opts__,
            decode=True,
            decode_type='json',
        )['dict']
        if not data:
            return {}
    except KeyError:
        return {}
    else:
        return _format_info(data)


def _format_info(data):
    '''
    Return user information in a pretty way
    '''
    return {
        'name': data['name'],
        'passwd': data.get('password'),
    }
