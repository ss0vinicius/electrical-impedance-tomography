int convertHexToInt(char data){
  String HEX_CONVERT = "0123456789ABCDEF";
  int value_hex = HEX_CONVERT.indexOf(data);
  return value_hex; 
}

String ValueIntVectByte(int data){
  return String(data,BIN);
}
