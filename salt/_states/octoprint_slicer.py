# -*- coding: utf-8 -*-
'''
Manage OctoPrint slicer profiles
================================

This state is useful for firing messages during state runs, using the SMTP
protocol

.. code-block:: yaml

    server-warning-message:
      smtp.send_msg:
        - name: 'This is a server warning message'
        - profile: my-smtp-account
        - recipient: admins@example.com
'''
# Import Python libs
from __future__ import absolute_import, unicode_literals, print_function
import logging

log = logging.getLogger(__name__)
__virtualname__ = 'octo_slicer'


def __virtual__():
    '''
    Only load if the SMTP module is available in __salt__
    '''
    if __opts__['pillar']['proxy']['proxytype'] == 'octoprint':
        return True
    return (False, 'The OctoPrint modules cannot be loaded: proxy is not configured.')


def profile(name, slicer, profile=None, absent=False):
    '''
    Manage the slicer profile

    .. code-block:: yaml

        10-perc-fill-20mms:
          octo_slicer.profile:
            - slicer: curalegacy
            - profile:
                displayName: example
                data:
                  layer_height: 0.2

        10-perc-fill-200mms:
          octo_slicer.profile:
            - slicer: curalegacy
            - absent: True

    name
        The message to send via SMTP

    slicer
        The name of the slicer to use

    profile
        A dictionary containing data for the slicing profile

    absent
        If True, the profile will be deleted
    '''
    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    if profile is None and absent is False:
        ret['result'] = False
        ret['comment'] = 'Missing profile or absent parameters'
        return ret

    slicers = __salt__['octo_slicer.list']().keys()
    old_data = __salt__['octo_slicer.get_profile'](slicer, name)

    if old_data == 'Either the slicer or the profile was not found':
        ret['result'] = False
        if slicer in slicers:
            ret['comment'] = 'The specified slicer ({0}) exists, but the profile does not'.format(slicer)
        else:
            ret['comment'] = 'The specified slicer ({0}) does not exist'.format(slicer)
        if __opts__['test'] is True:
            return ret

    del old_data['key']
    del old_data['default']
    del old_data['resource']

    if old_data == profile:
        ret['result'] = True
        ret['comment'] = 'data matches'
        return ret
    else:
        ret['comment'] = 'data does not match'

    if __opts__['test'] is True:
        return ret

    __salt__['octo_slicer.save_profile'](slicer, name, profile)

    ret['result'] = True
    ret['changes'] = {
        'old': old_data,
        'new': profile,
    }

    return ret
