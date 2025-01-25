import spidev
import RPi.GPIO as GPIO
import time
import csv
spi = spidev.SpiDev(0, 0) # create spi object connecting to /dev/spidev0.1
spi.max_speed_hz = 250000 # set speed to 250 Khz



leituras = list()

for emissroCorrente in range(0,16):

    if(emissroCorrente==15):
        emissroCorrente2 = 0
    else:
        emissroCorrente2 = emissroCorrente  + 1

    print("Corrente")
    print(f"{emissroCorrente} {emissroCorrente2}")
    
    corrente = (emissroCorrente << 4) + emissroCorrente2
    
    spi.writebytes([0x11,corrente ]) # write one by
    spi.writebytes([0x44])
    while((spi.readbytes(1)[0]) != corrente ):
        spi.writebytes([0x00,0x00])
        spi.writebytes([0x11,corrente])
        spi.writebytes([0x44])
            
    time.sleep(0.1)
    
   

    for i in range(1,14):

        emissor = emissroCorrente2 + i
        if (emissor>14):
            emissor = emissor - 15

        emissor2 = emissor  + 1
        
        emissores = (emissor << 4) + emissor2
        
        spi.writebytes([0x22,emissores]) # write one by
        spi.writebytes([0x55])
        while((spi.readbytes(1)[0]) != emissores):
            spi.writebytes([0x00,0x00])
            spi.writebytes([0x22,emissores])
            spi.writebytes([0x55])
        
        time.sleep(0.5)
        spi.writebytes([0xAA])
        ##spi.writebytes([0xFF,0xFE]) # write one byte
        spi.writebytes([0xCC])
        valor = spi.readbytes(1)
        
        while(valor[0] != 0xDD):
            
            spi.writebytes([0xCC])
            valor = spi.readbytes(1)
            time.sleep(1)
        
        spi.writebytes([0x99])
        values = spi.readbytes(1)
        values2 = spi.readbytes(1)
        values = (values2[0]  << 8) + values[0]
        
        leituras.append(values)
        
        print(values)
        


with open('leituras.csv', 'w') as f:

    w = csv.writer(f)
    
    w.writerow(leituras)

    f.close()

print(leituras)
print(len(leituras))

"""