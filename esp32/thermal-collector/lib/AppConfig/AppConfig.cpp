#include "AppConfig.h"

Config ConfigBuilder::Build()
{
    Config values = Config{};
    values.baudrate = 115200;
    values.temperatureSensorInputPin = 16;
    return values;
}
