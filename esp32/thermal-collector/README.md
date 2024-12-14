# Thermal collector
Device collects metrics and sends them to metrics service

## Hardware
This thermal collector is built using dht11 temperature&humidity sensor. I use GPIO 16 for data wire.

## Data transfer
The temperature and humidity are published to a MQTT topic received from server. The data is sent
in JSON format as {"temperature": FLOAT, "humidity": FLOAT}.

## TODOS:
- [ ] Cache WiFi and broker settings between restarts
