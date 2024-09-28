# Spotify

### Making flags persistent

Below is an example spotify-flags.conf file that defines the flags --disable-gpu-shader-disk-cache:

```
~/.var/app/com.spotify.Client/config/spotify-flags.conf

# This line will be ignored.
--disable-gpu-shader-disk-cache
```

### Wayland

This package enables the flags to run on Wayland, however it is opt-in. To opt-in run:

```sh
flatpak override --user --socket=wayland com.spotify.Client
```

To opt-out:

```sh
flatpak override --user --nosocket=wayland com.spotify.Client
```
