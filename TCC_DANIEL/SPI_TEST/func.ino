void configPinDigital(int inicialPin,int finalPin, int stepPin, bool mode){
  /*
   * Config state of Pin
  */
  if(mode){
    for(int i = inicialPin; i <= finalPin; i = i+stepPin){
      pinMode(i,OUTPUT);
    }
  }
  else{
    for(int i = inicialPin; i <= finalPin; i = i+stepPin){
      pinMode(i,INPUT);
    }
  }
}


void digitalWritePinEIT(String statePin,int initPin, int stepPin){
  /*
   * Function Write state of pin to EIT hardware
   *
   *
  */
  Serial.println(statePin);
  if(statePin.length() == 4){
    for(int i = 0; i < 4 ; i++){
      configPinDigital(initPin,statePin == "1");
      Serial.println(initPin);
      initPin = initPin + stepPin;
    }
  }
}





int tens(){
  Serial.print("Tens >>> ");
  Serial.println(A11);
  return analogRead(A11);
}
