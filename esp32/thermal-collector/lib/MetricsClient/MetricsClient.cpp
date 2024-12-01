#include "MetricsClient.h"
#include "HTTPClient.h"
#include "WiFi.h"
#include "Types.h"

WiFiClient wifi_client;
HTTPClient http_client;
char payloadBuffer[2048];
int retries = 1;
const int MAX_RETRIES = 10;
const MessagingConfig emptyConfig = MessagingConfig{"", 0, "", -1};

Result<String> extractIntOrStringValue(const String &jsonString, const String &key)
{
    String searchString = "\"" + key + "\":";
    int keyIndex = jsonString.indexOf(searchString);

    // Return if the key is not found
    if (keyIndex == -1)
    {
        return Result<String>();
    }

    int valueStartIndex = keyIndex + searchString.length();
    int valueEndIndex;

    if (jsonString[valueStartIndex] == '"')
    {
        valueEndIndex = jsonString.indexOf('"', valueStartIndex + 1);
        if (valueEndIndex == -1)
        {
            Serial.printf("[ERROR] Closing quote not found for key: %s\n", key.c_str());
            return Result<String>(); // Error in parsing
        }
    }
    else
    {
        valueEndIndex = jsonString.indexOf(',', valueStartIndex);
        if (valueEndIndex == -1)
        {
            valueEndIndex = jsonString.indexOf('}', valueStartIndex); // Check for closing brace as well
        }
    }

    String value = jsonString.substring(valueStartIndex, valueEndIndex);
    value.trim();

    if (value.startsWith("\""))
    {
        value.remove(0, 1);
    }
    if (value.endsWith("\""))
    {
        value.remove(value.length() - 1);
    }

    // Return the extracted value
    return Result<String>(new String(value));
}

Result<MessagingConfig> MetricsHTTPClient::GetMessagingConfig(String deviceRegisterURL, String macAddr, String ipAddr)
{
    if (retries == MAX_RETRIES)
    {
        Serial.println("[FATAL] Max retries attempt reached. Please verify that service is operating.");
        return Result<MessagingConfig>();
    }
    Serial.printf("[INFO] Requesting configuration from server. Attempt №%d\n", retries++);

    http_client.begin(wifi_client, deviceRegisterURL);
    http_client.addHeader("Content-Type", "application/json");
    http_client.addHeader("accept", "application/json");
    snprintf(
        payloadBuffer,
        sizeof(payloadBuffer),
        "{\"mac\":\"%s\", \"ip\":\"%s\", \"name\":\"%s__%s\"}",
        macAddr.c_str(), ipAddr.c_str(), macAddr.c_str(), ipAddr.c_str());

    int httpResponseCode = http_client.POST(String(payloadBuffer));
    if (httpResponseCode != 201 && httpResponseCode != 200)
    {
        Serial.printf("[ERROR] Error on HTTP request: %s\n", http_client.errorToString(httpResponseCode).c_str());
        return Result<MessagingConfig>();
    }

    String responseBody = http_client.getString();

    http_client.end();

    Result<String> brokerIP = extractIntOrStringValue(responseBody, String("broker_ip"));
    Result<String> brokerPort = extractIntOrStringValue(responseBody, String("broker_port"));
    Result<String> topic = extractIntOrStringValue(responseBody, String("metrics_topic_name"));
    Result<String> deviceId = extractIntOrStringValue(responseBody, String("id"));
    if (!brokerIP.ok || !brokerPort.ok || !topic.ok || !deviceId.ok)
    {
        Serial.println("[ERROR] One of expected fields was not found in response!");
        return Result<MessagingConfig>();
    }

    Serial.printf("%s, %s, %s, %s\n", brokerIP.value, brokerPort.value, topic.value, deviceId.value);
    MessagingConfig config{
        *brokerIP.value,
        brokerPort.value->toInt(),
        *topic.value,
        deviceId.value->toInt()};
    return Result<MessagingConfig>(new MessagingConfig(config));
}