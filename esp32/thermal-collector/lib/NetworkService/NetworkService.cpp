#include "NetworkService.h"
#include "WiFi.h"
#include <esp_wifi.h>

unsigned char mac[6];

void NetworkService::ConnectToWifi(const char *ssid, const char *password)
{
    WiFi.begin(ssid, password);
    Serial.println("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(100);
    }
    Serial.print("\nConnected to the WiFi network. \nLocal IP: ");
    Serial.println(WiFi.localIP());
    GetMacAddress(true);
};

unsigned char *NetworkService::GetMacAddress(bool printToSerial)
{
    esp_err_t ret = esp_wifi_get_mac(WIFI_IF_STA, mac);
    if (ret == ESP_OK && printToSerial)
    {
        Serial.printf("MAC: %02x:%02x:%02x:%02x:%02x:%02x\n",
                      mac[0], mac[1], mac[2],
                      mac[3], mac[4], mac[5]);
    }
    return mac;
}