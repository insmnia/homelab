#ifndef NETWORK_SERVICE_H
#define NETWORK_SERVICE_H

#include "ESPAsyncWebServer.h"
#include "Arduino.h"

class NetworkService
{
public:
    void WaitForConfigurationAndConnect();
    void MakeInitialConfigurationWifiAP();
    unsigned char *GetMacAddress(bool printToSerial);
    
private:
    unsigned long currentTime_ = millis();
    unsigned long previousTime_ = 0; 
    // Define timeout time in milliseconds (example: 2000ms = 2s)
    const long timeoutTime_ = 2000;
    AsyncWebServer server_ = AsyncWebServer(80);
    bool connectedToTargetWifi_;
};

#endif