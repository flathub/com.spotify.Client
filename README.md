# Spotify

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
env WAYLAND_DISPLAY= flatpak run --branch=beta com.spotify.Client --ozone-platform=x11 --disable-features=UseOzonePlatform
```

To go back to the default behaviour:

```sh
flatpak override --user --reset com.spotify.Client
```
