import serial
import sys
import time

adr=0x0
data= bytearray(26)
        
serialPort = serial.Serial(
    port='COM2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS)


def clearData():
    for j in range(0, 26):
        data[j]=0

def checkSumm():
    for j in range(0, 25):
        if data[25]+data[j]<256:
            data[25]=data[25]+data[j]
        else:
            data[25]=data[25]+data[j]-256
            
def setRemote(adress): #Установка соединения с ЛБП
    clearData()
    data[0]=0xAA
    data[1]=adress
    data[2]=0x20
    data[3]=1
    checkSumm()
    serialPort.write(data)
    return True

def closeRemote(adress): #закрытие соединения с ЛБП
    clearData()
    data[0]=0xAA
    data[1]=adress
    data[2]=0x20
    data[3]=0
    checkSumm()
    serialPort.write(data)
    serialPort.close()
    return True

def onVoltage(adress): #Подать напругу!
    clearData()
    data[0]=0xAA
    data[1]=adress
    data[2]=0x21
    data[3]=1
    checkSumm()
    serialPort.write(data)
    
def offVoltage(adress): #Снять напругу!
    clearData()
    data[0]=0xAA
    data[1]=adress
    data[2]=0x21
    data[3]=0
    checkSumm()
    serialPort.write(data)

def setVoltage(adress, Voltage): #становка напряжения в мВ
    bytesVoltage = list((Voltage >> i) & 0xFF for i in range(0,32,8))
    clearData()
    data[0]=0xAA
    data[1]=adress
    data[2]=0x23
    data[3]=bytesVoltage[0]
    data[4]=bytesVoltage[1]
    data[5]=bytesVoltage[2]
    data[6]=bytesVoltage[3]
    checkSumm()
    serialPort.write(data)

def setCurrent(adress, Current): #становка тока в мА
    bytesCurrent = list((Current >> i) & 0xFF for i in range(0,16,8))
    clearData()
    data[0]=0xAA
    data[1]=adress
    data[2]=0x24
    data[3]=bytesCurrent[0]
    data[4]=bytesCurrent[1]
    checkSumm()
    serialPort.write(data)

setRemote(adr)
print("connected")
setCurrent(adr, 100)
onVoltage(adr)

for i in range(0,50):
    setVoltage(adr, i*100)
    time.sleep(1)

offVoltage(adr)
closeRemote(adr)
print("Closed")

