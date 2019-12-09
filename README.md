<img src="https://raw.githubusercontent.com/anxdpanic/plugin.video.composite_for_plex/master/resources/media/icon.png" width="256" height="256" alt="Composite">

# Composite

![Build Status](https://img.shields.io/travis/anxdpanic/plugin.video.composite_for_plex/master.svg)
![License](https://img.shields.io/badge/license-GPL--2.0--or--later-success.svg)
![Kodi Version](https://img.shields.io/badge/kodi-jarvis%2B-success.svg)
![Contributors](https://img.shields.io/github/contributors/anxdpanic/plugin.video.composite_for_plex.svg)

Composite allows media and metadata stored in the Plex Media Server (PMS) to be viewed and played using the Kodi 16+ interface.

- Installation
    -
    * Kodi 17+: Enable - `Settings -> System -> Add-ons -> Unknown Sources`
    1. Download repository: [repository.anxdpanic-x.x.x.zip](https://github.com/anxdpanic/_repository/raw/master/zips/repository.anxdpanic/repository.anxdpanic-0.9.8.zip)
    2. [Install from zip file](http://kodi.wiki/view/Add-on_manager#How_to_install_from_a_ZIP_file) (repository.anxdpanic-x.x.x.zip)
    3. [Install from repository](http://kodi.wiki/view/add-on_manager#How_to_install_add-ons_from_a_repository) (anxdpanic Add-on Repository)

- Usage
    -

    Composite should work "out of the box" in most cases, as the default allows for automatic server discovery.
    If this doesn't work, then discovery can be switched off, and a manually entered hostname or IP address can be used.

    If you are watching remotely, or on a bandwidth limited network, switch on Transcoding to reduce the media quality
    to one that works best for you.

- Kodi 18+ Library
    -
    
    To add Composite (Plex) media to your library, add a video source for movies/tv shows.
 
    - Will not have support for most Plex features.
    - Watched status is not imported to your library, Plex's watched status will still be updated on playback.
    
    #### Sources
   
    - **Movies:** `plugin://plugin.video.composite_for_plex/library/movies/`
    - **TV Shows:** `plugin://plugin.video.composite_for_plex/library/tvshows/`

    **Wiki:** https://kodi.wiki/view/Adding_video_sources <br/>
    Instead of Steps 4-5 add the appropriate `plugin://` url from the sources above

- TraktToKodi
    -
    
    This add-on can be paired with the TraktToKodi web browser extension. <br/>
    
    In your TraktToKodi profile, set the `Add-on ID` to `plugin.video.composite_for_plex`

    **Chrome:**
    - Install from [Chrome Web Store](https://chrome.google.com/webstore/detail/trakttokodi/jongfgkokmlpdekeljpegeldjofbageo) <br/>
    - https://github.com/anxdpanic/TraktToKodi-Extension/tree/chrome
    
    **Firefox:**
    - Install from [AMO Gallery](https://addons.mozilla.org/en-US/firefox/addon/trakttokodi/)
    - https://github.com/anxdpanic/TraktToKodi-Extension/tree/firefox

- Support
    -

    Post an [Issue](https://github.com/anxdpanic/plugin.video.composite_for_plex/issues)

---

This add-on is a fork of PleXBMC by Hippojay

https://github.com/hippojay/plugin.video.plexbmc

https://github.com/Tgxcorporation/plugin.video.plexbmc
