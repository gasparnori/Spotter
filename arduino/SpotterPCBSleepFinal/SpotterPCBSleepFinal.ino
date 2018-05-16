/*
  Arduino Mega/Python interface for Spotter with the use of the MC v1.1 board

  The Arduino has two states:
  1. sleeping
    if the input on pin 2 is low (S1/S2 or both are turned off), the Arduino goes into sleep mode (calls sleepNow function, powerPin is low)
    All I/O outputs are powered down
    SPI communication is turned off
    Serial communication is turned off    -->to be improved: making Spotter see it, as if the device was disconnected
    waiting for a rising edge interrupt on pin 2

  2. Awake
    The Arduino waits for a handshake command.
     Once received, it will continually check the sensors and
     report their values via Serial port. --> this function is not necessary in our usage, it just returns 0's
     At the same time incoming commands and data will be written to:
     -> 4 digital ports
     -> 4 DAC's via SPI

  Created 18 January 2013 by Ronny Eichler

  Updated 08 October 2017 by Nora Gaspar

*/

//#define DEBUG
#define DAC_TEST_DELAY 20

//maximum number that the DAC can output
#define DACMAX 4095

#ifdef DEBUG
#define DEBUGLN(x)  Serial.println(x)
#define DEBUG(x)  Serial.print(x)
#else
#define DEBUGLN(x)
#define DEBUG(x)
#endif

#include "SPI.h" // handles SPI communication to MCP4921 DAC
#include <avr/sleep.h> //puts the device to sleep mode

// SPI pins: hardware SPI on the Arduino Mega (so the pins can't be changed!)
#define pin_SCK 52 //clock signal
#define pin_MOSI 51 //data from Arduino to the DAC's

// SPI clients
#define SPI_N_DEVS 4 // number of SPI clients
#define LED_TIMEOUT 100 //this is how long it waits after a command from Spotter before the indicator LED turns off
byte SPI_pins[SPI_N_DEVS] = {37, 38, 39, 40};
byte LEDS[SPI_N_DEVS] = {29, 28, 30, 31}; //indicator LED's on the MC box front panel
int LEDtimeouts[SPI_N_DEVS] = {LED_TIMEOUT, LED_TIMEOUT, LED_TIMEOUT, LED_TIMEOUT}; //separate counter for each LED

#define SCALE_FACTOR (4096/640) //the coordinates from Spotter need to be multiplied by a scale factor before sent out to the DAC
int scaledData = 0; //the maximum received number is 639, the max output is 4095  -->scale by six

//Power saver mode pins
#define sleepPin 2
#define powerPin 3
bool sleepstate = true;


// digital output pins: Regions of interest
#define DOUT_N 4
byte DOUT_pins[DOUT_N] = {45, 46, 47, 48};

//these variables are kept from the original code. They are used for interpreting commands from Spotter
#define CMDADDR 0x07 // bits 1-3
#define CMDTYPE 0x38 // bits 4-6
#define CMDMSBB 0xC0 // bits 7-8

#define TYPE_UTILITY 0x00 //command types from serial
#define TYPE_SPI_DAC 0x01
#define TYPE_DIGITAL 0x02

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
//Nora's changes: added the indicator LED's and their timer's
void setDAC(byte pin_idx, int outputValue) {
  // check if device index in range
  if (pin_idx >= SPI_N_DEVS) {
    return;
  }
  byte pin = SPI_pins[pin_idx];
  // select SPI device
  digitalWrite(pin, LOW);
  // command bits and 4 MSB data bits
  data = highByte(outputValue);
  data = 0b00001111 & data;
  data = 0b00110000 | data;
  SPI.transfer(data);
  // last 8 LSB data bits
  data = lowByte(outputValue);
  SPI.transfer(data);
  // deselect SPI device
  digitalWrite(pin, HIGH);

  //reset the indicator LED's counter, and turns it on
  LEDtimeouts[pin_idx] = LED_TIMEOUT;
  digitalWrite(LEDS[pin_idx], HIGH);

}

//Nora's changes: this function was left unchanged
/*
  Read digital pins, e.g. sensors
  Loop through digital pins, return
  byte whose LSB bits represent the state of
  a specific pin.
*/
byte readSensors() {
  return 0x00;
}


//Nora's changes: this function was left unchanged
/*
  Set digital pins to the value of their specific bit
  in the received state byte
*/
void setDigital(byte pin_idx, short outputValue) {
  // check if device index in range
  if (pin_idx >= DOUT_N) {
    return;
  }
  byte pin = DOUT_pins[pin_idx];
  if (outputValue > 0) {
    digitalWrite(pin, HIGH);
  }
  else {
    digitalWrite(pin, LOW);
  }
}


/*
  Report arduino capabilities to Spotter. I.e. give number
  of analog out, digital out pins.
*/
//Nora's changes: this function was left unchanged
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
//Nora's changes: added the scaling factor
void interpretCommand() {
  if (inBytes[3] != '\n') {
    return;
  }
  inData = (inBytes[2] << 8) + inBytes[1];
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
      //////////////// TO GO BACK TO THE PWM SIGNAL, COMMENT THE LINES WITH //////s
      ////////////////for (byte i=0; i<3; i++) {
      scaledData = inData * SCALE_FACTOR;
      setDAC(addr, scaledData);
      ////////////////    delay(1);
      // setDAC(addr, 0);
      //  delay(1);////////////////
      //  }////////////////
      break;
    case TYPE_DIGITAL:
      setDigital(addr, inData);
      break;
  }
  //  Serial.println(readSensors());
}

/*initialization function, to set every IO pin, and
  every communication channel into active state after reset or after waking up*/
//Nora's function
void initPins() {
  // sleep flag turn to false
  sleepstate = false;
  // initialize serial connection
  Serial.begin(115200);
  // power pin turns on
  digitalWrite(powerPin, digitalRead(sleepPin));
  
  //initialize SPI to talk to DAC
  for (byte i = 0; i < SPI_N_DEVS; i++) {
    //active low chip select pins are turned to HIGH
    digitalWrite(SPI_pins[i], HIGH); 
    //LEDS are turned on for a test (will flash)
    digitalWrite(LEDS[i], HIGH);
  }
  //initialize SPI connection
  SPI.begin();
  SPI.setBitOrder(MSBFIRST);

  // DAC test pulses
  for (byte i = 0; i < SPI_N_DEVS; i++) {
    setDAC(i, DACMAX);
    delay(DAC_TEST_DELAY);
    setDAC(i, 0);
  }

  // initialize digital output pins
  for (byte i = 0; i < DOUT_N; i++) {
    digitalWrite(DOUT_pins[i], LOW);
  }
}
void setup() {
  // attaching interrupt to interrupt 0 on the Arduino (pin 2). It will call the wakeUpNow function when detects a rising edge
  attachInterrupt(digitalPinToInterrupt(sleepPin), wakeUpNow, RISING);
  sleepstate = false;
  //input for the interrupt
  pinMode(sleepPin, INPUT);
  //sleep state indicator LED
  pinMode(powerPin, OUTPUT);
  // initializing the four SPI CS pins, and the four indicator LEDs
  for (byte i = 0; i < SPI_N_DEVS; i++) {
    pinMode(SPI_pins[i], OUTPUT);
    pinMode(LEDS[i], OUTPUT);
  }
  //initializing the digital output pins
  for (byte i = 0; i < DOUT_N; i++) {
    pinMode(DOUT_pins[i], OUTPUT);
  }
  
  initPins();
}

/*
  Called when serial data available after each loop()
  Requires use of non-blocking timings for opening outputs,
  otherwise delayed and buffers might fill up

  Current protocol is defined as one command byte, followed
  by two data bytes and closed with a newline.
*/
//Nora's changes: this function was left unchanged
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

void setLEDs() {
  for (int i = 0; i < SPI_N_DEVS; i++) {
    if (LEDtimeouts[i] > 0) {
      LEDtimeouts[i]--;
    }
    else {
      digitalWrite(LEDS[i], LOW);
    }
  }
}

// interrupt routine. Must be very short (if want to change something, change it in the called function, and not here)
void wakeUpNow() {
  if (sleepstate == true) {
    initPins();
  }
}

void sleepNow() {
  if (sleepstate == false) {
    sleepstate = true;

    attachInterrupt(digitalPinToInterrupt(sleepPin), wakeUpNow, RISING); //interrupt reattached here
    set_sleep_mode(SLEEP_MODE_IDLE);   // sleep mode is set here
    cli();
    sleep_enable();
    sei(); //enabling all the interrupts
    /////////////////////////power down USB///////////////////////////////
    Serial.end();
    /////////////////////////power down SPI///////////////////////////////
    SPI.end();
    //////////////////power down all IO outputs///////////////////////////
    for (byte i = 0; i < SPI_N_DEVS; i++) {
      digitalWrite(SPI_pins[i], LOW);
      digitalWrite(LEDS[i], LOW);
    }

    for (byte i = 0; i < DOUT_N; i++) {
      digitalWrite(DOUT_pins[i], LOW);
    }
    digitalWrite(powerPin, LOW);



    sleep_cpu();   //actually puts the device to sleep here
    sleep_disable(); //returns here after the interrupt
    
    //  detachInterrupt(digitalPinToInterrupt(sleepPin));
  }

}
void setAllDAC(int num){
  scaledData = num * SCALE_FACTOR;
  setDAC(0, scaledData);
  setDAC(1, scaledData);
  setDAC(2, scaledData);
  setDAC(3, scaledData);
 }

 void testDAC(){
    setDigital(0, HIGH);
    delay(100);
    setDigital(0, LOW);
     for (int i=0; i<63; i++){
      setAllDAC(i);
      delay(5000);
    }
    setAllDAC(639);
    delay(5000);
    setDigital(0, HIGH);
    
  }
 
void loop() {
  if (digitalRead(sleepPin) == LOW) { //if S2 or S1 switches are turned down
    sleepNow();
  }
  else {
    
    //testDAC();
  
 
    digitalWrite(powerPin, digitalRead(sleepPin));  //turns the power pin up
    setLEDs();    //indicator LED control
    delay(1);
 }


}

