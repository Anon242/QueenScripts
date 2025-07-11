# 1 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino"
# 2 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino" 2
# 3 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino" 2


Board queen(6);

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

iarduino_NeoPixel led(A8, 20); //Инициализируем ленту
uint8_t colorR = 0;
uint8_t colorG = 0;
uint8_t colorB = 0;
uint8_t colorNum = 0;
Engine engine = Engine(46,13);

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
  ((queen.getBits(0,1)) ? ((
# 86 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino" 3
 (*(volatile uint8_t *)(0x10B))
# 86 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino"
 ) |= (1UL << (
# 86 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino" 3
 4
# 86 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino"
 ))) : ((
# 86 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino" 3
 (*(volatile uint8_t *)(0x10B))
# 86 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino"
 ) &= ~(1UL << (
# 86 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino" 3
 4
# 86 "C:\\Program Files\\QueenScripts\\inofile\\inofile.ino"
 ))));
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

  for(int i = 0; i < 20; i++){
    led.setColor(i, 0, 0, 0);
  }

  for(int i = 0; i < colorNum; i++){
    led.setColor(i, colorR, colorG, colorB);
  }



  led.write();
}
