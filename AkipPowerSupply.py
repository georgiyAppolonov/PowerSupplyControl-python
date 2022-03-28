import serial
import sys
import time

#во всех методах прописать селф

class AkipPowerSupply():
    """
    Your docstrings are here.
    
    Attributes
    ----------
    There are docstrings about each attribute.
    
    Methods
    -------
    There are docstrings about each metod.
    
    ....
    
    Use numpydoc style-guide or Google python style-guide
    """

    
    
    def __init__(self, adr):
        """
        Знать бы что собстно инициализировать

        Принимает
        ---------
        byte - адрес устройства (0x00-0x1E)
        """

        adr=0x0 
        data=bytearray(26)
        
        pass
    
    
    def _check_sum(self):
        """
        Нахождение чек суммы данных, отправляемых на ЛБП
        +костыль вместо переполнения байта
        """
        
        for j in range(0, 25):
        if data[25]+data[j]<256:
            data[25]=data[25]+data[j]
        else:
            data[25]=data[25]+data[j]-256
        pass
    

    def _clear_data(self):
        """
        Очистка массива данных перед началом сборки нового пакета
        """

        for j in range(0, 26):
            data[j]=0
        pass
    
    
    def connect(self):
        """
        Подключение к ЛБП, активация Remote режима
        
        Возвращает
        ----------
        bool - произошло ли подключение
        """
            
        clearData()
        data[0]=0xAA
        data[1]=adress
        data[2]=0x20
        data[3]=1
        checkSumm()
        serialPort.write(data)
        pass
    
    
    def disconect(self):
        """
        Your docstrings...
        """
            
        clearData()
        data[0]=0xAA
        data[1]=adr
        data[2]=0x20
        data[3]=0
        checkSumm()
        serialPort.write(data)
        serialPort.close()
        pass
    
    
    def reset(self): #А есть ли такая функция?
        """
        Your docstrings...
        """
        
        pass
    
    
    def configure_port(self):
        """
        Установка настроек порта.

        Стандартные параметры: COM2, 9600 бод, 8 бит, без чётности, 1 стопбит        
        """
        serialPort = serial.Serial(
        port='COM2',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS)
        pass
    
    
    def on_voltage(self):
        """
        Подать напряжение на выход ЛБП
        """
        
        clearData()
        data[0]=0xAA
        data[1]=adr
        data[2]=0x21
        data[3]=1
        checkSumm()
        serialPort.write(data)  
        pass
    
    
    def off_voltage(self):
        """
        Снять напряжение с выхода ЛБП

        """
        
        clearData()
        data[0]=0xAA
        data[1]=adr
        data[2]=0x21
        data[3]=0
        checkSumm()
        serialPort.write(data)
        pass
    
    
    def set_voltage(self, Voltage):
        """
        Устанавливает напряжение на выходе ЛБП
        Раскладывает входное число на 4 байта, которые и отправляет.

        Принимает
        ---------
        Число - Напряжение в мВ
        """

        bytesVoltage = list((Voltage >> i) & 0xFF for i in range(0,32,8)) 
        clearData()
        data[0]=0xAA
        data[1]=adr
        data[2]=0x23
        data[3]=bytesVoltage[0]
        data[4]=bytesVoltage[1]
        data[5]=bytesVoltage[2]
        data[6]=bytesVoltage[3]
        checkSumm()
        serialPort.write(data)
        pass
    
    
    
    def set_max_current(self, Сurrent):
        """
        Устанавливает ограничение силы тока на выходе ЛБП
        Раскладывает входное число на 2 байта, которые и отправляет.

        Принимает
        ---------
        Число - Сила тока в мА
        """
        
        bytesCurrent = list((Current >> i) & 0xFF for i in range(0,16,8))
        clearData()
        data[0]=0xAA
        data[1]=adr
        data[2]=0x24
        data[3]=bytesCurrent[0]
        data[4]=bytesCurrent[1]
        checkSumm()
        serialPort.write(data)
        pass

    def state(self):
        """
        Запрашивает состояние ЛБП (режим работы CC/CV)...

        Возвращает
        ----------
        bool - состояние СС - сработавшее ограничение тока, возможная перегрузка
        """

        #Посмотреть в даташнике 
        pass
