#include "NetworkService.h"
#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include <esp_wifi.h>
#include "Types.h"

unsigned char mac[6];
const char *APSsid = "esp32tc-point-ap";
String wifiSsid, wifiPwd, apiKey;

String registerURL = "";
String wifiAddr = "";
String macAddr = "";
NetworkSettings *networkSettingsLocalPtr;

IPAddress local_ip(192, 168, 1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

bool wifiReleased;

String macToString(const unsigned char *mac)
{
    String result = "";
    for (int i = 0; i < 6; i++)
    {
        result += String(mac[i], HEX);
        if (i < 5)
        {
            result += ':';
        }
    }
    result.toUpperCase();
    return result;
}

Result<NetworkSettings> NetworkService::WaitForConfigurationAndConnect()
{
    if (macAddr != "")
    { // we have already connected to WiFi
        return Result<NetworkSettings>(networkSettingsLocalPtr);
    }

    if (wifiSsid != "" && wifiPwd != "" && wifiReleased)
    {
        // end handling requests
        server_.end();
        WiFi.mode(WIFI_STA);

        Serial.print("Connecting to ");
        Serial.println(wifiSsid);

        // connect to wifi sent from a configuration
        WiFi.begin(wifiSsid, wifiPwd);
        while (WiFi.status() != WL_CONNECTED)
        {
            Serial.print(".");
            delay(500);
        }

        Serial.print("\nConnected to the WiFi network. \nLocal IP: ");
        Serial.println(WiFi.localIP());

        wifiAddr = WiFi.localIP().toString();
        macAddr = GetMacAddress(true);
        networkSettingsLocalPtr = new NetworkSettings{registerURL, macAddr, wifiAddr};
        return Result<NetworkSettings>(networkSettingsLocalPtr);
    }
    return Result<NetworkSettings>();
};

String NetworkService::GetMacAddress(bool printToSerial)
{
    esp_err_t ret = esp_wifi_get_mac(WIFI_IF_STA, mac);
    if (ret == ESP_OK && printToSerial)
    {
        Serial.printf("MAC: %02x:%02x:%02x:%02x:%02x:%02x\n",
                      mac[0], mac[1], mac[2],
                      mac[3], mac[4], mac[5]);
    }
    return macToString(mac);
}
void NetworkService::MakeInitialConfigurationWifiAP()
{
    wifiReleased = false;
    Serial.println("\n[*] Creating Wifi spot");
    WiFi.softAP(APSsid, "esp32passphrase", 9);
    WiFi.softAPConfig(local_ip, gateway, subnet);

    Serial.print("[+] AP Created with IP Gateway ");
    Serial.println(WiFi.softAPIP());

    server_.on("/configure", HTTP_POST, [](AsyncWebServerRequest *request)
               {
        wifiSsid = request->getHeader(String("XXX-HL-WIFI-SSID"))->value();
        wifiPwd = request->getHeader(String("XXX-HL-WIFI-PWD"))->value();
        apiKey = request->getHeader(String("XXX-HL-API-KEY"))->value();
        registerURL = request->getHeader(String("XXX-HL-REGISTER-URL"))->value();
        request->send(200, "text/html", "Configuration accepted!");
        wifiReleased = true; });

    server_.begin();
    Serial.println("[*] Waiting for client...");
}
