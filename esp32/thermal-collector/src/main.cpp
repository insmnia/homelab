#include "Arduino.h"
#include "AppConfig.h"
#include "NetworkService.h"

ConfigBuilder app_config_builder = ConfigBuilder();
NetworkService wifi_service = NetworkService();
Config config;

void setup() {
    config = app_config_builder.Build();

    Serial.begin(config.baudrate);
    wifi_service.MakeInitialConfigurationWifiAP();
}


void loop(){
    wifi_service.WaitForConfigurationAndConnect();
}
