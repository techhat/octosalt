# -*- coding: utf-8 -*-
'''
Support for OctoPrint
'''

# Import python libs
from __future__ import absolute_import, generators, print_function, with_statement, unicode_literals
import json
import logging

# Import salt libs
import salt.utils.http

log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load the module if proxy configuration is present
    '''
    if __opts__['pillar'].get('proxy', {}).get('proxytype', '') == 'octoprint':
        return True
    return (False, 'The OctoPrint modules cannot be loaded: proxy is not configured.')


def status():
    '''
    Return OctoPrint status

    CLI Example:

    .. code-block:: bash

        salt octominion octoprint.status
    '''
    url = '{0}/api/printer'.format(__opts__['pillar']['proxy']['url'])
    return salt.utils.http.query(
        url,
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']


def version():
    '''
    Return OctoPrint version

    CLI Example:

    .. code-block:: bash

        salt octominion octoprint.status
    '''
    url = '{0}/api/version'.format(__opts__['pillar']['proxy']['url'])
    return salt.utils.http.query(
        url,
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']


def connection():
    '''
    Return OctoPrint connection information

    CLI Example:

    .. code-block:: bash

        salt octominion octoprint.connection
    '''
    url = '{0}/api/connection'.format(__opts__['pillar']['proxy']['url'])
    return salt.utils.http.query(
        url,
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']


def connect(
        port=None,
        baudrate=None,
        printerprofile=None,
        save=False,
        autoconnect=None,
    ):
    '''
    Connect OctoPrint to the printer

    CLI Example:

    .. code-block:: bash

        salt octominion octoprint.connection
    '''
    url = '{0}/api/connection'.format(__opts__['pillar']['proxy']['url'])
    data = {
        'command': 'connect',
        'save': save,
    }

    if port:
        data['port'] = port

    if baudrate:
        data['baudrate'] = baudrate

    if printerprofile:
        data['printerprofile'] = printerprofile

    if autoconnect:
        data['autoconnect'] = autoconnect

    return salt.utils.http.query(
        url,
        'POST',
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        data=json.dumps(data),
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']


def disconnect():
    '''
    Disconnect OctoPrint from printer

    CLI Example:

    .. code-block:: bash

        salt octominion octoprint.disconnect
    '''
    url = '{0}/api/connection'.format(__opts__['pillar']['proxy']['url'])
    data = {'command': 'disconnect'}
    return salt.utils.http.query(
        url,
        'POST',
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        data=json.dumps(data),
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']


def start():
    '''
    Start the loaded print

    CLI Example:

    .. code-block:: bash

        salt octominion octoprint.start
    '''
    url = '{0}/api/job'.format(__opts__['pillar']['proxy']['url'])
    data = salt.utils.http.query(
        url,
        'POST',
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey'],
                     'Content-type': 'application/json'},
        opts=__opts__,
        data=json.dumps({'command': 'start'}),
        decode=True,
        decode_type='json',
    )
    if int(data.get('status', 0)) == 204 or int(data.get('status', 0)) == 200:
        return True
    return False


def stop():
    '''
    Stop the current print

    CLI Example:

    .. code-block:: bash

        salt octominion octoprint.stop
    '''
    url = '{0}/api/job'.format(__opts__['pillar']['proxy']['url'])
    data = salt.utils.http.query(
        url,
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        data={'command': 'stop'},
        decode=True,
        decode_type='json',
    )
    if int(data.get('status', 0)) == 204 or int(data.get('status', 0)) == 200:
        return True
    return False


def restart():
    '''
    Restart the current, paused print, from the beginning

    CLI Example:

    .. code-block:: bash

        salt octominion octoprint.stop
    '''
    url = '{0}/api/job'.format(__opts__['pillar']['proxy']['url'])
    data = salt.utils.http.query(
        url,
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        data={'command': 'stop'},
        decode=True,
        decode_type='json',
    )
    if int(data.get('status', 0)) == 204 or int(data.get('status', 0)) == 200:
        return True
    return False


def pause():
    '''
    Pause the current print

    CLI Example:

    .. code-block:: bash

        salt octominion octoprint.pause
    '''
    url = '{0}/api/job'.format(__opts__['pillar']['proxy']['url'])
    data = salt.utils.http.query(
        url,
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        data={'command': 'pause', 'action': 'pause'},
        decode=True,
        decode_type='json',
    )
    if int(data.get('status', 0)) == 204 or int(data.get('status', 0)) == 200:
        return True
    return False


def resume():
    '''
    Resume the paused print

    CLI Example:

    .. code-block:: bash

        salt octominion octoprint.resume
    '''
    url = '{0}/api/job'.format(__opts__['pillar']['proxy']['url'])
    data = salt.utils.http.query(
        url,
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        data={'command': 'pause', 'action': 'resume'},
        decode=True,
        decode_type='json',
    )
    if int(data.get('status', 0)) == 204 or int(data.get('status', 0)) == 200:
        return True
    return False


def job_status():
    '''
    Return OctoPrint job status

    CLI Example:

    .. code-block:: bash

        salt octominion octoprint.status
    '''
    url = '{0}/api/job'.format(__opts__['pillar']['proxy']['url'])
    return salt.utils.http.query(
        url,
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']
