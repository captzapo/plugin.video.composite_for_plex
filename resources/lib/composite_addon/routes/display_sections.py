# -*- coding: utf-8 -*-
"""

    Copyright (C) 2011-2018 PleXBMC (plugin.video.plexbmc) by hippojay (Dave Hawes-Johnson)
    Copyright (C) 2018-2019 Composite (plugin.video.composite_for_plex)

    This file is part of Composite (plugin.video.composite_for_plex)

    SPDX-License-Identifier: GPL-2.0-or-later
    See LICENSES/GPL-2.0-or-later.txt for more information.
"""

from kodi_six import xbmcplugin  # pylint: disable=import-error

from ..addon.common import get_handle
from ..addon.constants import COMMANDS
from ..addon.constants import CONFIG
from ..addon.constants import MODES
from ..addon.logger import Logger
from ..addon.strings import i18n
from ..addon.utils import create_gui_item
from ..plex import plex

LOG = Logger()


def run(settings, content_filter=None, display_shared=False):
    plex_network = plex.Plex(load=True)
    xbmcplugin.setContent(get_handle(), 'files')

    server_list = plex_network.get_server_list()
    LOG.debug('Using list of %s servers: %s' % (len(server_list), server_list))

    items = []
    items += server_section_menus_items(server_list, content_filter, display_shared, settings)

    if display_shared:
        if items:
            xbmcplugin.addDirectoryItems(get_handle(), items, len(items))

        xbmcplugin.endOfDirectory(get_handle(), cacheToDisc=settings.get_setting('kodicache'))
        return

    # For each of the servers we have identified
    if (settings.get_setting('show_myplex_queue_menu') and
            plex_network.is_myplex_signedin()):
        details = {
            'title': i18n('myPlex Queue')
        }
        extra_data = {
            'type': 'Folder',
            'mode': MODES.MYPLEXQUEUE
        }
        items.append(create_gui_item('http://myplexqueue', details, extra_data, settings=settings))

    items += server_additional_menu_items(server_list, content_filter, settings)
    items += action_menu_items(plex_network, settings)

    if items:
        xbmcplugin.addDirectoryItems(get_handle(), items, len(items))

    xbmcplugin.endOfDirectory(get_handle(), cacheToDisc=settings.get_setting('kodicache'))


def server_section_menus_items(server_list, content_filter, display_shared, settings):
    items = []
    for server in server_list:

        sections = server.get_sections()

        for section in sections:

            if ((display_shared and server.is_owned()) or
                    (content_filter is not None and section.content_type() != content_filter)):
                continue

            if section.content_type() is None:
                LOG.debug('Ignoring section %s: %s of type %s as unable to process'
                          % (server.get_name(), section.get_title(), section.get_type()))
                continue

            if not settings.prefix_server() or (settings.prefix_server() and len(server_list) > 1):
                details = {
                    'title': '%s: %s' % (server.get_name(), section.get_title())
                }
            else:
                details = {
                    'title': section.get_title()
                }

            extra_data = {
                'fanart_image': server.get_fanart(section),
                'type': 'Folder'
            }

            path = section.get_path()

            if settings.get_setting('secondary'):
                mode = MODES.GETCONTENT
            else:
                mode = section.mode()
                path = path + '/all'

            extra_data['mode'] = mode
            section_url = '%s%s' % (server.get_url_location(), path)

            context = None
            if not settings.get_setting('skipcontextmenus'):
                context = [(i18n('Refresh library section'),
                            'RunScript(' + CONFIG['id'] + ', update, %s, %s)' %
                            (server.get_uuid(), section.get_key()))]

            # Build that listing..
            items.append(create_gui_item(section_url, details, extra_data,
                                         context, settings=settings))

    return items


def server_additional_menu_items(server_list, content_filter, settings):
    items = []
    for server in server_list:

        if server.is_offline() or server.is_secondary():
            continue

        # Plex plugin handling
        if (content_filter is not None) and (content_filter != 'plugins'):
            continue

        if not settings.prefix_server() or (settings.prefix_server() and len(server_list) > 1):
            prefix = server.get_name() + ': '
        else:
            prefix = ''

        if settings.get_setting('show_channels_menu'):
            details = {
                'title': prefix + i18n('Channels')
            }
            extra_data = {
                'type': 'Folder',
                'mode': MODES.CHANNELVIEW
            }

            item_url = '%s/channels/all' % server.get_url_location()
            items.append(create_gui_item(item_url, details, extra_data, settings=settings))

        if settings.get_setting('show_plex_online_menu'):
            # Create plexonline link
            details = {
                'title': prefix + i18n('Plex Online')
            }
            extra_data = {
                'type': 'Folder',
                'mode': MODES.PLEXONLINE
            }

            item_url = '%s/system/plexonline' % server.get_url_location()
            items.append(create_gui_item(item_url, details, extra_data, settings=settings))

        if settings.get_setting('show_playlists_menu'):
            # create playlist link
            details = {
                'title': prefix + i18n('Playlists')
            }
            extra_data = {
                'type': 'Folder',
                'mode': MODES.PLAYLISTS
            }

            item_url = '%s/playlists' % server.get_url_location()
            items.append(create_gui_item(item_url, details, extra_data, settings=settings))

        if settings.get_setting('show_widget_menu'):
            # create Widgets link
            details = {
                'title': prefix + i18n('Widgets')
            }
            extra_data = {
                'type': 'Folder',
                'mode': MODES.WIDGETS
            }

            item_url = '%s' % server.get_url_location()
            items.append(create_gui_item(item_url, details, extra_data, settings=settings))

    return items


def action_menu_items(plex_network, settings):
    items = []
    if plex_network.is_myplex_signedin():

        if plex_network.is_plexhome_enabled():
            details = {
                'title': i18n('Switch User')
            }
            extra_data = {
                'type': 'file'
            }

            item_url = 'cmd:' + COMMANDS.SWITCHUSER
            items.append(create_gui_item(item_url, details, extra_data, settings=settings))

        details = {
            'title': i18n('Sign Out')
        }
        extra_data = {
            'type': 'file'
        }

        item_url = 'cmd:' + COMMANDS.SIGNOUT
        items.append(create_gui_item(item_url, details, extra_data, settings=settings))

        details = {
            'title': i18n('Display Servers')
        }
        extra_data = {
            'type': 'file'
        }
        data_url = 'cmd:' + COMMANDS.DISPLAYSERVER
        items.append(create_gui_item(data_url, details, extra_data, settings=settings))

        if settings.get_setting('cache'):
            details = {
                'title': i18n('Clear Caches')
            }
            extra_data = {
                'type': 'file'
            }
            item_url = 'cmd:' + COMMANDS.DELETEREFRESH
            items.append(create_gui_item(item_url, details, extra_data, settings=settings))
    else:
        details = {
            'title': i18n('Sign In')
        }
        extra_data = {
            'type': 'file'
        }

        item_url = 'cmd:' + COMMANDS.SIGNIN
        items.append(create_gui_item(item_url, details, extra_data, settings=settings))

    return items
