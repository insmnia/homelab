# Homelab

## Goals
1. Create a server on RPI 5. Server must expose HTTP API to receive collected metrics from devices.
Server itself uses PostgreSQL to store data from different sources. Server must host MQTT broker (NanoMQ) which is used by other devices to transfer metrics.

2. Create collecting points for temperature. Each collecting point consists of esp32 board and
temperature and/or humidity sensor. Each collecting point is set to a different room.
CP sends data over MQTT (broker is hosted on rpi).
