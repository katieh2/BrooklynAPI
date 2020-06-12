from threading import Thread 
from time import sleep, monotonic
import serial
import atexit
from BrooklynAPI.Empire import Empire as empire_card

class Brooklyn:
    def __init__(self, port='/dev/ttyACM0'):
        self.cards = [None,None,None,None]
        self.ser = serial.Serial(port=port,baudrate=1000000,timeout=None)
        self.ser.write(bytearray([140]))
        self.ser.flush()
        self.ser.read(1)
        atexit.register(self.end)
        
    def end(self):
        print("Returning Brooklyn to idle mode")
        self.ser.write(bytearray([170]))
        self.ser.close()
        print("Programmed ended gracefully.")

    def card(self, cid, card_type):
        card = card_type(self, cid)
        self.cards[cid-1] = card
        return card
    
    def write(self,cid,cmd,packet_data):
        packet = [255]
        packet.append(cid)
        packet.append(cmd)
        packet.append(len(packet_data))
        packet.extend(packet_data)
        packet_sum = sum(packet)
        packet.append(packet_sum // 256)
        packet.append(packet_sum % 256)

        byte_send_packet = bytearray(packet)
        self.ser.write(byte_send_packet)
        self.ser.flush()
        resp = list(self.ser.read(4))
        resp.extend(list(self.ser.read(resp[3]+2)))
        return resp


class CardType:
    Empire = empire_card