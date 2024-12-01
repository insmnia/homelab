#ifndef METRICS_CLIENT_H
#define METRICS_CLIENT_H

#include "Arduino.h"
#include "Types.h"

struct MessagingConfig
{
    String brokerIP;
    int brokerPort;
    String topic;
    long deviceId;

    MessagingConfig(String brokerIP_, int brokerPort_, String topic_, long deviceId_)
    {
        brokerIP = brokerIP_;
        brokerPort = brokerPort_;
        topic = topic_;
        deviceId = deviceId_;
    }
    MessagingConfig() {};
};

class MetricsHTTPClient
{
public:
    Result<MessagingConfig> GetMessagingConfig(String deviceRegisterURL, String macAddr, String ipAddr);
};

class MetricsMQTTClient
{
};

#endif