import serial
import sys
import time

adr=0x0             #Адрес ЛБП (0-30)
data=bytearray(26)

#----------Стандартные настройки------------------
stdCurrent  = 100   #Ограничение тока в mA
voltageStep = 10    #Ступени регулировки напряжения mV
maxVoltage  = 10000 #Напряжение окончания замеров
#-------------------------------------------------


        
serialPort = serial.Serial( #установка настроек порта. 9600 бод, 8 бит, без чётности, 1 стопбит
    port='COM2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS)


#----------Очистка массива данных-----------------
def clearData():
    for j in range(0, 26):
        data[j]=0
        

#----------Нахождение суммы данных----------------
def checkSumm(): 
    for j in range(0, 25):
        if data[25]+data[j]<256:
            data[25]=data[25]+data[j]
        else:
            data[25]=data[25]+data[j]-256

            
#----------Установка соединения с ЛБП-------------
def setRemote(adress): 
    clearData()
    data[0]=0xAA
    data[1]=adress
    data[2]=0x20
    data[3]=1
    checkSumm()
    serialPort.write(data)

#----------Закрыть соединения с ЛБП---------------
def closeRemote(adress): 
    clearData()
    data[0]=0xAA
    data[1]=adress
    data[2]=0x20
    data[3]=0
    checkSumm()
    serialPort.write(data)
    serialPort.close()

#----------Подать напругу!------------------------
def onVoltage(adress): 
    clearData()
    data[0]=0xAA
    data[1]=adress
    data[2]=0x21
    data[3]=1
    checkSumm()
    serialPort.write(data)

#----------Снять напругу!-------------------------
def offVoltage(adress): 
    clearData()
    data[0]=0xAA
    data[1]=adress
    data[2]=0x21
    data[3]=0
    checkSumm()
    serialPort.write(data)

#----------Установка напряжения в мВ--------------
def setVoltage(adress, Voltage): 
    bytesVoltage = list((Voltage >> i) & 0xFF for i in range(0,32,8)) #разложение большого числа на несколько байт
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

#----------Установка тока в мА--------------------
def setCurrent(adress, Current): 
    bytesCurrent = list((Current >> i) & 0xFF for i in range(0,16,8)) #разложение большого числа на несколько байт
    clearData()
    data[0]=0xAA
    data[1]=adress
    data[2]=0x24
    data[3]=bytesCurrent[0]
    data[4]=bytesCurrent[1]
    checkSumm()
    serialPort.write(data)

#----------Собстно сам код------------------------
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

