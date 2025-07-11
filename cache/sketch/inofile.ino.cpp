#include <Arduino.h>
#line 1 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino"
#include <QueenUnisense3v1.h>
#include <iarduino_NeoPixel.h>

#define DEVICE_ID 6
Board queen(DEVICE_ID);

//=================================================================================== 
//      Filename  : QueenUnisense3v1
//      Author    : MeGum
//      Github    : https://github.com/Anon242/QueenKit
//      Created   : 2025-07-10 13:45:09
//      Version   : 1.0
//      Notes     : 
//                : адреска и analog in
//=================================================================================== 

class Engine{
  public:
  // Принимаю ЦИФРОВЫЕ АРДУИНОВСКИЕ пины, управляю АРДУИНОВСКИМИ МЕТОДАМИ
  Engine(uint8_t _pinNumGround, uint8_t _pinNumPlus){
    pinNumGround = _pinNumGround;
    pinNumPlus =_pinNumPlus;
  }
  // Сколько на открытие/закрытие в ms
  const int timeMs = 3000;
  // Ардуиновские пины
  uint8_t pinNumGround , pinNumPlus;
  bool isOpened = false;
  bool onMove = false;

  //long ms;
  //long oldMs;

  void open(){
    if(isOpened)
      return;
    onMove = true;
    digitalWrite(pinNumGround,1);
    digitalWrite(pinNumPlus,0);
    delay(timeMs);
    digitalWrite(pinNumGround,0);
    digitalWrite(pinNumPlus,0);

    isOpened = true;
    onMove = false;
  }
  void close(){
    if(!isOpened)
      return;
    onMove = true;
    digitalWrite(pinNumGround,0);
    digitalWrite(pinNumPlus,1);
    delay(timeMs);
    digitalWrite(pinNumGround,0);
    digitalWrite(pinNumPlus,0);

    isOpened = false;
    onMove = false;
  }
};

// !!!!!!!!
#define LEDCOUNT 20
iarduino_NeoPixel led(A8, LEDCOUNT); //Инициализируем ленту
uint8_t colorR = 0;
uint8_t colorG = 0;
uint8_t colorB = 0;
uint8_t colorNum = 0;
Engine engine = Engine(46,13);

#line 71 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino"
void setup();
#line 79 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino"
void loop();
#line 84 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino"
void onMessage();
#line 71 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino"
void setup() 
{ 
  queen.init(onMessage); 
  led.begin();
  delay(300);
  engine.open();
}

void loop() 
{ 
  queen.loop(); 
}

void onMessage() 
{  
  bitWrite(PORTL,PL4,queen.getBits(0,1));
  // Получаем буфер ADC
  uint16_t *adcBuffer = queen.inADC();
  for (uint8_t i = 0; i < 16; i++) {
    uint8_t bitIndex = 16 + 10 * i;
    // Назначаем PWM из шины
    //queen.pwmOuts(queen.getBits(bitIndex, 10), i + 1);
    // Отправляем данные ADC в шину
    queen.setBits(bitIndex, 10, adcBuffer[i]);
  }
  // Отправляем цифровые пины в шину
  queen.setBits(0, 16, queen.in());
  colorR = queen.getBits(192,10);
  colorG = queen.getBits(202,10);
  colorB = queen.getBits(212,10);

  colorNum = queen.getBits(222,10);

  for(int i = 0; i < LEDCOUNT; i++){
    led.setColor(i, 0, 0, 0); 
  }

  for(int i = 0; i < colorNum; i++){
    led.setColor(i, colorR, colorG, colorB); 
  }



  led.write();
}

