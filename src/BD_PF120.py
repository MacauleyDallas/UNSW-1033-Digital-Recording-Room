from ModuleSupport import eventEx
from extronlib.interface import EthernetClientInterface
from extronlib.system import Timer


class BirdogPF120:
    tele = 1
    wide = 0
    camId = 0
    __interface__ = None
    __connectionTimer__ = None

    def __addIPHeader__(cmd):
        l = len([cmd[i:i + 2] for i in range(0, len(cmd), 2)])
        return b''.join([bytes.fromhex('0100'), bytes.fromhex(format(l, '04')), bytes.fromhex('000000')], bytes.fromhex(cmd))

    def __send__(self, packet):
        # TODO: Check if ethernet or rs232 interface
        if True:
            packet = self.__addIPHeader__(packet)
        self.__interface__.send()
        
    def __init__(self, interface, id, ZoomSpeed):
        self.__interface__ = interface
        self.camId = id
        self.zoomSpeed = ZoomSpeed
   
    def Connect(self):
        self.__interface__.Connect()
        self.__connectionTimer__ = Timer(5, self.KeepAlive)
        self.__connectionTimer__.Restart()

    def Disconnect(self):
        self.__interface__.Disconnect()
        self.__connectionTimer__.Stop()

    def KeepAlive(self, *args):
        self.__interface__.Send('8{}090400FF'.format())
        self.__connectionTimer__.Restart()
    
    def Zoom(self, State : bool = True, Direction : int = 1):
        if State:
            if Direction == self.tele:
                cmd = '8{}0104072{}}FF'.format(self.camId, self.zoomSpeed)
            elif Direction == self.wide:
                cmd = '8{}0104073{}FF'.format(self.camId, self.zoomSpeed)
        else:
            cmd = '8{}01040700FF'
        self.__send__(cmd)

    
    

    

