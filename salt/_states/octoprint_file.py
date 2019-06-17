# -*- coding: utf-8 -*-
'''
Manage OctoPrint printer profiles
=================================

This state is useful for firing messages during state runs, using the SMTP
protocol

.. code-block:: yaml

    _default:
      octo_printer.profile:
        - profile:
            id: _default
            model: My Printer
            name: Default
'''
# Import Python libs
from __future__ import absolute_import, unicode_literals, print_function
import hashlib
import logging

log = logging.getLogger(__name__)
__virtualname__ = 'octo_file'


def __virtual__():
    '''
    Only load if the SMTP module is available in __salt__
    '''
    if __opts__['pillar']['proxy']['proxytype'] == 'octoprint':
        return True
    return (False, 'The OctoPrint modules cannot be loaded: proxy is not configured.')


def present(name, path):
    '''
    Ensure that a file is on the printer

    .. code-block:: yaml

    local/remote_file:
      octo_file.present:
        - path: /path/to/local_file

    name
        The name of the printer profile

    path
        The path on the hosting minion to a file to upload to the printer
    '''
    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    location = name.split('/')[0]
    file_name = '/'.join(name.split('/')[1:])
    files = __salt__['octo_file.list']()['files']
    file_data = {}
    for item in files:
        if item['name'] == file_name:
            file_data = item
            break

    local_sha1 = None

    if not file_data:
        if __opts__['test'] is True:
            ret['result'] = False
            ret['comment'] = 'The specified file ({0}) does not exist'.format(name)
            return ret

    blocksize = 65536
    m = hashlib.sha1()
    with open(path, 'rb') as f:
        buffer = f.read(blocksize)
        while len(buffer) > 0:
            m.update(buffer)
            buffer = f.read(blocksize)
    local_sha1 = m.hexdigest()
    if local_sha1 == file_data['hash']:
        ret['result'] = True
        ret['comment'] = 'The correct file exists on the printer'
        return ret

    if __opts__['test'] is True:
        ret['result'] = False
        ret['comment'] = ('The file hash on the printer ({}) does not '
                          'match the local hash ({})'.format(file_data['hash'], local_sha1))
        return ret

    ret['comment'] = __salt__['octo_file.upload'](path, name)
    ret['result'] = True
    ret['changes'] = {
        'old sha1': file_data.get('hash'),
        'new sha1': local_sha1,
    } 
    return ret
