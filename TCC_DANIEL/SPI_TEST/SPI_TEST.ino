#include "eit.h"


/*
 * Código de comunicação e comutação entre eletrodos utilizando SPI
 * 
 * MISO -> nativo do arduino due
 * MOSI -> Nativo do arduino due
 * SCK -> nativo do arduino due
 * SS -> pino 10 do arduino due
 * 
*/


//~---------------------------Definições----------------------------

#define dataOk 3

int stepPin = 3;

int initPin = 23;

int finalPin = 53;

int tensao = 0;


//-----------------Definirescolpo de funções----------

//config


//func
void configPinDigital(int inicialPin = 0,int finalPin = 0, int stepPin = 0, bool mode = false);
void digitalWritePinEIT();
byte find_Action(byte receive);
byte interpretAction(byte action,int receive);
int tens();


//convert
int convertHexToInt();
String ValueIntVectByte();



//_________________variaveis globais__________________

bool flag=false;
bool flagDataConplete = false;

uint16_t DataReceived;

uint16_t data;

uint16_t eletrodoEmissor;
uint16_t eletrodoLeitor;

enum NexAction {SetZero,SetWriteEIT,SetReadEIT,SetReLoadRasberry};

byte DataReceivedIndex = 0;

eit_eletrodo eletrodos(23,53,2);

void setup() {
  Serial.begin(9600);
  while(!Serial);
  //SPI serial recieve
  REG_PMC_PCER0 |= PMC_PCER0_PID24;   // Power up SPI clock
  REG_SPI0_WPMR = 0<<SPI_WPMR_WPEN;   //Unlock user interface for SPI
  
  //Instance SPI0, MISO: PA25, (MISO), MOSI: PA26, (MOSI), SCLK: PA27, (SCLK), NSS: PA28, (NPCS0)
  REG_PIOA_ABSR &= ~PIO_ABSR_P25;     // Transfer Pin control from PIO to SPI
  REG_PIOA_PDR |= PIO_PDR_P25;      // disable pio to control this pin (MISO)
  
  REG_PIOA_ABSR &= ~PIO_ABSR_P26;     // Transfer Pin control from PIO to SPI
  REG_PIOA_PDR |= PIO_PDR_P26;      // disable pio to control this pin (MOSI)
  
  REG_PIOA_ABSR &= ~PIO_ABSR_P27;     // Transfer Pin control from PIO to SPI
  REG_PIOA_PDR |= PIO_PDR_P27;      // disable pio to control this pin (SCLK)
  
  REG_PIOA_ABSR &= ~PIO_ABSR_P28;     // Transfer Pin control from PIO to SPI
  REG_PIOA_PDR |= PIO_PDR_P28;      //disable pio to control this pin (NSS)

  REG_SPI0_CR = 1;            // Enable SPI
  REG_SPI0_MR = 0;            // Slave mode
  
  SPI0->SPI_IER = SPI_IER_RDRF;     // Receive Data Register Full Interrupt
  NVIC_EnableIRQ(SPI0_IRQn);
  
  SPI0->SPI_CSR[0] = SPI_CSR_NCPHA|SPI_CSR_BITS_8_BIT;  // Shift on falling edge and transfer 8 bits. SPI_CSR_BITS_16_BIT  SPI_CSR_BITS_8_BIT 
  pinMode(3,INPUT); // Seta o pino 3 como sendo o chip select do SPI
  
  Serial.println("START");


}



bool flagData = false;
bool flagReturn = false;
bool flagEletrodoCorrente = false;
bool flagEletrodoLeitorTensao = false;
bool flagExecutar = false;
bool flagReturnValueEletrodoTense = false;
bool flagReturnValueEletrodoCorrent = false;
bool flagReturnValueEletrodotens = false;
bool leituraAnalogica = false;
bool flagEnvioDeDadosOk = false;
bool flagEnvioDeDados = false;
bool flagAtivarLeituras = false;
bool flagParteDoDado = false;
bool flagReceberEletrodoTensao = false;

byte contador = 0;

int emissor;

byte action = 0; //Selecção de qual comanda sera executado na proximo envio ou leitura;



void SPI0_Handler()
{
  uint32_t status = SPI0->SPI_SR;

 
  if (status & SPI_SR_RDRF & !flagParteDoDado){
    
    DataReceived = SPI0->SPI_RDR & SPI_RDR_RD_Msk;

    if(DataReceived){
  
      if(flagEletrodoCorrente){
        setWritePins(DataReceived);
        flagEletrodoCorrente = false;
      }
      else if(flagReceberEletrodoTensao){
        setReadTens(DataReceived);
        flagReceberEletrodoTensao = false;
      }
      else if(DataReceived == 0x11 & !flagEletrodoCorrente){
        
        flagEletrodoCorrente = true;
      }
      else if(DataReceived == 0x22 & !flagReceberEletrodoTensao){
        flagReceberEletrodoTensao = true;
      }
      else if(DataReceived == 0x33){
        flagReturn = true;
      }
      else if(DataReceived == 0x44){
        flagReturnValueEletrodoCorrent = true;
      }
      else if(DataReceived == 0x55){
        flagReturnValueEletrodotens  = true;
      }
      else if(DataReceived == 0xAA){
        leituraAnalogica = true;
      }
      else if(DataReceived == 0xCC){
        flagEnvioDeDadosOk = true;
      }
      else if(DataReceived == 0xEE){
         flagAtivarLeituras = true;
      }
      else if(DataReceived == 0X99){
        flagParteDoDado = true;
      }
      else if(DataReceived){
        data = DataReceived;
      }
    }
  
  }
  if (status & SPI_SR_TDRE){

    if(flagReturn){
     SPI0->SPI_TDR = data  & SPI_RDR_RD_Msk;
     flagReturn = false;
     }
    else if(flagReturnValueEletrodoCorrent){
      SPI0->SPI_TDR = eletrodos.getValorEmissorCorrente();
      flagReturnValueEletrodoCorrent = false;
    }
    else if(flagReturnValueEletrodotens){
      SPI0->SPI_TDR = eletrodos.getValorLeituraTens();
      flagReturnValueEletrodotens = false;
    }
    else if(flagEnvioDeDadosOk){
      if(flagEnvioDeDados){
        SPI0->SPI_TDR = 0xDD;
      }
      else{
        SPI0->SPI_TDR = 0xBB;
      }
      flagEnvioDeDadosOk = false;
    }
    else if (flagParteDoDado){
      if(contador == 0){
        SPI0->SPI_TDR = tensao & 0b0000000011111111;

        contador++;
      }
      else if(contador == 1){
        SPI0->SPI_TDR = tensao >> 8;
        contador++;
      }
      else if(contador == 2){
      contador = 0;
      tensao = 0;
      flagParteDoDado = false;
      flagEnvioDeDados = false;
      }
      
    }
   }


}

byte indice = 0;

void loop() {

  if(leituraAnalogica & !flagEnvioDeDados){
    eletrodos.writeData();
        
    delayMicroseconds(500);
    analogReadResolution(12);
    for(int p = 0; p<100;p++){
      tensao = tensao + analogRead(5);
      Serial.println(tensao);
      }
      
    tensao = tensao/100;
    delayMicroseconds(200);
    flagEnvioDeDados = true;
    leituraAnalogica = false;
    }
   
}


//----------- funções ---------

void setWritePins(int WritePins){
  eletrodos.setEmissorCorrente(WritePins);
}

void setReadTens(int WritePins){
  eletrodos.setLeituraTens(WritePins);
}
