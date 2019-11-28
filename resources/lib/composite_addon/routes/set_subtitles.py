# -*- coding: utf-8 -*-
"""

    Copyright (C) 2011-2018 PleXBMC (plugin.video.plexbmc) by hippojay (Dave Hawes-Johnson)
    Copyright (C) 2018-2019 Composite (plugin.video.composite_for_plex)

    This file is part of Composite (plugin.video.composite_for_plex)

    SPDX-License-Identifier: GPL-2.0-or-later
    See LICENSES/GPL-2.0-or-later.txt for more information.
"""

import xbmcgui  # pylint: disable=import-error

from ..addon.common import CONFIG
from ..addon.common import PrintDebug
from ..addon.common import encode_utf8
from ..addon.common import get_argv
from ..addon.common import i18n
from ..plex import plex

LOG = PrintDebug(CONFIG['name'])
PLEX_NETWORK = plex.Plex(load=False)


def run():
    """
        Display a list of available Subtitle streams and allow a user to select one.
        The currently selected stream will be annotated with a *
    """

    PLEX_NETWORK.load()

    server_uuid = get_argv()[2]
    metadata_id = get_argv()[3]

    server = PLEX_NETWORK.get_server_from_uuid(server_uuid)
    tree = server.get_metadata(metadata_id)

    sub_list = ['']
    display_list = ['None']
    fl_select = False
    part_id = ''
    for parts in tree.getiterator('Part'):

        part_id = parts.get('id')

        for streams in parts:

            if streams.get('streamType', '') == '3':

                stream_id = streams.get('id')
                lang = encode_utf8(streams.get('languageCode', i18n('Unknown')))
                LOG.debug('Detected Subtitle stream [%s] [%s]' % (stream_id, lang))

                if streams.get('format', streams.get('codec')) == 'idx':
                    LOG.debug('Stream: %s - Ignoring idx file for now' % stream_id)
                    continue

                sub_list.append(stream_id)

                if streams.get('selected') == '1':
                    fl_select = True
                    language = streams.get('language', i18n('Unknown')) + '*'
                else:
                    language = streams.get('language', i18n('Unknown'))

                display_list.append(language)
        break

    if not fl_select:
        display_list[0] = display_list[0] + '*'

    result = xbmcgui.Dialog().select(i18n('Select subtitle'), display_list)
    if result == -1:
        return

    LOG.debug('User has selected stream %s' % sub_list[result])
    server.set_subtitle_stream(part_id, sub_list[result])
