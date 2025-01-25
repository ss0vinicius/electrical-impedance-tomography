
#ifndef eit_eletrodo_H
#define eit_eletrodo_H

#include "Arduino.h"

struct pinosAtivos{
  int valor_salvo;
  byte saida;
  byte entrada;
};
  

class eit_eletrodo
{
  public:
      eit_eletrodo(int pinInit,int pinFinal,int stepPin);

      //Metodos

      void writeData();
      void writeMultiPlex(byte values,byte initPin,byte finalPin);

      // Set variaveis
      void setPinEmissorCorrenteSaida(byte pin_emissor_corrente_saida);
      void setPinEmissorCorrenteEntrada(byte pin_emissor_corrente_entrada);
      void setPinLeitorTensao(byte pin_leitor_tensao);
      void setPinLeitorTensaoReferencia(byte pin_leitor_tensao_referencia);

      void setEmissorCorrente(int eletrodosEmissoresCorrente);
      void setLeituraTens(int eletrodosLeitorTensao);
      

      //Get Variaveis

      int getValorLeituraTens();
      int getValorEmissorCorrente();
      
      byte getPinEmissorCorrenteSaida();
      byte getPinEmissorCorrenteEntrada();
      byte getPinLeitorTensao();
      byte getPinLeitorTensaoReferencia();
      

  private:
    

      byte _pin_emissor_corrente_saida;
      byte _pin_emissor_corrente_entrada;
      byte _pin_leitor_tensao;
      byte _pin_leitor_tensao_referencia;

      pinosAtivos _pin_emissor_corrente;
      pinosAtivos _pin_leitura_tensao;

  
};

#endif
