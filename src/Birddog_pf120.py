from Devices import birddogPTZ
from ModuleSupport import eventEx
from extronlib.interface import EthernetClientInterface
from extronlib.system import Timer

@eventEx(birddogPTZ, ['Connected', 'Disconnected'])
def SMDConnectionEvent(interface : EthernetClientInterface, state):
    print('SMD on IP', interface.IPAddress, 'is', state)
    if state == 'Connected':
        interface.StartKeepAlive(30, 'Q')
    else:
        interface.StopKeepAlive()
        PTZConnectionTimer.Restart()


def ConnectSMD(timer, count):
    r = birddogPTZ.Connect()
    if r in ['Connected', 'ConnectedAlready']:
        birddogPTZ.Send('\xx\x01\x00\x01\xFF')
        timer.Stop()
    else:
        timer.Restart()
        
PTZConnectionTimer = Timer(5, ConnectSMD)
PTZConnectionTimer.Stop()