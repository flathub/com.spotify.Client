# Spotify

### Reporting bugs

This is community flatpak packaging of official spotify binaries. Please report issues only specifically related to flatpak. Issues reproducible on other platforms can be reported directly in [upstream](https://community.spotify.com/t5/Desktop-Linux/bd-p/desktop_linux).

### Making flags persistent

Below is an example spotify-flags.conf file that defines the flags --disable-gpu-shader-disk-cache:

```
~/.var/app/com.spotify.Client/config/spotify-flags.conf

# This line will be ignored.
--disable-gpu-shader-disk-cache
```

### Wayland

This package runs Wayland by default; an X11 fallback is in place for X11 environments. To force a single X11 run (from Wayland), use:

```sh
flatpak override --user --socket=x11 com.spotify.Client
env WAYLAND_DISPLAY= flatpak run com.spotify.Client --ozone-platform=x11 --disable-features=UseOzonePlatform
```

To go back to the default behaviour:

```sh
flatpak override --user --reset com.spotify.Client
```

### Pipewire and Pulseaudio

Recent Spotify versions use pipewire audio output by default, on older systems pipewire daemon may be not available. In order to switch back to pulseaudio daemon, specify appropriate flag during one-time launch:

```sh
flatpak run com.spotify.Client --audio-api=pulseaudio
```

In order to make it persistent, write the option into config file described in #### Making flags persistent:
```
~/.var/app/com.spotify.Client/config/spotify-flags.conf

# This line will be ignored.
--audio-api=pulseaudio
```
