# tado-autoassist
Self-hosted tado autoassist including geofencing and open window detection

## Configuration
You can configure the autoassist though config files, environment variables, or a combination of the two.

For file-based configuration, create a `settings.toml` in the working directory with the following properties:
```
# Tado account data
username = "username"
password = "password"

# Auto assistant update interval settings
# Specify the number of seconds between open window and geofencing checks, or comment one of them out to disable
open_window_interval = 10.0
geofencing_interval = 60.0

# Path to logging file
# Comment out to disable file-based logging
log_file = "autoassist.log"
```
If you want to, you optionally can move the `password` out of the main `settings.toml` into a separate `.secrets.toml`.

For environment variable based configuration, prefix the config file setting names listed above with `TADO_AA_`, e.g.
using `TADO_AA_PASSWORD` to specify the password.

## Docker Deployment [![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/ietz/tado-autoassist)](https://hub.docker.com/r/ietz/tado-autoassist)
To deploy the autoassist with docker, use the [ietz/tado-autoassist](https://hub.docker.com/r/ietz/tado-autoassist) images.
Either mount your `settings.toml` configuration file to `/app/settings.toml`, or set the config environment variables:
```
docker run -d \
    -e 'TADO_AA_USERNAME=me@example.com' \
    -e 'TADO_AA_PASSWORD=password' \
    -e 'TADO_AA_OPEN_WINDOW_INTERVAL=10.0' \
    -e 'TADO_AA_GEOFENCING_INTERVAL=60.0' \
    ietz/tado-autoassist
```
