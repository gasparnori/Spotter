
//the framesize is 360*640, the DAC max is 4095
#define DAC_TEST_DELAY 20
#define DACMAX 4095

#define DEBUGLN(x)
#define DEBUG(x)


#include "SPI.h" // handles SPI communication to MCP4921 DAC

  // SPI pins
  #define pin_SCK 13
  #define pin_MOSI 11
  #define pin_MISO 12
  // SPI clients
  #define SPI_N_DEVS 2 // number of SPI clients
  byte SPI_pins[SPI_N_DEVS] = {6, 7};
  // digital input pins
  #define DIN_N 2
  byte DIN_pins[DIN_N] = {8, 9};
  // digital output pins
  #define DOUT_N 4
  byte DOUT_pins[DOUT_N] = {2, 3, 4, 5};


#define CMDADDR 0x07 // bits 1-3 00000111
#define CMDTYPE 0x38 // bits 4-6 00111000
#define CMDMSBB 0xC0 // bits 7-8 11000000

#define TYPE_UTILITY 0x00
#define TYPE_SPI_DAC 0x01
#define TYPE_DIGITAL 0x02

#define SCALE_FACTOR (4096/640)
int scaledData=0; //the maximum received number is 639, the max output is 4095  -->scale by six

int inData = 0;
byte outData = 0;

int tmp = 0x00;
byte inBytes[4];

byte data = 0x00;
//byte n = 0;


/* 
 Transfer 4 command bits and 12 data bits
 via SPI to the DACs
 */
void setDAC(byte pin_idx, int outputValue) {
  // check if device index in range
  if (pin_idx >= SPI_N_DEVS) {
    return;
  }
  byte pin = SPI_pins[pin_idx];
  // command bits and 4 MSB data bits
  // data = highByte(outputValue);
  data = 0b00001111 &  highByte(outputValue);
  data = 0b00110000 | data;
  
  // select SPI device
  digitalWrite(pin, LOW);
  SPI.transfer(data);
  // last 8 LSB data bits
  SPI.transfer(lowByte(outputValue));
  // deselect SPI device
  digitalWrite(pin, HIGH);
}


/*
Report arduino capabilities to Spotter. I.e. give number
 of analog out, digital out pins.
 */
void report(byte request, short inputValue) {
  switch (request) {
    case 0x00:
      Serial.println(inputValue, DEC);
      break;
    case 0x01:
      Serial.println(SPI_N_DEVS, DEC);
      break;
    case 0x02:
      Serial.println(DOUT_N, DEC);
      break;
  }
}


/*
Interpret the received byte array by splitting it into a command, followed
 by payload data used in its execution
 */
void interpretCommand() {
  //checks whetever it's a new line
  if (inBytes[3] != '\n') {
    return;
  }
  //creating 16 bits of input data
  inData = (inBytes[2]<<8) + inBytes[1];
  if (inData > DACMAX) {
    inData = DACMAX;
  }
  byte addr = (CMDADDR & inBytes[0]);
  byte type = (CMDTYPE & inBytes[0]) >> 3;
  DEBUGLN(type);
  DEBUGLN(addr);
  DEBUGLN(inData);

  switch (type) {
  case TYPE_UTILITY: 
    report(addr, inData);
    break;
  case TYPE_SPI_DAC:
     scaledData=inData*SCALE_FACTOR;
     setDAC(addr, scaledData);
    break;
  case TYPE_DIGITAL:
    break;
  }
//  Serial.println(readSensors());
}


void setup(){
  // initialize serial connection
  Serial.begin(57600);

  // ready SPI to talk to DAC
  for (byte i = 0; i < SPI_N_DEVS; i++) {
    pinMode(SPI_pins[i], OUTPUT);
    digitalWrite(SPI_pins[i], HIGH);
  }
  SPI.begin();
  SPI.setBitOrder(MSBFIRST);

  // DAC test pulses
  for (byte i = 0; i < SPI_N_DEVS; i++) {
    setDAC(i, DACMAX);
    delay(DAC_TEST_DELAY);
    setDAC(i, 0);
    delay(100);
  }

}

/*
Called when serial data available after each loop()
 Requires use of non-blocking timings for opening outputs,
 otherwise delayed and buffers might fill up
 
 Current protocol is defined as one command byte, followed
 by two data bytes and closed with a newline.
 */
void serialEvent() {
  while (Serial.available()) {
    byte n = 0;
    while (n < 4) {
      // get the new byte:
      tmp = Serial.read();
      if (tmp > -1) {
        inBytes[n] = tmp;
        n++;
      }
    }
    interpretCommand();
  }
}


void loop() {
  delay(1);
}

