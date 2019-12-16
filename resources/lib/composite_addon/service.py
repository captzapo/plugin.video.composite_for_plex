# -*- coding: utf-8 -*-
"""

    Copyright (C) 2019 Composite (plugin.video.composite_for_plex)

    This file is part of Composite (plugin.video.composite_for_plex)

    SPDX-License-Identifier: GPL-2.0-or-later
    See LICENSES/GPL-2.0-or-later.txt for more information.
"""

from kodi_six import xbmcgui  # pylint: disable=import-error

from .addon.logger import Logger
from .addon.monitor import Monitor
from .addon.player import CallbackPlayer
from .addon.settings import AddonSettings
from .companion import companion
from .companion.client import get_client

LOG = Logger('service')


def run():
    settings = AddonSettings()

    sleep_time = 10

    LOG.debug('Service initialization...')

    window = xbmcgui.Window(10000)
    player = CallbackPlayer(window=window, settings=settings)
    monitor = Monitor()

    companion_thread = None
    if settings.use_companion():
        companion_thread = companion.CompanionReceiverThread(get_client(settings), settings)

    while not monitor.abortRequested():

        if monitor.waitForAbort(sleep_time):
            break

    companion.shutdown(companion_thread)
    player.cleanup_threads(only_ended=False)  # clean up any/all playback monitoring threads
