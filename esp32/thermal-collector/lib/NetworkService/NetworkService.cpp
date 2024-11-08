#include "NetworkService.h"
#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include <esp_wifi.h>

unsigned char mac[6];
const char* APSsid = "esp32tc-point-ap";
String wifiSsid;
String wifiPwd;
IPAddress local_ip(192,168,1,1);
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);

bool wifiReleased;


void NetworkService::WaitForConfigurationAndConnect()
{
    if (connectedToTargetWifi_){
        return;
    }
    if(wifiSsid != "" && wifiPwd != "" && wifiReleased){
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
            delay(100);
        }
        connectedToTargetWifi_ = true;

        Serial.print("\nConnected to the WiFi network. \nLocal IP: ");
        Serial.println(WiFi.localIP());

        GetMacAddress(true);
    }
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
void NetworkService::MakeInitialConfigurationWifiAP(){
    wifiReleased = false;
    Serial.println("\n[*] Creating Wifi spot");
    WiFi.softAP(APSsid, "");
    WiFi.softAPConfig(local_ip, gateway, subnet);

    Serial.print("[+] AP Created with IP Gateway ");
    Serial.println(WiFi.softAPIP());

    server_.on("/configure", HTTP_POST, [](AsyncWebServerRequest* request) { 
	   wifiSsid = request->getHeader(String("XXX-HL-WIFI-SSID"))->value();
	   wifiPwd = request->getHeader(String("XXX-HL-WIFI-PWD"))->value();
	   request->send(200, "text/html", "Configuration accepted!");
       wifiReleased = true;
	 });

    server_.begin();
    Serial.println("[*] Waiting for client...");
}