# -*- coding: utf-8 -*-
'''
Support for Octoprint
'''

# Import python libs
from __future__ import absolute_import, generators, print_function, with_statement, unicode_literals
import json
import logging

# Import 3rd party libs
import requests

# Import salt libs
import salt.utils.http

log = logging.getLogger(__name__)

__virtualname__ = 'octo_file'


def __virtual__():
    '''
    Only load the module if Octoprint is configured
    '''
    if __opts__['pillar']['proxy']['proxytype'] == 'octoprint':
        return True
    return (False, 'The octoprint modules cannot be loaded: proxy is not configured.')


def remove(path):
    '''
    Delete a file. The path must include one of the following as the location:

        * ``local``: Uses OctoPrint's ``uploads`` folder
        * ``sdcard``: Uses the printer's SD card

    CLI Examples:

    .. code-block:: bash

        salt octominion file.remove <location/path>
        salt octominion file.remove local/vase.gcode
    '''
    url = '{0}/api/files/{1}'.format(__opts__['pillar']['proxy']['url'], path)

    return salt.utils.http.query(
        url,
        'DELETE',
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']


def readdir(path):
    '''
    Return a list containing the contents of a directory. The path must include
    one of the following as the location:

        * ``local``: Uses OctoPrint's ``uploads`` folder
        * ``sdcard``: Uses the printer's SD card

    CLI Example:

    .. code-block:: bash

        salt octominion file.readdir <location[/path]>
        salt octominion file.readdir local
        salt octominion file.readdir local/vases
    '''
    url = '{0}/api/files/{1}'.format(__opts__['pillar']['proxy']['url'], path)

    data = salt.utils.http.query(
        url,
        header_dict={'X-Api-Key': __opts__['pillar']['proxy']['apikey']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']

    return _format_dir(data, path)


def _format_dir(data, path):
    '''
    Reformat the files from OctoPrint's JSON structure into something more
    akin to a server's directory structure
    '''
    ipath = '/'.join(path.split('/')[1:])

    ret = []
    if 'files' in data:
        for item in data['files']:
            if item['type'] == 'folder':
                ret.append(item['name'] + '/')
            else:
                ret.append(item['name'])
    elif 'children' in data:
        for item in data['children']:
            if item['type'] == 'folder':
                ret.append(item['name'] + '/')
            else:
                ret.append(item['name'])
    return sorted(ret)


def upload(localfile, remotepath):
    '''
    Uploads a file. The path remote must include one of the following as the
    location:

        * ``local``: Uses OctoPrint's ``uploads`` folder
        * ``sdcard``: Uses the printer's SD card

    CLI Examples:

    .. code-block:: bash

        salt octominion file.upload <remotepath> <location/remotepath>
        salt octominion file.upload /path/to/local/file.gco local/file.gco
    '''
    location = remotepath.split('/')[0]
    url = '{0}/api/files/{1}'.format(__opts__['pillar']['proxy']['url'], location)
    filename = localfile.split('/')[-1]
    if localfile.endswith('.stl'):
        mimetype = 'model/stl'
    mimetype = 'text/plain'

    ret = requests.post(
        url,
        headers={'X-Api-Key': __opts__['pillar']['proxy']['apikey'],},
        files=[
            ('file', (filename, open(localfile, 'rb'), mimetype)),
        ],
    ).text
    return json.loads(ret)
