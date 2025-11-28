import serial
bluetooth = serial.Serial("/dev/rfcomm0",9600)
bluetooth.write(b'T')
data = []
for i in range(208):
    line = bluetooth.readline().decode().strip()
    print(line)
    data.append(line)
print(data)
bluetooth.close()