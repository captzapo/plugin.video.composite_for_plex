# -*- coding: utf-8 -*-
"""

    Copyright (C) 2019 Composite (plugin.video.composite_for_plex)

    This file is part of Composite (plugin.video.composite_for_plex)

    SPDX-License-Identifier: GPL-2.0-or-later
    See LICENSES/GPL-2.0-or-later.txt for more information.
"""

import platform
import sys
import uuid

from kodi_six import xbmc  # pylint: disable=import-error
from kodi_six import xbmcaddon  # pylint: disable=import-error
from kodi_six import xbmcvfs  # pylint: disable=import-error

from ..addon.settings import AddonSettings

__ID = 'plugin.video.composite_for_plex'
__ADDON = xbmcaddon.Addon(id=__ID)

SETTINGS = AddonSettings(__ID)


def get_device_name(device_name):
    if device_name is None:
        device_name = SETTINGS.get_setting('devicename')
    return device_name


def get_client_identifier(client_id):
    if client_id is None:
        client_id = SETTINGS.get_setting('client_id')

        if not client_id:
            client_id = str(uuid.uuid4())
            SETTINGS.set_setting('client_id', client_id)

    return client_id


def create_plex_identification(device_name=None, client_id=None, user=None, token=None):
    headers = {
        'X-Plex-Device': get_device(),
        'X-Plex-Client-Platform': 'Kodi',
        'X-Plex-Device-Name': get_device_name(device_name),
        'X-Plex-Language': 'en',
        'X-Plex-Platform': platform.uname()[0],
        'X-Plex-Client-Identifier': get_client_identifier(client_id),
        'X-Plex-Product': __ADDON.getAddonInfo('name'),
        'X-Plex-Platform-Version': platform.uname()[2],
        'X-Plex-Version': '0.0.0a1',
        'X-Plex-Provides': 'player,controller'
    }

    if token is not None:
        headers['X-Plex-Token'] = token

    if user is not None:
        headers['X-Plex-User'] = user

    return headers


def get_device():
    device = None
    if xbmc.getCondVisibility('system.platform.windows'):
        device = 'Windows'
    if xbmc.getCondVisibility('system.platform.linux') \
       and not xbmc.getCondVisibility('system.platform.android'):
        device = 'Linux'
    if xbmc.getCondVisibility('system.platform.osx'):
        device = 'Darwin'
    if xbmc.getCondVisibility('system.platform.android'):
        device = 'Android'
    if xbmcvfs.exists('/etc/os-release') \
       and 'libreelec' in xbmcvfs.File('/etc/os-release').read():
        device = 'LibreELEC'
    if xbmcvfs.exists('/proc/device-tree/model') \
       and 'Raspberry Pi' in xbmcvfs.File('/proc/device-tree/model').read():
        device = 'Raspberry Pi'
    if device is None:
        try:
            device = platform.system()
        except:  # pylint: disable=bare-except
            try:
                device = platform.platform(terse=True)
            except:  # pylint: disable=bare-except
                device = sys.platform

    return device
