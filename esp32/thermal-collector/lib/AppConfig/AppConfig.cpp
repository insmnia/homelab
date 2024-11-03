#include "AppConfig.h"

Config ConfigBuilder::Build()
{
    Config values = Config{};
    values.baudrate = 115200;
    values.wifi_ssid = "HorekihWifi";
    values.wifi_password = "horekihwifi2";
    return values;
}
