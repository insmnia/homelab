#ifndef NETWORK_SERVICE_H
#define NETWORK_SERVICE_H

#include "ESPAsyncWebServer.h"
#include "Arduino.h"
#include "Types.h"

struct NetworkSettings
{
    String registerURL;
    String macAddr;
    String ipAddr;

    NetworkSettings(String registerURL_, String macAddr_, String ipAddr_)
    {
        registerURL = registerURL_;
        macAddr = macAddr_;
        ipAddr = ipAddr_;
    }
};

class NetworkService
{
public:
    Result<NetworkSettings> WaitForConfigurationAndConnect();
    void MakeInitialConfigurationWifiAP();
    String GetMacAddress(bool printToSerial);

private:
    unsigned long currentTime_ = millis();
    unsigned long previousTime_ = 0;
    // Define timeout time in milliseconds (example: 2000ms = 2s)
    const long timeoutTime_ = 2000;
    AsyncWebServer server_ = AsyncWebServer(80);
    bool connectedToTargetWifi_;
};

#endif