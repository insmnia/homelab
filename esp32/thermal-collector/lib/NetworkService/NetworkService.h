#ifndef NETWORK_SERVICE_H
#define NETWORK_SERVICE_H

class NetworkService
{
public:
    void ConnectToWifi(const char *ssid, const char *password);
    unsigned char *GetMacAddress(bool printToSerial);
};

#endif