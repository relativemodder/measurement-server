#include <OneWire.h>
#include <DallasTemperature.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

#define ONE_WIRE_BUS 0                // Пин подключения OneWire шины, 0 (D3)
OneWire oneWire(ONE_WIRE_BUS);        // Подключаем бибилотеку OneWire
DallasTemperature sensors(&oneWire);  // Подключаем бибилотеку DallasTemperature

float sensor0_value = 0.0;
float sensor1_value = 0.0;
float sensor2_value = 0.0;
float sensor3_value = 0.0;

DeviceAddress temperatureSensors[4];  // Размер массива определяем исходя из количества установленных датчиков
uint8_t deviceCount = 0;

const char* ssid = "Green_Roof";
const char* password = "00005555";

//Your Domain name with URL path or IP address with path
const char* serverName = "http://193.124.118.234/api/temperature";

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
// Set timer to 10 seconds (10000)
unsigned long timerDelay = 10000;


// Функция вывода адреса датчика
void printAddress(DeviceAddress deviceAddress) {
  for (uint8_t i = 0; i < 8; i++) {
    if (deviceAddress[i] < 16) Serial.print("0");
    Serial.print(deviceAddress[i], HEX);  // Выводим адрес датчика в HEX формате
  }
}

void setup(void) {
  Serial.begin(115200);                    // Задаем скорость соединения с последовательным портом
  sensors.begin();                         // Иницилизируем датчики
  deviceCount = sensors.getDeviceCount();  // Получаем количество обнаруженных датчиков

  for (uint8_t index = 0; index < deviceCount; index++) {
    sensors.getAddress(temperatureSensors[index], index);
  }

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.println("Timer set to 10 seconds (timerDelay variable), it will take 10 seconds before publishing the first reading.");
}

void loop(void) {
 //Send an HTTP POST request every 10 minutes
  if ((millis() - lastTime) > timerDelay) {
    sensors.requestTemperatures();
    sensor0_value = sensors.getTempC(temperatureSensors[0]);
    sensor1_value = sensors.getTempC(temperatureSensors[1]);
    sensor2_value = sensors.getTempC(temperatureSensors[2]);
    sensor3_value = sensors.getTempC(temperatureSensors[3]);

     if (WiFi.status() == WL_CONNECTED) {
      WiFiClient client;
      HTTPClient http;
       // Your Domain name with URL path or IP address with path
      http.begin(client, serverName);
      // Specify content-type header
      http.addHeader("Content-Type", "application/json");
      // Data to send with HTTP POST
      String httpRequestData = "{\"temperatures\": [{\"thermometer_id\": 0, \"value\": " + String(sensor0_value) + "}, {\"thermometer_id\": 1, \"value\": " + String(sensor1_value) +"}, {\"thermometer_id\": 2, \"value\": " + String(sensor2_value) + "}, {\"thermometer_id\": 3, \"value\": " + String(sensor3_value) + "}], \"pseudo_table_id\": \"string\"}";           
      Serial.print("HTTP Request Data: ");
      Serial.println(httpRequestData);
      
      int httpResponseCode = http.POST(httpRequestData);
      
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      // Free resources
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}
