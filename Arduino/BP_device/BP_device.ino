/** 
 * Communicate with Android device
 */

// Libary to use digital pins as RX and TX.
#include <SoftwareSerial.h>
SoftwareSerial mySerial(2, 3); // RX, TX

void setup() {
  mySerial.begin(9600);
  Serial.begin(9600);

  sendCommand("AT");
  sendCommand("AT+ADDR?");
  sendCommand("AT+UUID0xAAA0");
  sendCommand("AT+NAMEBloodPressure");
  sendCommand("AT+ROLE?");
  sendCommand("AT+ROLE0");
  sendCommand("AT+TYPE0");
  sendCommand("AT+PIO1?");
  sendCommand("AT+UUID?");
  //sendCommand("AT+PASS?");
}

void sendCommand(const char * command){
  Serial.print("Command send :");
  Serial.println(command);
  mySerial.println(command);
  //wait some time
  delay(100);
  
  char reply[100];
  int i = 0;
  while (mySerial.available()) {
    reply[i] = mySerial.read();
    i += 1;
  }
  //end the string
  reply[i] = '\0';
  Serial.print(reply);
  Serial.println("Reply end");
}

void communication(int int_data){
  char reply[50];
  int i = 0;
  while (mySerial.available()) {
    reply[i] = mySerial.read();
    i += 1;
  }
  //end the string
  reply[i] = '\0';
  if(strlen(reply) > 0){
    Serial.println(reply);
    
    if(reply[0] == 'A'){
      Serial.println("Equal!");
      String String_data = String(int_data);
      mySerial.print(String_data);
      Serial.println(String_data);
    }
  }


    
}

void loop() {
  int data = random(94,200);
  communication(data);
  delay(500);
}
