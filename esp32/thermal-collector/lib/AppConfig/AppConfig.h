#ifndef APP_CONFIG_H
#define APP_CONFIG_H

struct Config {
    int baudrate;
    const char *wifi_ssid;
    const char *wifi_password;
};

class ConfigBuilder{
    public:
        Config Build();
};

#endif