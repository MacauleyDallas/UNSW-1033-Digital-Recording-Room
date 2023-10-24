from ModuleSupport import eventEx
from extronlib.interface import EthernetClientInterface
from extronlib.system import Timer


class BirdogPF120:
    tele = 1
    wide = 0
    camId = 0
    __interface__ = None
    __connectionTimer__ = None

    def __addIPHeader__(self, cmd):
        l = len([cmd[i:i + 2] for i in range(0, len(cmd), 2)])
        return b''.join([bytes.fromhex('0100'), bytes.fromhex(format(l, '04')), bytes.fromhex('000000'), bytes.fromhex(cmd)])

    def __send__(self, packet):
        # TODO: Check if ethernet or rs232 interface
        if True:
            packet = self.__addIPHeader__(packet)
        self.__interface__.send()
        
    def __init__(self, interface, id, ZoomSpeed):
        self.__interface__ = interface
        self.camId = id
        self.zoomSpeed = ZoomSpeed
   
    def Zoom(self, State : bool = True, Direction : int = 1):
        if State:
            if Direction == self.tele:
                cmd = '8{}0104072{}FF'.format(self.camId, self.zoomSpeed)
            elif Direction == self.wide:
                cmd = '8{}0104073{}FF'.format(self.camId, self.zoomSpeed)
        else:
            cmd = '8{}01040700FF'.format(self.camId)
        self.__send__(cmd)
        
    def AutoFocus(self, State : bool = True):
        if State:
            cmd = '8{}01043802FF'.format(self.camId, self.zoomSpeed)
        else:
            cmd = '8{}01043803FF'.format(self.camId)
        self.__send__(cmd)
        
    def Focus(self, State : bool = True, Direction : int = 1):
        if State:
            if Direction == self.tele:
                cmd = '8{}0104082{}FF'.format(self.camId, self.zoomSpeed)
            elif Direction == self.wide:
                cmd = '8{}0104083{}FF'.format(self.camId, self.zoomSpeed)
        else:
            cmd = '8{}01040800FF'.format(self.camId)
        self.__send__(cmd)

    
    

    

