#include "Arduino.h"
#include "AppConfig.h"
#include "NetworkService.h"
#include "MetricsClient.h"
#include "DHT.h"
#define MINUTE 1000 * 60

ConfigBuilder app_config_builder = ConfigBuilder();
NetworkService wifi_service = NetworkService();
MetricsHTTPClient metrics_client = MetricsHTTPClient();
MetricsMQTTClient metrics_mqtt_client;
bool ready = false;

Config config;
MessagingConfig messaging_config;
DHT dht;

void setup()
{
    config = app_config_builder.Build();
    dht.setup(config.temperatureSensorInputPin, DHT::DHT11);

    Serial.begin(config.baudrate);
    wifi_service.MakeInitialConfigurationWifiAP();

    while (!ready)
    {
        Result<NetworkSettings> networkSettings = wifi_service.WaitForConfigurationAndConnect();
        // replace with cache check
        if (!networkSettings.ok)
        {
            continue;
        }
        Result<MessagingConfig> mConfig = metrics_client.GetMessagingConfig(
            networkSettings.value->registerURL,
            networkSettings.value->macAddr,
            networkSettings.value->ipAddr);

        if (mConfig.ok)
        {
            ready = true;
            messaging_config.brokerIP = mConfig.value->brokerIP;
            messaging_config.brokerPort = mConfig.value->brokerPort;
            messaging_config.topic = mConfig.value->topic;
            messaging_config.deviceId = mConfig.value->deviceId;
            Serial.println("Configuration completed. Starting sending metrics");

            // clean-up memory
            delete mConfig.value;
            delete networkSettings.value;
        }
        delay(5000);
    }
    metrics_mqtt_client.Begin(messaging_config.brokerIP, messaging_config.brokerPort, messaging_config.deviceId);
}

void loop()
{
    metrics_mqtt_client.SendMeasurements(messaging_config.topic, dht.getTemperature(), dht.getHumidity());
    delay(MINUTE / 2);
}
