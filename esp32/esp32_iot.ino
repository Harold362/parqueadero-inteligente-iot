#include <WiFi.h>
// Librería WiFi del ESP32
// Permite conectar el ESP32 a internet o red local

#include <WebServer.h>
// Librería para crear servidor web interno
// El ESP32 crea una página web local

#include <SPI.h>
// Librería comunicación SPI
// Necesaria para el RFID

#include <MFRC522.h>
// Librería del módulo RFID RC522

// ================= PINES RFID ==================

#define SS_PIN 5
// Pin SDA del RFID conectado al GPIO 5

#define RST_PIN 22
// Pin RST del RFID conectado al GPIO 22

MFRC522 rfid(SS_PIN, RST_PIN);
// Crea objeto RFID

// ================= WIFI ==================

// NOMBRE DEL HOTSPOT O WIFI
const char* ssid = "Moto50fusion";

// CONTRASEÑA DEL WIFI
const char* password = "contraseña";

/*
PARA CAMBIAR A OTRO CELULAR:

const char* ssid = "SamsungJuan";
const char* password = "12345678";

SOLO SE MODIFICAN ESTAS DOS LINEAS
*/

// ================= SERVIDOR WEB ==================

WebServer server(80);
// Crea servidor web puerto 80

/*
Puerto 80 = páginas web normales
*/

// ================= RFID ==================

String tarjetaValida = "AD698F21";
// UID autorizado de la tarjeta RFID

// ================= VARIABLES WEB ==================

String estadoLibres = "M1,M2,M3,M4,M5,M6";
// Guarda módulos libres

String estadoMalParqueo = "NO";
// Guarda estado mal parqueo

String ultimaTarjeta = "NINGUNA";
// Guarda último usuario RFID

String horaAcceso = "--";
// Guarda hora del último acceso

// ================= LEDS ==================

int ledRojo = 25;
// LED rojo mal parqueo

int ledVerde = 26;
// LED verde zonas libres

int ledAmarillo = 4;
// LED amarillo acceso RFID

// ================= PAGINA WEB ==================

void pagina() {

  // Crea contenido HTML
  String html = "<html><head><meta charset='UTF-8'>";

  // Refresca página cada 2 segundos
  html += "<meta http-equiv='refresh' content='2'>";

  // Título navegador
  html += "<title>Parqueadero</title></head><body>";

  // Título principal
  html += "<h2>PARQUEADERO INTELIGENTE</h2>";

  // Mostrar módulos libres
  html += "<p><b>Libres:</b> " + estadoLibres + "</p>";

  // Mostrar mal parqueo
  html += "<p><b>Mal parqueo:</b> " + estadoMalParqueo + "</p>";

  // Mostrar último RFID
  html += "<p><b>RFID:</b> " + ultimaTarjeta + "</p>";

  // Mostrar tiempo acceso
  html += "<p><b>Hora:</b> " + horaAcceso + "</p>";

  // Cierra HTML
  html += "</body></html>";

  // Envía página al navegador
  server.send(200, "text/html", html);
}

// ================= SETUP ==================

void setup() {

  // Inicia puerto serial
  Serial.begin(115200);

  // Inicia SPI RFID
  SPI.begin(18,19,23,5);

  // Inicializa RFID
  rfid.PCD_Init();

  // Configura LEDs salida
  pinMode(ledRojo, OUTPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledAmarillo, OUTPUT);

  // Estados iniciales LEDs
  digitalWrite(ledRojo, LOW);
  digitalWrite(ledVerde, HIGH);
  digitalWrite(ledAmarillo, LOW);

  // ================= WIFI ==================

  // Conecta ESP32 al WiFi
  WiFi.begin(ssid, password);

  // Espera conexión WiFi
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);while(WiFi.status() != WL_CONNECTED) {

  Serial.println("Conectando WiFi...");

  delay(1000);
    }
  }

  /*
  Cuando conecta:
  El hotspot o router le asigna automáticamente una IP
  */

  // Página principal "/"
  server.on("/", pagina);

  // Inicia servidor web
  server.begin();

  // Muestra IP en monitor serial
  Serial.println(WiFi.localIP());

  /*
  Esa IP es la que abres desde:
  celular
  computador
  navegador

  Ejemplo:
  http://10.66.128.18
  */
}

// ================= LOOP ==================

void loop() {

  // Atiende clientes web
  server.handleClient();

  // ================= DATOS PYTHON ==================

  if(Serial.available()) {

    // Lee mensaje serial
    String dato = Serial.readStringUntil('\n');

    // Limpia espacios
    dato.trim();

    // ================= MAL PARQUEO ==================

    if(dato == "ROJO_ON") {

      digitalWrite(ledRojo, HIGH);

      estadoMalParqueo = "SI";
    }

    else if(dato == "ROJO_OFF") {

      digitalWrite(ledRojo, LOW);

      estadoMalParqueo = "NO";
    }

    // ================= ZONAS LIBRES ==================

    else if(dato == "VERDE_ON") {

      digitalWrite(ledVerde, HIGH);
    }

    else if(dato == "VERDE_OFF") {

      digitalWrite(ledVerde, LOW);
    }

    // ================= MODULOS LIBRES ==================

    else if(dato.startsWith("LIBRES:")) {

      // Guarda módulos libres enviados por Python
      estadoLibres = dato.substring(7);
    }
  }

  // ================= RFID ==================

  // Espera tarjeta RFID
  if (!rfid.PICC_IsNewCardPresent()) return;

  // Lee tarjeta
  if (!rfid.PICC_ReadCardSerial()) return;

  String uid = "";

  // Convierte UID a texto
  for (byte i = 0; i < rfid.uid.size; i++) {

    uid += String(rfid.uid.uidByte[i], HEX);
  }

  // Convierte mayúsculas
  uid.toUpperCase();

  // Envía UID a Python
  Serial.println(uid);

  // ================= TARJETA AUTORIZADA ==================

  if(uid == tarjetaValida) {

    // Guarda nombre usuario
    ultimaTarjeta = "ING HAROLD";

    // Guarda tiempo desde encendido
    horaAcceso = String(millis()/1000) + " seg";

    // Enciende LED amarillo
    digitalWrite(ledAmarillo, HIGH);

    delay(1500);

    digitalWrite(ledAmarillo, LOW);
  }

  delay(300);
}
