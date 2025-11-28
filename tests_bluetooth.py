import serial
bluetooth = serial.Serial("/dev/rfcomm0",9600)
bluetooth.write(b'H')
data = bluetooth.readline()
print(data)
bluetooth.close()