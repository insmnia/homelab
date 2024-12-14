#ifndef APP_CONFIG_H
#define APP_CONFIG_H

struct Config {
    int baudrate;
    int temperatureSensorInputPin;
};

class ConfigBuilder{
    public:
        Config Build();
};

#endif