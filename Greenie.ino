//Librerias utilizadas
#include "DHT.h"
#include <Servo.h>
#include <ArduinoJson.h>

//Config sensor de Temp y Humedad
#define DHTPIN 7 
#define DHTTYPE DHT11 
DHT dht(DHTPIN, DHTTYPE);

//Pines analogicos
const int waterSensorPin = A0;
const int lightSensorPin = A1;
const int soilSensorPin = A3;

//Pines digitales
const int ECO = 8;
const int TRIG = 9;
const int pinServos = 10;
const int pinRelayBomb = 11;
const int pinRelayVent = 12;
const int pinRelayLuz = 13;

//Variables para el sensor del tanque de agua
int DURACION;
int DISTANCIA;
int Tanque = 22;

//Variables del estado de cada actuador
bool ventilador;
bool tapaSuperior;
bool luces;
bool riego;
bool ventManualControl = false;  // ventilador ** true = modo manual, false = modo automático


//Definicion del Servo
Servo miServo;

void setup() {

//Setup default para los relay
    pinMode(pinRelayBomb, OUTPUT);
    digitalWrite(pinRelayBomb, LOW);

    pinMode(pinRelayVent, OUTPUT);
    digitalWrite(pinRelayVent, HIGH);

    pinMode(pinRelayLuz, OUTPUT);
    digitalWrite(pinRelayLuz, HIGH);

    pinMode(TRIG, OUTPUT);
    pinMode(ECO,INPUT);

    miServo.attach(pinServos); 
    //---  Se cierra la tapa superior por defecto
    for (int pos = 0; pos <= 85; pos += 1) { 
        miServo.write(pos);              
        delay(10);                       
    }

//Default de los activadores
    bool ventilador = false;
    bool tapaSuperior = false;
    bool luces = true;
    bool riego = false;

//Inicio de Serial
    Serial.begin(9600);
    dht.begin();
}

//---  Loop principal del arduino
void loop() {
    //Delay entre lecturas por parte del arduino
    delay(3000);
    StaticJsonDocument<200> docOut; //Preparacion del Json de datos

//--- Lectura del sensor de temperatura y humedad ---
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    if (isnan(humidity) || isnan(temperature)){
        docOut["humedadAmbiente"] = "Error";
        docOut["temperatura"] = "Error";
    } else {
        docOut["humedadAmbiente"] = humidity; //Se agrega el dato de Humedad Ambiente
        docOut["temperatura"] = temperature; //Se agrega el dato de Temperatura Ambiente
    }

// --- Lectura del sensor de nivel de agua drenaje---
    int valorAgua = analogRead(waterSensorPin);
    int porcentajeAgua = map(valorAgua, 600,0,100,0); //Se hace la conversion del dato a porcentaje 600==100% --> 0==0%
    docOut["aguaDrenada"] = porcentajeAgua; //Se agrega el dato de Agua Drenada
//--- Lectura del sensor de luz ---
    int valorLuz = analogRead(lightSensorPin);
    int porcentajeLuz = map(valorLuz, 60,985,100,0); //Se hace la conversion del dato a porcentaje 60==100% --> 985==0%
    docOut["luzAmbiente"] = porcentajeLuz; //Se agrega el dato de Luz

//--- Lectura del sensor de humedad de tierra ---
    int valorHumTierra = analogRead(soilSensorPin);
    int porcentajeHumedadTierra = map(valorHumTierra, 400,600,100,0); //Se hace la conversion del dato a porcentaje 400==100% --> 600==0%
    docOut["humedadSuelo"] = porcentajeHumedadTierra; //Se agrega el dato de Humedad de Suelo

// --- Lectura del sensor de nivel de agua potable---
    digitalWrite(TRIG, HIGH);
    delay(1);
    digitalWrite(TRIG, LOW);
    DURACION = pulseIn(ECO, HIGH);
    DISTANCIA = DURACION / 58.2;
    DISTANCIA = Tanque - DISTANCIA;
    int porcentajeAguaP = map(DISTANCIA,20,0,100,0); //Se hace la conversion del dato a porcentaje 20==100% --> 0==0%
    docOut["aguaPotable"] = porcentajeAguaP;  //Se agrega el dato de Agua Potable



//--- Se agrega el estado actual del invernadero 
    docOut["luces"] = luces;
    docOut["ventilador"] = ventilador;
    docOut["tapaSuperior"] = tapaSuperior;
    docOut["riego"] = riego;    
    docOut["ventManual"] = ventManualControl;


//---  Se envia por el Serial todo el Json
    serializeJson(docOut, Serial);
    Serial.println(); // Linea para separar los mensajes en el serial

    
//--- LEE COMANDOS JSON ENTRANTES
    if (Serial.available()) {
        String jsonStr = Serial.readStringUntil('\n');
        StaticJsonDocument<200> doc;

        DeserializationError error = deserializeJson(doc, jsonStr);

        if (error) {
            return;
        }
        if (doc.containsKey("luces")) {
             bool entrada = doc["luces"];
             if (entrada){
                luces = true;
                digitalWrite(pinRelayLuz, HIGH);
             }else{
                luces = false;
                digitalWrite(pinRelayLuz, LOW);
             } 
        }


// --- Control manual/automático del ventilador ---


        if (doc.containsKey("ventManual")) {
            ventManualControl = doc["ventManual"];
        }

        // --- Control manual del ventilador ---
        if (ventManualControl) {
            if (doc.containsKey("vent")) {
                bool entrada = doc["vent"];
                ventilador = entrada;
                digitalWrite(pinRelayVent, entrada ? LOW : HIGH); // LOW activa el interruptor 
            }
        }

        
        // --- Control automático del ventilador ---
        else {
            if (temperature > 30.0) {
                ventilador = true;
                digitalWrite(pinRelayVent, LOW);
            } else {
                ventilador = false;
                digitalWrite(pinRelayVent, HIGH);
            }
        }


        if (doc.containsKey("techo")) {
             bool entrada = doc["techo"];
             if (entrada){
                tapaSuperior = true;
                luces = false;
                digitalWrite(pinRelayLuz, LOW);
                for (int pos = 85; pos >= 0; pos -= 1) { 
                    miServo.write(pos);              
                    delay(15);                       
                    }
             }else{
                tapaSuperior = false;
                luces = true;
                digitalWrite(pinRelayLuz, HIGH);
                for (int pos = 0; pos <= 85; pos += 1) { 
                    miServo.write(pos);              
                    delay(15);                       
                }
             } 
        }

    }


}   

