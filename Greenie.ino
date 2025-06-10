
// Include the DHT11 library for interfacing with the sensor.
#include "DHT.h"
#include <Servo.h>
#include <ArduinoJson.h>


#define DHTPIN 7 
#define DHTTYPE DHT11 
DHT dht(DHTPIN, DHTTYPE);

const int waterSensorPin = A0;
const int lightSensorPin = A1;
const int soilSensorPin = A3;

const int ECO = 8;
const int TRIG = 9;
const int pinServos = 10;
const int pinRelayBomb = 11;
const int pinRelayVent = 12;
const int pinRelayLuz = 13;

int contadorTempAlta = 0;
int contadorTempBaja = 0;

int DURACION;
int DISTANCIA;
int Tanque = 22;

int umbralTemp = 26;

bool ventilador = false;
bool tapaSuperior = false;
bool luces = true;


int lecturas = 0;

Servo miServo;

void setup() {

    pinMode(pinRelayBomb, OUTPUT);
    digitalWrite(pinRelayBomb, LOW);

    pinMode(pinRelayVent, OUTPUT);
    digitalWrite(pinRelayVent, HIGH);

    pinMode(pinRelayLuz, OUTPUT);
    digitalWrite(pinRelayLuz, HIGH);

    pinMode(TRIG, OUTPUT);
    pinMode(ECO,INPUT);


    miServo.attach(pinServos); 
    miServo.write(85);

    Serial.begin(9600);
    dht.begin();
}

void loop() {
    delay(3000);
    StaticJsonDocument<200> docOut;
//--- Lectura del sensor de temperatura y humedad ---
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();


    if (isnan(humidity) || isnan(temperature)){
        //Serial.println(F("Failed to read from DHT sensor!"));
        
    } else {
        docOut["humedadAmbiente"] = humidity;
        docOut["temperatura"] = temperature;

        // Automatizacion de ventilador
        if (temperature > umbralTemp) {
            contadorTempAlta++;
            contadorTempBaja = 0; // se rompe la racha de temperaturas bajas

            if (contadorTempAlta >= 5 && !ventilador) {
                digitalWrite(pinRelayVent, LOW); // enciende ventilador (LOW si el relay es activo en bajo)
                ventilador = true;
            }
        } else {
            contadorTempBaja++;
            contadorTempAlta = 0; // se rompe la racha de temperaturas altas

            if (contadorTempBaja >= 5 && ventilador) {
                digitalWrite(pinRelayVent, HIGH); // apaga ventilador
                ventilador = false;
            }
        }
    }

// --- Lectura del sensor de nivel de agua drenaje---
    int valorAgua = analogRead(waterSensorPin);
    int porcentajeAgua = map(valorAgua, 600,0,100,0);
    docOut["aguaDrenada"] = porcentajeAgua;

    // if (valorAgua < 100) {
    //     Serial.println("Nivel: Bajo");
    // } else if (valorAgua < 300) {
    //     Serial.println("Nivel: Medio");
    // } else {
    //     Serial.println("Nivel: Alto");
    // }
    // Serial.println(" ");

//--- Lectura del sensor de luz ---
    int valorLuz = analogRead(lightSensorPin);
    int porcentajeLuz = map(valorLuz, 60,985,100,0);
    docOut["luzAmbiente"] = porcentajeLuz;

    if (valorLuz < 500){
        miServo.write(0);
    } else {
        miServo.write(85);
    }

//--- Lectura del sensor de humedad de tierra ---
    int valorHumTierra = analogRead(soilSensorPin);
    int porcentajeHumedadTierra = map(valorHumTierra, 400,600,100,0);

    docOut["humedadSuelo"] = porcentajeHumedadTierra;

// --- Lectura del sensor de nivel de agua potable---
    digitalWrite(TRIG, HIGH);
    delay(1);
    digitalWrite(TRIG, LOW);
    DURACION = pulseIn(ECO, HIGH);
    DISTANCIA = DURACION / 58.2;
    DISTANCIA = Tanque - DISTANCIA;

    docOut["aguaPotable"] = DISTANCIA;

    // if (DISTANCIA < 5) {
    //     Serial.println("Nivel: Bajo");
    // } else if (DISTANCIA < 10) {
    //     Serial.println("Nivel: Medio");
    // } else {
    //     Serial.println("Nivel: Alto");
    // }
    docOut["luces"] = luces;
    docOut["ventilador"] = ventilador;
    docOut["tapaSuperior"] = tapaSuperior;
    
    serializeJson(docOut, Serial);
    Serial.println();

        // LEE COMANDOS JSON ENTRANTES
    // if (Serial.available()) {
    //     String entrada = Serial.readStringUntil('\n');
    //     StaticJsonDocument<200> docIn;
    //     DeserializationError error = deserializeJson(docIn, entrada);
        
    //     if (!error) {
    //     if (docIn.containsKey("vent")) {
    //         String estado = docIn["vent"];
    //         if (estado == "on") {
    //         digitalWrite(ledPin, HIGH);
    //         } else if (estado == "off") {
    //         digitalWrite(ledPin, LOW);
    //         }
    //     }
    // } else {
    // // Error de JSON
    // }
}
