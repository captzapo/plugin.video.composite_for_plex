# -*- coding: utf-8 -*-
"""

    Copyright (C) 2011-2018 PleXBMC (plugin.video.plexbmc) by hippojay (Dave Hawes-Johnson)
    Copyright (C) 2018-2019 Composite (plugin.video.composite_for_plex)

    This file is part of Composite (plugin.video.composite_for_plex)

    SPDX-License-Identifier: GPL-2.0-or-later
    See LICENSES/GPL-2.0-or-later.txt for more information.
"""

import platform
import sys
import time

from .addon.common import get_params
from .addon.constants import COMMANDS
from .addon.constants import CONFIG
from .addon.constants import MODES
from .addon.constants import STREAM_CONTROL_MAP
from .addon.logger import Logger
from .addon.settings import AddonSettings

LOG = Logger()


def run(start_time):  # pylint: disable=too-many-locals, too-many-statements, too-many-branches, too-many-return-statements
    settings = AddonSettings()

    if settings.get_setting('wolon'):
        from .addon.wol import wake_servers  # pylint: disable=import-outside-toplevel
        wake_servers(settings)

    params = get_params()

    try:
        mode = int(params.get('mode', MODES.UNSET))
    except ValueError:
        mode = params.get('mode')

    command = params.get('command', COMMANDS.UNSET)
    path_mode = params.get('path_mode')

    library = path_mode is not None and path_mode.startswith('library/')
    media_id = params.get('media_id')
    server_uuid = params.get('server_uuid')

    url = params.get('url')

    LOG.debug('%s %s: Kodi %s on %s with Python %s' %
              (CONFIG['name'], CONFIG['version'], CONFIG['kodi_version'],
               platform.uname()[0], '.'.join([str(i) for i in sys.version_info])),
              no_privacy=True)  # force no privacy to avoid redacting version strings

    LOG.debug('Mode |%s| Command |%s| Url |%s| Parameters |%s| Server UUID |%s| Media Id |%s|'
              % (mode, command, url, params, server_uuid, media_id))

    LOG.debug('Settings:\nFullRes Thumbs |%s| Streaming |%s| Filter Menus |%s| Flatten |%s|\n'
              'Stream Control |%s| Force DVD |%s| SMB IP Override |%s| NAS IP |%s|' %
              (settings.get_setting('fullres_thumbs'),
               settings.get_stream(),
               settings.get_setting('secondary'),
               settings.get_setting('flatten'),
               STREAM_CONTROL_MAP.get(settings.get_setting('streamControl')),
               settings.get_setting('forcedvd'),
               settings.get_setting('nasoverride'),
               settings.get_setting('nasoverrideip')))

    if command == COMMANDS.REFRESH:
        from .routes import refresh  # pylint: disable=import-outside-toplevel
        refresh.run(settings)
        return _finished(start_time)

    if command == COMMANDS.SWITCHUSER:
        from .routes import switch_user  # pylint: disable=import-outside-toplevel
        switch_user.run()
        return _finished(start_time)

    if command == COMMANDS.SIGNOUT:
        from .routes import sign_out  # pylint: disable=import-outside-toplevel
        sign_out.run()
        return _finished(start_time)

    if command == COMMANDS.SIGNIN:
        from .routes import sign_in  # pylint: disable=import-outside-toplevel
        sign_in.run()
        return _finished(start_time)

    if command == COMMANDS.SIGNINTEMP:
        from .routes import sign_in_temp  # pylint: disable=import-outside-toplevel
        sign_in_temp.run()
        return _finished(start_time)

    if command == COMMANDS.MANAGEMYPLEX:
        from .routes import manage_my_plex  # pylint: disable=import-outside-toplevel
        manage_my_plex.run()
        return _finished(start_time)

    if command == COMMANDS.DISPLAYSERVER:
        from .routes import display_known_servers  # pylint: disable=import-outside-toplevel
        display_known_servers.run()
        return _finished(start_time)

    if command == COMMANDS.DELETEREFRESH:
        from .routes import delete_refresh  # pylint: disable=import-outside-toplevel
        delete_refresh.run()
        return _finished(start_time)

    if command == COMMANDS.UPDATE:
        from .routes import refresh_library  # pylint: disable=import-outside-toplevel
        refresh_library.run()
        return _finished(start_time)

    # Mark an item as watched/unwatched in plex
    if command == COMMANDS.WATCH:
        from .routes import watch_status  # pylint: disable=import-outside-toplevel
        watch_status.run()
        return _finished(start_time)

    # delete media from PMS
    if command == COMMANDS.DELETE:
        from .routes import delete_media  # pylint: disable=import-outside-toplevel
        delete_media.run()
        return _finished(start_time)

    # Display subtitle selection screen
    if command == COMMANDS.SUBS:
        from .routes import set_subtitles  # pylint: disable=import-outside-toplevel
        set_subtitles.run()
        return _finished(start_time)

    # Display audio stream selection screen
    if command == COMMANDS.AUDIO:
        from .routes import set_audio  # pylint: disable=import-outside-toplevel
        set_audio.run()
        return _finished(start_time)

    # Allow a master server to be selected (for myPlex Queue)
    if command == COMMANDS.MASTER:
        from .routes import set_master_server  # pylint: disable=import-outside-toplevel
        set_master_server.run(settings)
        return _finished(start_time)

    if command == COMMANDS.DELETEFROMPLAYLIST:
        from .routes import delete_playlist_item  # pylint: disable=import-outside-toplevel
        delete_playlist_item.run()
        return _finished(start_time)

    if command == COMMANDS.ADDTOPLAYLIST:
        from .routes import add_playlist_item  # pylint: disable=import-outside-toplevel
        add_playlist_item.run()
        return _finished(start_time)

    if mode in [MODES.TXT_OPEN, MODES.TXT_PLAY]:
        from .routes import trakttokodi  # pylint: disable=import-outside-toplevel
        trakttokodi.run(settings, params)
        return _finished(start_time)

    if ((path_mode in [MODES.TXT_MOVIES_LIBRARY, MODES.TXT_TVSHOWS_LIBRARY] and
         (mode is None or mode == MODES.UNSET)) or params.get('kodi_action')):
        from .routes import kodi_library  # pylint: disable=import-outside-toplevel
        kodi_library.run(settings, params)
        return _finished(start_time)

    # Run a function based on the mode variable that was passed in the URL
    if (isinstance(mode, int) and mode < 0) or (not url and (not server_uuid and not media_id)):
        from .routes import display_sections  # pylint: disable=import-outside-toplevel
        display_sections.run(settings)
        return _finished(start_time)

    if mode in [MODES.GETCONTENT, MODES.TXT_TVSHOWS, MODES.TXT_MOVIES,
                MODES.TXT_MOVIES_ON_DECK, MODES.TXT_MOVIES_RECENT_ADDED,
                MODES.TXT_MOVIES_RECENT_RELEASE, MODES.TXT_TVSHOWS_ON_DECK,
                MODES.TXT_TVSHOWS_RECENT_ADDED, MODES.TXT_TVSHOWS_RECENT_AIRED]:
        from .routes import get_content  # pylint: disable=import-outside-toplevel
        get_content.run(settings, url, server_uuid, mode)
        return _finished(start_time)

    if mode == MODES.TVSHOWS:
        from .routes import process_shows  # pylint: disable=import-outside-toplevel
        process_shows.run(settings, url)
        return _finished(start_time)

    if mode == MODES.MOVIES:
        from .routes import process_movies  # pylint: disable=import-outside-toplevel
        process_movies.run(settings, url)
        return _finished(start_time)

    if mode == MODES.ARTISTS:
        from .routes import process_artists  # pylint: disable=import-outside-toplevel
        process_artists.run(settings, url)
        return _finished(start_time)

    if mode == MODES.TVSEASONS:
        from .routes import process_seasons  # pylint: disable=import-outside-toplevel
        process_seasons.run(settings, url, rating_key=params.get('rating_key'), library=library)
        return _finished(start_time)

    if mode == MODES.PLAYLIBRARY:
        from .routes import play_library_media  # pylint: disable=import-outside-toplevel
        play_library_media.run(settings, url=url, server_uuid=server_uuid, media_id=media_id,
                               transcode=int(params.get('transcode', 0)) == 1,
                               transcode_profile=params.get('transcode_profile'))
        return _finished(start_time)

    if mode == MODES.TVEPISODES:
        from .routes import process_episodes  # pylint: disable=import-outside-toplevel
        process_episodes.run(settings, url, rating_key=params.get('rating_key'), library=library)
        return _finished(start_time)

    if mode == MODES.PLEXPLUGINS:
        from .routes import process_plex_plugins  # pylint: disable=import-outside-toplevel
        process_plex_plugins.run(settings, url)
        return _finished(start_time)

    if mode == MODES.PROCESSXML:
        from .routes import process_xml  # pylint: disable=import-outside-toplevel
        process_xml.run(settings, url)
        return _finished(start_time)

    if mode == MODES.BASICPLAY:
        from .routes import play_media_stream  # pylint: disable=import-outside-toplevel
        play_media_stream.run(url)
        return _finished(start_time)

    if mode == MODES.ALBUMS:
        from .routes import process_albums  # pylint: disable=import-outside-toplevel
        process_albums.run(settings, url)
        return _finished(start_time)

    if mode == MODES.TRACKS:
        from .routes import process_tracks  # pylint: disable=import-outside-toplevel
        process_tracks.run(settings, url)
        return _finished(start_time)

    if mode == MODES.PHOTOS:
        from .routes import process_photos  # pylint: disable=import-outside-toplevel
        process_photos.run(settings, url)
        return _finished(start_time)

    if mode == MODES.MUSIC:
        from .routes import process_music  # pylint: disable=import-outside-toplevel
        process_music.run(settings, url)
        return _finished(start_time)

    if mode == MODES.VIDEOPLUGINPLAY:
        from .routes import play_video_channel  # pylint: disable=import-outside-toplevel
        play_video_channel.run(settings, url, params.get('identifier'), params.get('indirect'))
        return _finished(start_time)

    if mode == MODES.PLEXONLINE:
        from .routes import plex_online  # pylint: disable=import-outside-toplevel
        plex_online.run(settings, url)
        return _finished(start_time)

    if mode == MODES.CHANNELINSTALL:
        from .routes import install_plugin  # pylint: disable=import-outside-toplevel
        install_plugin.run(url, params.get('name', ''))
        return _finished(start_time)

    if mode == MODES.CHANNELVIEW:
        from .routes import channel_view  # pylint: disable=import-outside-toplevel
        channel_view.run(settings, url)
        return _finished(start_time)

    if mode == MODES.PLAYLIBRARY_TRANSCODE:
        from .routes import play_library_media  # pylint: disable=import-outside-toplevel
        play_library_media.run(settings, url=url, transcode=True)
        return _finished(start_time)

    if mode == MODES.MYPLEXQUEUE:
        from .routes import myplex_queue  # pylint: disable=import-outside-toplevel
        myplex_queue.run()
        return _finished(start_time)

    if mode == MODES.CHANNELSEARCH:
        from .routes import channel_search  # pylint: disable=import-outside-toplevel
        channel_search.run(settings, url, params.get('prompt'))
        return _finished(start_time)

    if mode == MODES.CHANNELPREFS:
        from .routes import channel_settings  # pylint: disable=import-outside-toplevel
        channel_settings.run(url, params.get('id'))
        return _finished(start_time)

    if mode == MODES.SHARED_MOVIES:
        from .routes import display_sections  # pylint: disable=import-outside-toplevel
        display_sections.run(settings, content_filter='movies', display_shared=True)
        return _finished(start_time)

    if mode == MODES.SHARED_SHOWS:
        from .routes import display_sections  # pylint: disable=import-outside-toplevel
        display_sections.run(settings, content_filter='tvshows', display_shared=True)
        return _finished(start_time)

    if mode == MODES.SHARED_PHOTOS:
        from .routes import display_sections  # pylint: disable=import-outside-toplevel
        display_sections.run(settings, content_filter='photos', display_shared=True)
        return _finished(start_time)

    if mode == MODES.SHARED_MUSIC:
        from .routes import display_sections  # pylint: disable=import-outside-toplevel
        display_sections.run(settings, content_filter='music', display_shared=True)
        return _finished(start_time)

    if mode == MODES.SHARED_ALL:
        from .routes import display_sections  # pylint: disable=import-outside-toplevel
        display_sections.run(settings, display_shared=True)
        return _finished(start_time)

    if mode == MODES.PLAYLISTS:
        from .routes import process_xml  # pylint: disable=import-outside-toplevel
        process_xml.run(settings, url)
        return _finished(start_time)

    if mode == MODES.DISPLAYSERVERS:
        from .routes import display_plex_servers  # pylint: disable=import-outside-toplevel
        display_plex_servers.run(settings, url)
        return _finished(start_time)

    if mode == MODES.WIDGETS:
        from .routes import widgets  # pylint: disable=import-outside-toplevel
        widgets.run(settings, url)
        return _finished(start_time)

    return _finished(start_time)


def _finished(start_time):
    LOG.debug('Finished. |%.3fs|' % (time.time() - start_time))
