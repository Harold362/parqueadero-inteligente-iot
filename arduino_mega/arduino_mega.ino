#include <Servo.h>
// Librería para controlar servomotores

#include <LiquidCrystal.h>
// Librería para pantalla LCD 16x2

// ================= LCD ==================

LiquidCrystal lcd(7,8,9,10,11,12);

/*
Conexiones LCD:

RS -> pin 7
E  -> pin 8
D4 -> pin 9
D5 -> pin 10
D6 -> pin 11
D7 -> pin 12
*/

// ================= SERVOS ==================

Servo servoEntrada;
// Objeto servo entrada

Servo servoSalida;
// Objeto servo salida

int pinServoEntrada = 6;
// Pin servo entrada

int pinServoSalida  = 5;
// Pin servo salida

// ================= SENSORES IR ==================

int irEntrada = 2;
// Sensor IR entrada

int irSalida  = 3;
// Sensor IR salida

// ================= VARIABLES ==================

bool parqueaderoLleno = false;
// Guarda si el parqueadero está lleno

String dato = "";
// Guarda datos recibidos desde Python

unsigned long ultimoEntrada = 0;
// Guarda último tiempo apertura entrada

unsigned long ultimoSalida = 0;
// Guarda último tiempo apertura salida

// ================= SETUP ==================

void setup() {

  // Inicia comunicación serial
  Serial.begin(9600);

  /*
  Comunicación con Python:

  Python -> Arduino Mega
  */

  // Conecta servo entrada
  servoEntrada.attach(pinServoEntrada);

  // Conecta servo salida
  servoSalida.attach(pinServoSalida);

  // Posición inicial servos
  servoEntrada.write(0);
  servoSalida.write(0);

  /*
  0 grados = barrera cerrada
  */

  // Configura sensores IR
  pinMode(irEntrada, INPUT);
  pinMode(irSalida, INPUT);

  // Inicia LCD 16 columnas x 2 filas
  lcd.begin(16,2);

  // Limpia pantalla
  lcd.clear();



lcd.setCursor(0,0);
lcd.print("PARQUEADERO");

lcd.setCursor(0,1);
lcd.print("INTELIGENTE");

delay(2500);

lcd.clear();

lcd.setCursor(0,0);
lcd.print("HECHO POR:");

lcd.setCursor(0,1);
lcd.print("ING HAROLD CORREA");

delay(3000);

lcd.clear();
}

// ================= LOOP PRINCIPAL ==================

void loop() {

  // ================= DATOS SERIAL ==================

  while(Serial.available()) {

    // Lee datos desde Python
    dato = Serial.readStringUntil('\n');

    // Elimina espacios y saltos línea
    dato.trim();

    // ================= PARQUEADERO LLENO ==================

    if(dato == "LLENO") {

      parqueaderoLleno = true;
    }

    // ================= RFID AUTORIZADO ==================

    else if(dato == "YESID") {

      // Limpia LCD
      lcd.clear();

      // Mensaje bienvenida
      lcd.setCursor(0,0);
      lcd.print("BIENVENIDO");

      lcd.setCursor(0,1);
      lcd.print("HAROLD");

      /*
      Cuando RFID válido:
      abre barrera entrada
      */

      servoEntrada.write(90);

      delay(3000);

      servoEntrada.write(0);

      // Espera visual mensaje
      delay(2000);

      // Limpia pantalla
      lcd.clear();

      // Mostrar módulo asignado
      lcd.setCursor(0,0);
      lcd.print("SU MODULO");

      lcd.setCursor(0,1);
      lcd.print("ES M1");

      delay(3000);
    }

    // ================= MODULOS LIBRES ==================

    else {

      // Ya no está lleno
      parqueaderoLleno = false;

      // Limpia LCD
      lcd.clear();

      // Título
      lcd.setCursor(0,0);
      lcd.print("LIBRES:");

      // Mostrar módulos enviados desde Python
      lcd.setCursor(0,1);
      lcd.print(dato);

      /*
      Ejemplo:

      M1,M4,M6
      */
    }
  }

  // ================= MENSAJE LLENO ==================

  if(parqueaderoLleno) {

    lcd.clear();

    lcd.setCursor(0,0);
    lcd.print("NO HAY ZONAS");

    lcd.setCursor(0,1);
    lcd.print("LIBRES");
  }

  // ================= ENTRADA ==================

  /*
  Si sensor IR detecta vehículo
  */

  if(digitalRead(irEntrada) == LOW &&
     millis() - ultimoEntrada > 5000) {

      /*
      LOW = detectó objeto
      */

      // Solo abrir si NO está lleno
      if(!parqueaderoLleno) {

        // Guarda tiempo actual
        ultimoEntrada = millis();

        // Abre barrera
        servoEntrada.write(90);

        delay(3000);

        // Cierra barrera
        servoEntrada.write(0);
      }
  }

  // ================= SALIDA ==================

  if(digitalRead(irSalida) == LOW &&
     millis() - ultimoSalida > 5000) {

      // Guarda tiempo
      ultimoSalida = millis();

      // Abre salida
      servoSalida.write(90);

      delay(3000);

      // Cierra salida
      servoSalida.write(0);
  }

  // Pequeña pausa estabilidad
  delay(200);
}
