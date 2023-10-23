from extronlib import event
from extronlib.interface import EthernetClientInterface
from extronlib.system import Wait, Timer, ProgramLog 
from  itertools import cycle

class TCPConnection:    
    def __init__(self, Device, *args):
        self.Device = Device     # the actual device
        self.Cmds = args         # the command or commands(list) and polltime 
        self.Connection = {'Client' : '', 'Counter' : 0, 'ProgLog': 0} # initial connection status and connect retry counter
        self.ClientConnect() # make first connection
        if self.Cmds:            # if there are args start the polling
            if self.Cmds[1]:
                self.DevicePoll = Timer(self.Cmds[1], self.DevicePolling)
                self.CmdList = cycle(self.Cmds[0]) 
    def ClientConnect(self):
        try:    
            self.Connection['Client'] = self.Device.Connect()        
            if self.Connection['Client'] in ('unknown: Connection timed out', 'unknown: No route to host', 'SSH Failed to connect', 'error: Connection refused'):    
                self.Connection['Counter'] += 1
                ProgramLog('DisconnectionCounter={}'.format(self.Connection['Counter']))          
                if self.Connection['Counter'] >= 3:
                    self.Connection['Counter'] = 0
                    self.Connection['ProgLog'] = 0
                    ProgramLog('{}-Can\'t connect, trying again..', 'error')
                    self.Device.Disconnect()  
            elif self.Connection['Client'] == 'Connected' or 'ConnectedAlready':
                self.Connection['Counter'] = 0
                if self.Connection['ProgLog'] == 0:
                    ProgramLog('{}:{}-Connection Successful'.format(self.Device.IPAddress, self.Device.IPPort), 'info')
                    self.Connection['ProgLog'] = 1
        except:
            pass        
    def DevicePolling(self, timer, count):    
        self.Cmd = next(self.CmdList)
        self.ClientConnect()
        if self.Connection['Client'] in ('Connected','ConnectedAlready'):
            self.Device.Send(self.Cmd)

            
class ModuleConnection: 
    Updates = set()    
    def __init__(self, Module, ID, *args):
        self.Module = Module
        self.Cmds = args
        self.ID = ID
        self.Connection = {'Client' : '', 'Counter' : 0, 'ProgLog' : 0, 'ID' : ''}  
        self.ClientConnect()
        if self.Cmds:
            if self.Cmds[1]:
                self.DevicePoll = Timer(self.Cmds[1], self.DevicePolling)               
                self.CmdList = cycle(self.Cmds[0])                    
    def ClientConnect(self):          
        try:
            self.Connection['Client'] = self.Module.Connect()
            ModuleConnection.ConnectionInfo((self.ID, self.Connection['Client']))             
            if self.Connection['Client'] in ('unknown: Connection timed out', 'unknown: No route to host', 'SSH Failed to connect', 'error: Connection refused'):             
                self.Connection['Counter'] += 1
                ProgramLog('DisconnectionCounter={}'.format(self.Connection['Counter']))
                if self.Connection['Counter'] >= 3:
                    self.Connection['Counter'] = 0
                    self.Connection['ProgLog'] = 0
                    self.Connection['Client'] = 'Disconnected'
                    ProgramLog('{}-Can\'t connect, trying again..', 'error')
                    ModuleConnection.ConnectionInfo((self.ID, self.Connection['Client']))
                    self.Module.Disconnect() 
            elif self.Connection['Client'] in ('Connected','ConnectedAlready'):
                self.Connection['Counter'] = 0
                if self.Connection['ProgLog'] == 0:
                    ProgramLog('{}:{}-Connection Successful'.format(self.Module.IPAddress, self.Module.IPPort), 'info')
                    self.Connection['ProgLog'] = 1 
        except:
            pass        

    def DevicePolling(self, timer, count): 
        self.Cmd = next(self.CmdList)
        self.ClientConnect()
        if self.Connection['Client'] in ('Connected','ConnectedAlready'):
            try:
                if self.Cmds[2]:
                    self.Module.Update(self.Cmd, self.Cmds[2])
                else:
                    self.Module.Update(self.Cmd)
            except:
                pass
    def ConnectionInfo(data):
        for callback in ModuleConnection.Updates:
            callback(data)            
    def ConnectionStatus(info, callback):
        ModuleConnection.Updates.add(callback)
        return callback
class SerialConnection:       
    def __init__(self, Device, *args):
        self.Device = Device
        self.Cmds = args
        if self.Cmds:
            if self.Cmds[1]:
                self.DevicePoll = Timer(self.Cmds[1], self.DevicePolling)
                self.CmdList = cycle(self.Cmds[0]) 
    def DevicePolling(self, timer, count):
        self.Cmd = next(self.CmdList)
        self.Device.Send(self.Cmd)
          
            
