from cmath import pi
import re
#import spidev
#import RPi.GPIO as GPIO
import time
import csv

class ComunicaSPI:
    def initSPI(self):
        self.spi = spidev.SpiDev(0,0) # conectar a interface /dev/spidev0.1
        self.spi.max_speed_hz = 250000
    

    def tensePin(self,pinoA,pinoB):
        """
        Seta e confere se os pinos de tensão setados estão corretos.

        Args
            pinoA: Pino de medição
            pinoB: Pino de referencia
        Returns
            bool: retorna de verdadeiro se conseguiu realializar e setar o pino de tensão
        
        """
        pino = int(self.concatenaPins(int(pinoA),int(pinoB)))
        self.setPinTense(pino)
        numberIntera = 0
        while ((self.getPinTense() != pino) and (numberIntera < 50)):
            self.setPinTense(pinTense = pino)
            numberIntera += 1
            time.sleep(0.1)
        
        if numberIntera >= 50:
            return False
        
        return True
        
    
    def correntePin(self,pinoA:int,pinoB:int):
        """
        Seta e confere se os pinos de corrente setados estão corretos.

        Args
            pinoA: Pino de emissão
            pinoB: Pino de entrada
        Returns
            bool: retorna de verdadeiro se conseguiu realializar e setar o pino de corrente
        
        """
        pino = int(self.concatenaPins(pinoA,pinoB))
        self.setPinCorrente(pino)
        numberIntera = 0
        while ((self.getPinCorrente() != pino) and (numberIntera < 50)):
            self.spi.writebytes([0x00])
            self.setPinCorrente(pino)
            numberIntera += 1
            time.sleep(0.1)
            
        
        if numberIntera >= 50:
            return False
        
        return True
    

    def ativaLeituras(self):
        self.spi.writebytes([0xAA])
    
    
    def Leitura(self):
        self.spi.writebytes([0xCC])
        while(self.spi.readbytes(1)[0] != 0xDD):
            time.sleep(0.5)
            self.spi.writebytes([0x00])
            self.spi.writebytes([0xCC])
        valor = self.getLeitura()
        return valor





    def concatenaPins(self,firstPin,secondPin):
        """
        Args
            firstPin: Pino A
            secondPin: Pino B
        Returns
            str: retorna de forma concatenada o valor em hexadecimal dos dosi valores sendo 0X(firstPin)(secondPin)
        """
        return  str((firstPin <<4) + secondPin)


    def setPinTense(self,pinTense:int):
        self.spi.writebytes([0x22,pinTense]) #Seta o pino de tensão com o valor hex pinTense com o comando 0x22 
    

    def setPinCorrente(self,pinCorrente:int):
        self.spi.writebytes([0x11,pinCorrente])#Seta o pino de Corrente com o valor hex pinCorrente com o comando 0x11
    
    def getPinTense(self):
        """
        Retorna o eletrodo de leitura de tensão es carregado no arduino, lembrando que esse valor sera numerico mas
        sera preciso de sua forma hexecimal para compreender qual eletrodo esta setado.

        Args:

        Return:
            str: Valor em hexadecimal dos pinos de tensão
        """
        self.spi.writebytes([0x55])
        return self.spi.readbytes(1)[0]
    
    
    def getPinCorrente(self):
        """
        Retorna o eletrodo de corrente carregado no arduino, lembrando que esse valor sera numerico mas sera preciso
        de sua forma hexecimal para compreender qual eletrodo esta setado.
        
        Args:

        Return:
            str: Valor em hexadecimal dos pinos de tensão
        """

        self.spi.writebytes([0x44])
        return self.spi.readbytes(1)[0]



    def getLeitura(self):
        
        leitura = 0

        self.spi.writebytes([0x99])
        time.sleep(0.1)
        leitura1 = self.spi.readbytes(1)
        
        leitura2 = self.spi.readbytes(1)
        
        
        leitura = int((leitura2[0] << 8)+ leitura1[0])
        return leitura
