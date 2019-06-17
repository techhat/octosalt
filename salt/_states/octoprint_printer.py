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
import logging

log = logging.getLogger(__name__)
__virtualname__ = 'octo_printer'


def __virtual__():
    '''
    Only load the module if proxy configuration is present
    '''
    if __opts__['pillar'].get('proxy', {}).get('proxytype', '') == 'octoprint':
        return True
    return (False, 'The OctoPrint modules cannot be loaded: proxy is not configured.')


def profile(name, profile=None, absent=False):
    '''
    Manage the slicer profile

    .. code-block:: yaml

    _default:
      octo_printer.profile:
        - profile:
            id: _default
            model: My Printer
            name: Default

    name
        The name of the printer profile

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

    printers = __salt__['octo_printer.list']()['profiles']

    if name not in printers:
        ret['result'] = False
        ret['comment'] = 'The specified printer ({0}) does not exist'.format(name)
        if __opts__['test'] is True:
            return ret

    old_data = printers.get(name, {})
    del old_data['resource']
    for item in ('axes', 'color', 'current', 'default', 'extruder', 'heatedBed',
                 'heatedChamber', 'volume'):
        # These items show in the return data, even if they weren't in the state
        if item not in profile:
            del old_data[item]

    if old_data == profile:
        ret['result'] = True
        ret['comment'] = 'profile matches'
        return ret
    else:
        ret['comment'] = 'profile does not match'

    if __opts__['test'] is True:
        return ret

    if not old_data:
        __salt__['octo_printer.add_profile']({'profile': profile})
    else:
        ret['comment'] = __salt__['octo_printer.update_profile'](name, {'profile': profile})

    ret['result'] = True
    ret['changes'] = {
        'old': old_data,
        'new': profile,
    }

    return ret
