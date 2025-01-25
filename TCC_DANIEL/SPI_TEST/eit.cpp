
#include "Arduino.h"
#include "eit.h"

eit_eletrodo::eit_eletrodo(int pinInit,int pinFinal,int stepPin)
{
  // define os pinos de saída do arduino due como output;
  for(int i = pinInit; i<=pinFinal ;i+=stepPin){
    pinMode(i,OUTPUT); 
    digitalWrite(i,LOW);
  }
}

void eit_eletrodo::writeData(){
  // set os pinos dos multiplexadores

  writeMultiPlex(_pin_emissor_corrente.saida,23,29);
  writeMultiPlex(_pin_emissor_corrente.entrada,31,37);
  writeMultiPlex(_pin_leitura_tensao.saida,39,45);
  writeMultiPlex(_pin_leitura_tensao.entrada,47,53);
  
}


void eit_eletrodo::writeMultiPlex(byte values,byte initPin,byte finalPin){
  // Seta os pinos do multiplexador
  String setPin = String(values,BIN);
  byte i = 0;
  for(int pin = initPin; pin <= initPin +(finalPin - initPin) ;pin+=2){
    if(digitalRead(pin) != setPin[i]){
      if(setPin[i] == '0'){
        digitalWrite(pin,LOW);
      }
      else{
        digitalWrite(pin,HIGH);
      }
      
    }
    i+=1;
  }
  
}

//------------------Set variaveis------------------
void eit_eletrodo::setPinEmissorCorrenteSaida(byte pin_emissor_corrente_saida){
  _pin_emissor_corrente_saida = pin_emissor_corrente_saida;
}

void eit_eletrodo::setPinEmissorCorrenteEntrada(byte pin_emissor_corrente_entrada){
  _pin_emissor_corrente_entrada = pin_emissor_corrente_entrada;
}

void eit_eletrodo::setPinLeitorTensao(byte pin_leitor_tensao){
  _pin_leitor_tensao = pin_leitor_tensao;
}

void eit_eletrodo::setPinLeitorTensaoReferencia(byte pin_leitor_tensao_referencia){
  _pin_leitor_tensao_referencia = pin_leitor_tensao_referencia;
}

void eit_eletrodo::setEmissorCorrente(int eletrodosEmissoresCorrente){
  //Salva os eletros responsaveis por efetuar injetar corrente no sistemas
  _pin_emissor_corrente.valor_salvo = eletrodosEmissoresCorrente;
  _pin_emissor_corrente.saida = (eletrodosEmissoresCorrente >> 4);
  _pin_emissor_corrente.entrada = (eletrodosEmissoresCorrente & 0b00001111);
  
}

void eit_eletrodo::setLeituraTens(int eletrodosLeitorTensao){
  //Salva os eletros responsaveis por efetuar a leitura da variação de tensão
  _pin_leitura_tensao.valor_salvo = eletrodosLeitorTensao;
  _pin_leitura_tensao.saida = (eletrodosLeitorTensao >> 4);
  _pin_leitura_tensao.entrada = (eletrodosLeitorTensao & 0b00001111);
}



//------------------Get variaveis------------------


int eit_eletrodo::getValorLeituraTens(){
  return _pin_leitura_tensao.valor_salvo;
}

int eit_eletrodo::getValorEmissorCorrente(){
  return _pin_emissor_corrente.valor_salvo;
}

byte eit_eletrodo::getPinEmissorCorrenteSaida(){
  return _pin_emissor_corrente_saida;
}

byte eit_eletrodo::getPinEmissorCorrenteEntrada(){
  return _pin_emissor_corrente_entrada;
}

byte eit_eletrodo::getPinLeitorTensao(){
  return _pin_leitor_tensao;
}

byte eit_eletrodo::getPinLeitorTensaoReferencia(){
  return _pin_leitor_tensao_referencia;
}
