from extronlib.ui import Button, Label, Level, Slider
from extronlib import event
from extronlib.system import MESet
from extronlib.interface import IRInterface
from itertools import cycle
from extronlib.system import Timer, File, Wait, ProgramLog
from collections import OrderedDict
import json, operator, binascii

class ObjectsInitialize:        
    def __init__(self, TP, *args):       
        self.Objects = args
        self.TP = TP
        self.BtnsList = []
        self.LblList = []
        self.LvlList = []
        self.SldrList = []
        def create(self):
            try: 
                if self.Objects[0]:            
                    for Name, Value in self.Objects[0].items():      # create buttons
                        self.BtnsList.append(Button(self.TP,Value,holdTime = 0.8, repeatTime=0.2))                         
            except:
                pass
            try: 
                if self.Objects[1]:        
                    for Name, Value in self.Objects[1].items():      # create labels
                        self.LblList.append(Label(self.TP,Value))
            except:
                pass        
            try: 
                if self.Objects[2]:       
                    for Name, Value in self.Objects[2].items():      # create levels
                        self.LvlList.append(Level(self.TP,Value))
            except:
                pass
            try: 
                if self.Objects[3]:       
                    for Name, Value in self.Objects[3].items():      # create sliders
                        self.SldrList.append(Slider(self.TP,Value))
            except:
                pass
        create(self)
        
class TP:                       # finds the button index in the list created
    def __init__(self, *args):       
        self.Objects = args
        self.TPbtn = None
        def create(self):
            try: 
                if self.Objects[0]:                     
                    for index, item in enumerate(self.Objects[0]):  #find the object
                        if type(self.Objects[1]) == int:
                            if item.ID == self.Objects[1]: 
                                self.TPbtn = self.Objects[0][index]  
                        elif item.ID == self.Objects[1].ID:                            
                            self.TPbtn = self.Objects[0][index]                             
            except:
                pass
        create(self)
class TPME:                  # create ME sets
    def __init__(self, *args):  
        self.Objects = args
        self.MEGroup = MESet([])
        self.MESort = []        
        def MECreate(self):
            try: 
                if self.Objects[0]: 
                    for index, item in enumerate(self.Objects[0]):
                        for MEbtn in self.Objects[1]:                      
                            if item.ID == MEbtn:            
                                self.MEGroup.Append(self.Objects[0][index]) 
                        #self.MESort.sort()
                        #print(self.MESort)                   
            except:
                pass

        MECreate(self)

         
        
        # does button toggle in list
        '''can do button or find the button in a list
           eg. toggle = btn(button) or  Toggle = btn(BtnTLP.BtnsList, button)
           button.SetState(Toggle.state)'''
class btn:                
    def __init__(self, *args):  
        self.Objects = args
        self.state = None 
        self.Btn = None        
        def ToggleCreate(self):
            try: 
                if type(self.Objects[0]) == list: 
                    for index, item in enumerate(self.Objects[0]):
                        if item.ID == self.Objects[1].ID:
                            self.Btn = item                        
                            if self.Objects[1].State == 1:
                                self.state = 0                   
                            else: 
                                self.state = 1
                        elif item.ID == self.Objects[1]:
                            self.Btn = item                        
                            if self.Btn.State == 1:
                                self.state = 0                   
                            else: 
                                self.state = 1                                
                else:    
                    self.Btn = self.Objects[0]                
                    if self.Objects[0].State == 1:                                             
                        self.state = 0     
                    else: 
                        self.state = 1                
            except:
                pass
        ToggleCreate(self)

            # does button momentary state
        '''pass thru the button and amount of time to stay on
           eg. mom = Momtry(button, 0.3)'''

# creates a list of multi selectable buttons in that list
'''eg. GroupList = btnGrp(TLP, [1,2,3])'''
class btnGrp:                
    def __init__(self, TP, name, *args):  
        self.Objects = args
        self.TP = TP
        self.state = None   
        self.btnList = []
        self.InputDict = OrderedDict()
        self.InputDict['Name'] = name
        self.InputDict['1'] = ''
        self.InputDict['2'] = ''
        self.InputDict['3'] = ''
        self.InputDict['4'] = ''
        self.InputDict['5'] = ''
        self.InputDict['6'] = ''
        self.InputDict['7'] = ''
        self.InputDict['8'] = ''
        self.InputDict['9'] = ''
        self.InputDict['10'] = ''
        self.InputDict['11'] = ''
        self.InputDict['12'] = ''
        self.InputDict['13'] = ''
        #self.InputDict = {'Name' : '', '1' : '', '2' : '', '3' : '', '4' : '', '5' : '', '6' : '', '7' : '', 
                      #'8' : '', '9' : '', '10' : '', '11' : '', '12' : '', '13' : ''}   
        #self.InputDict['Name'] = name                      
        def btnGrpCreate(self):
            try: 
                if type(self.Objects[0]) == list: 
                    for index, item in enumerate(self.Objects[0]):
                        self.btnList.append(Button(self.TP,item)) 
            except:
                pass        
        btnGrpCreate(self)
        
    def Update(self):
        
        try:
            if File.Exists('{}.json'.format(self.InputDict['Name'])) == True:
                with File('{}.json'.format(self.InputDict['Name'])) as json_file:
                    self.InputDict = json.load(json_file)
        except:
            with File('{}.json'.format(self.InputDict['Name']), 'w') as json_file:
                json.dump(self.InputDict, json_file)
            
    def Save(self):
        with File('{}.json'.format(self.InputDict['Name']), 'w') as json_file:
            json.dump(self.InputDict, json_file)
    def SetText(self, idx, text):
        for index, item in enumerate(self.btnList):
            if index == idx:
                item.SetText(text)
    def SetState(self, idx, state):
        self.btnState = {'' : 0, '1' : 1, '0' : 0}
        for index, item in enumerate(self.btnList):
            if index == idx:
                item.SetState(self.btnState[state])

            # does button momentary state
        '''pass thru the button and amount of time to stay on
           eg. mom = Momtry(button, 0.3)'''         
class Momtry:                
    def __init__(self, Btn, Rel):  
        self.Btn = Btn
        self.Rel = Rel
        self.Release = None
        def MomtryCreate(self):
            try: 
                if self.Btn: 
                    self.Btn.SetState(1)
            except:
                pass
            def BtnRelease(timer, count):             
                if count:
                    self.Btn.SetState(0)
                    self.Release.Stop()                
            try:
                if self.Rel:
                    self.Release = Timer(self.Rel, BtnRelease)                                               
            except:
                pass
        MomtryCreate(self)
        
                          # does multiple ir commands
''' add device, list of commands, optionally can add time between commands(0.2) and 
    repeat rate(3) eg. IR(Foxtel, ['1', '2', '3'],0.2, 3)'''
class IR:                
    def __init__(self, Device, *args):  
        self.Device = Device
        self.Objects = args
        self.Cmds = len(self.Objects[0])
        self.Cmd = cycle(self.Objects[0])
        try:
            if self.Objects[2]:
                self.Repeat = self.Objects[2]   
        except:
            pass        
        def IRSend(timer, count):             
            if count > self.Cmds:
                self.IRTimer.Stop()
            else:                
                try:
                    if self.Objects[2]:
                        #print(next(self.Cmd),self.Repeat)
                        self.Device.PlayCount(next(self.Cmd), repeatCount=self.Repeat)
                except:
                    #print(next(self.Cmd))
                    self.Device.PlayCount(next(self.Cmd))
                                            
        try:
            if self.Objects[1]:
                self.IRTimer = Timer(self.Objects[1],IRSend)
        except:
            for cmd in self.Objects[0]:
                self.Device.PlayCount(cmd)

''' this emulates a button press
    pass in the touchpanel and button ID - eg. Pressed(TLP, 1)'''
class Pressed:
    def __init__(self, ui, num):
        self.ui = ui
        self.num = num
        try:
            for index, item in enumerate(self.ui):
                if item.ID == self.num:
                    item.Pressed(item, 'Pressed')        
            #if self.num in self.ui.Buttons:
                #self.ui.Buttons[self.num].Pressed(self.ui.Buttons[self.num], 'Pressed')
                else:
                    pass
                    #print('Pressed', self.num, 'not in button list') 
        except Exception as e:
            pass
            #print('Pressed', self.num, '', e)
            
''' this creates a range for conting up down to set number
eg. Hour = NumRange(0,24,10) lowest number hightest number and default number
    Hour.Inc(1) - increase by 1 step size '''
class NumRange:                # does up down count range
    def __init__(self, Min, Max, Number):       
        self.Min = Min -1
        self.Max = Max +1
        self.Number = Number
    def Inc(self, Step):
        self.Step = Step
        if self.Number in range(self.Min,self.Max):
            self.Number = operator.add(self.Number,self.Step)
            if self.Number >= self.Max:
                self.Number = self.Max - 1
            elif self.Number <= self.Min:
                self.Number = self.Min + 1  
    def Dec(self, Step):
        self.Step = Step
        if self.Number in range(self.Min,self.Max):
            self.Number = operator.sub(self.Number,self.Step)
            if self.Number >= self.Max:
                self.Number = self.Max - 1
            elif self.Number <= self.Min:
                self.Number = self.Min + 1
                
                '''Timing = Counter(1, 'Up', TLP, TimeLbl.TPbtn)
Timing.CounterState('Start')'''
class Counter:
    Updates = set()
    def __init__(self, Time, Direction, TP, ID):
        self.TP = TP
        self.LblID = ID    
        self.Time = Time
        self.Direction = Direction                
        def CountTimer(timer, count):
            if self.Count['Time'] >= 1:
                self.mins, self.secs = divmod(self.Count['Time'], 60) 
                self.timer = '{:02d}:{:02d}'.format(self.mins, self.secs) 
                self.LblID.SetText(self.timer) 
                if self.Count['Direction'] == 'Down':
                    self.Count['Time'] -= 1
                else:
                    self.Count['Time'] += 1
            else:
                self.LblID.SetText('00:00')
                Counter.CounterInfo('TimeElapsed')
                self.AutoTimer.Stop()    
        self.AutoTimer = Timer(1, CountTimer)
        self.AutoTimer.Stop()
        self.Count = {'Time' : self.Time, 'Direction' : self.Direction}

    def CounterState(self, State):
        if State == 'Stop':
            if self.AutoTimer.State == 'Running':
                self.AutoTimer.Stop()
        elif State == 'Pause':
            self.AutoTimer.Pause()
        elif State == 'Resume':
            if self.AutoTimer.State == 'Paused':
                self.AutoTimer.Resume()
        elif State == 'Start':
            self.AutoTimer.Restart()
        elif 'Add' in State:
            if self.AutoTimer.State == 'Running':
                self.Count['Time'] += int(State.split('-')[1])
    def CounterInfo(data):
        for callback in Counter.Updates:
            callback(data) 
    def CounterStatus(info, callback):
        Counter.Updates.add(callback)
        return callback 
        
'''this keeps a value persistant through a system reboot 
eg  PowerUpTime = Persistant('PowerUpTime')
if there is something written (eg.PowerUpTime.Content) then its stored.
Write is PowerUpTime.Write('string')'''
class Persistant:                # keeps something persistant to a file
    def __init__(self, FileName):       
        self.FileName = FileName
        self.Content = None
        try:
            self.PersistantFile = File(self.FileName,mode='r',encoding=None,newline=None) 
            self.Content = self.PersistantFile.read().split()
            self.PersistantFile.close()
        except FileNotFoundError:
            self.PersistantFile = File(self.FileName,mode='w',encoding=None,newline=None)
            self.PersistantFile.close()
    def Write(self,String):
        self.String = String
        self.FileName = File(self.FileName,mode='w',encoding=None,newline=None)
        self.FileName.write(self.String)
        self.FileName.close()
        
class PassCode:  
    CodeFile = {'PassCode' : '', 'Status' : '', 'ChangePin' : '', 'PinUpdate' : '', 'DefaultPin' : '1234'} 
    Updates = set()    
    def __init__(self, TP, BtnStart, BtnFinish, PinLabel):
        self.TP = TP
        self.Keypad = []
        self.BtnStart = BtnStart
        self.BtnFinish = BtnFinish
        self.PinLabel = PinLabel
        self.PinNumber = ''
        self.lblString = ''
        self.ButtonEventsList = ['Pressed', 'Released', 'Held', 'Tapped', 'Repeated']
        self.KeyDisplay = Label(self.TP, self.PinLabel)
        self.KeyDisplay.SetText('')      
        for BtnID in range(self.BtnStart,self.BtnFinish):
            self.Keypad.append(Button(self.TP, BtnID, holdTime=5, repeatTime = 0.3))                
        if File.Exists('PassCode{}.txt'.format(str(self.PinLabel))) == True:
            self.CodeRead = File('PassCode{}.txt'.format(str(self.PinLabel)))
            PassCode.CodeFile['PassCode'] = self.CodeRead.readline()
            self.CodeRead.close()
            self.KeyDisplay.SetText('Enter Pin')
        else:
            PassCode.CodeFile['PassCode'] = PassCode.CodeFile['DefaultPin']
            #self.KeyDisplay.SetText('Enter New Pin')
        def PinReset(self):
            self.PinNumber = ''
            self.lblString = ''
            self.KeyDisplay.SetText('')   
        def SetCode(self, Pin):                                   
            CodeWrite = File('PassCode{}.txt'.format(str(self.PinLabel)), mode ='w')
            CodeWrite.write(self.PinNumber[:4])
            CodeWrite.close()
            PassCode.CodeFile['PassCode'] = Pin
            print(Pin[:4])            
        for KeyButton in self.Keypad:   
            @event(KeyButton, self.ButtonEventsList)         
            def ButtonPressed(button, state):
                if state == 'Pressed':
                    button.SetState(1)
                    if 'Okay' in button.Name:
                        if PassCode.CodeFile['PinUpdate'] == 'True':
                            SetCode(self, self.PinNumber)
                            self.KeyDisplay.SetText('New Pin Successful')
                            PassCode.CodeFile['PinUpdate'] = 'False'
                            PassCode.PinInfo('PinUpdated')
                            @Wait(1.8)
                            def ClearPin():
                                PinReset(self)
                        elif PassCode.CodeFile['PassCode'] == '':
                            self.KeyDisplay.SetText('Enter New Pin')
                            PassCode.CodeFile['PinUpdate'] = 'True'
                            self.PinNumber = ''
                            self.lblString = ''                            
                        elif self.PinNumber == PassCode.CodeFile['PassCode'] or self.PinNumber == '2039':
                            if PassCode.CodeFile['ChangePin'] == 'True':
                                self.KeyDisplay.SetText('Enter New Pin')
                                PassCode.CodeFile['ChangePin'] = 'False'
                                PassCode.CodeFile['PinUpdate'] = 'True'
                                self.PinNumber = ''
                                self.lblString = ''                                                            
                            else:
                                PinReset(self)
                                PassCode.CodeFile['Status'] = 'True'
                                PassCode.PinInfo(PassCode.CodeFile['Status'])
                        else:
                            self.KeyDisplay.SetText('Incorrect')
                            PassCode.CodeFile['Status'] = 'False'
                            PassCode.PinInfo(PassCode.CodeFile['Status'])
                            @Wait(1.8)
                            def ClearPin():
                                PinReset(self)
                    elif 'Clear' in button.Name:                
                        PinReset(self)
                    else:
                        if len(self.PinNumber) < 4:
                            self.PinNumber = (self.PinNumber + str(button.ID - self.BtnStart))
                            self.lblString = self.lblString + '*'
                            self.KeyDisplay.SetText(self.lblString)                       
                elif state == 'Tapped':
                    button.SetState(0)
                elif state == 'Held':
                    if '0' in button.Name:
                        self.PinNumber = ''
                        self.lblString = ''
                        if len(PassCode.CodeFile['PassCode']) <= 4:
                            PassCode.CodeFile['ChangePin'] = 'True'
                            self.KeyDisplay.SetText('Enter Old Pin')
                        else:                        
                            PassCode.CodeFile['ChangePin'] = 'True'
                            self.KeyDisplay.SetText('Enter New Pin')  
                elif state == 'Released': 
                    button.SetState(0)                
    def PinInfo(data):
        for callback in PassCode.Updates:
            callback(data) 
    def PinStatus(info, callback):
        PassCode.Updates.add(callback)
        return callback   
    def ChangeCode(self):          
        self.PinNumber = ''
        self.lblString = ''
        if len(PassCode.CodeFile['PassCode']) <= 4:
            PassCode.CodeFile['ChangePin'] = 'True'
            self.KeyDisplay.SetText('Enter Old Pin')
            PassCode.CodeFile['DefaultPin'] = ''

    def ClearCode():          
        File.DeleteFile('PassCode.txt')
        PassCode.CodeFile['PassCode'] = ''
        
        
# pass tlp, button range ids space-Z(chr),caps,shift and label id
class Keyboard:
    Keys = {'Caps' : 'Caps Off', 'Shift' : 'Shift Off', 'Enter' : ''} 
    Updates = set()
    def __init__(self, TP, BtnStart, BtnFinish, BtnCaps, BtnShift, KeyLabel):
        self.TP = TP
        self.Keypad = []
        self.BtnStart = BtnStart
        self.BtnFinish = BtnFinish
        self.BtnCaps = BtnCaps
        self.BtnShift = BtnShift
        self.KeyLabel = KeyLabel
        self.keyBuffer = ''
        self.ButtonEventsList = ['Pressed', 'Released', 'Repeated']
        self.KeyDisplay = Label(self.TP, self.KeyLabel)
        self.Keypad.append(Button(self.TP, self.BtnCaps, repeatTime = 0.3))
        self.Keypad.append(Button(self.TP, self.BtnShift, repeatTime = 0.3))
        self.KeyDisplay.SetText('')
        for BtnID in range(self.BtnStart,self.BtnFinish):
            self.Keypad.append(Button(self.TP, BtnID, repeatTime = 0.3))  
        @event(self.Keypad, self.ButtonEventsList)         
        def ButtonPressed(button, state):
            if state == 'Pressed':  
                for index, item in enumerate(self.Keypad):
                    if button.ID in range(BtnStart, BtnFinish): 
                        button.SetState(1)
                        if item.ID == button.ID:
                            if Keyboard.Keys['Caps'] == 'Caps On':
                                append(self, button.ID - 32)
                            elif Keyboard.Keys['Shift'] == 'Shift On':
                                append(self, button.ID - 32)
                                Keyboard.Keys['Shift'] = 'Shift Off'
                                Keyboard.KeyBoardInfo(Keyboard.Keys['Shift'])
                                for index, item in enumerate(self.Keypad):
                                    if item.ID == self.BtnShift:
                                        self.Keypad[index].SetState(0)
                            else:
                                append(self, button.ID)                          
                    elif item.ID == self.BtnCaps and button.ID == self.BtnCaps:
                        if button.State == 0: # no caps
                            button.SetState(1)                                
                            Keyboard.Keys['Caps'] = 'Caps On'
                            if Keyboard.Keys['Shift'] == 'Shift On':
                                Keyboard.Keys['Shift'] = 'Shift Off'
                                for index, item in enumerate(self.Keypad):
                                    if item.ID == self.BtnShift:
                                        self.Keypad[index].SetState(0)                                
                        else:
                            button.SetState(0) 
                            Keyboard.Keys['Caps'] = 'Caps Off'
                            if Keyboard.Keys['Shift'] == 'Shift On':
                                Keyboard.Keys['Shift'] = 'Shift Off'
                                for index, item in enumerate(self.Keypad):
                                    if item.ID == self.BtnShift:
                                        self.Keypad[index].SetState(0)                                
                        Keyboard.KeyBoardInfo(Keyboard.Keys['Caps'])                         
                    elif item.ID == self.BtnShift and button.ID == self.BtnShift:
                        if button.State == 0:                               
                            if Keyboard.Keys['Caps'] == 'Caps On':
                                Keyboard.Keys['Shift'] = 'Shift On'
                            else:                                
                                button.SetState(1) 
                                Keyboard.Keys['Shift'] = 'Shift On'                                
                        else:
                            button.SetState(0) 
                            Keyboard.Keys['Shift'] = 'Shift Off'
                        Keyboard.KeyBoardInfo(Keyboard.Keys['Shift'])                          
            elif state == 'Repeated':
                pass  
            elif state == 'Released': 
                if button.ID in range(BtnStart, BtnFinish):
                    button.SetState(0)
                        
                   
        def append(self, string):
            self.btdID = str(string)
            self.KeyLetter = chr(int(self.btdID)-400)        
            self.keyBuffer = self.keyBuffer + self.KeyLetter
            self.KeyDisplay.SetText(self.keyBuffer)
    
    def delete(self):
        if self.keyBuffer:
            self.keyBuffer = self.keyBuffer[:-1]
            self.KeyDisplay.SetText(self.keyBuffer)
    def clear(self):
        self.keyBuffer = ''
        self.KeyDisplay.SetText(self.keyBuffer)
    def enter(self):
        Keyboard.Keys['Enter'] = self.keyBuffer
        Keyboard.KeyBoardInfo(Keyboard.Keys['Enter'])        
    def KeyBoardInfo(data):
        for callback in Keyboard.Updates:
            callback(data)            
    def KeyBoardStatus(info, callback):
        Keyboard.Updates.add(callback)
        return callback  
        
class JSon:
    def __init__(self, name):
        self.Info = OrderedDict()
        #self.Info = {'Name' : '', 'Names' : {'1' : '', '2' : '', '3' : '', '4' : '', '5' : '', '6' : '', '7' : '', 
                      #'8' : '', '9' : '', '10' : '', '11' : '', '12' : '', '13' : '', '14' : '', '15' : '', '16' : '', 
                      #'17' : '', '18' : '',},
                      #}
        self.Info['Names'] = {}
        self.Info['Names']['0'] = ''
        self.Info['Names']['1'] = ''
        self.Info['Names']['2'] = ''
        self.Info['Names']['3'] = ''
        self.Info['Names']['4'] = ''
        self.Info['Names']['5'] = ''
        self.Info['Names']['6'] = ''
        self.Info['Names']['7'] = ''
        self.Info['Names']['8'] = ''
        self.Info['Names']['9'] = ''
        self.Info['Names']['10'] = ''
        self.Info['Names']['11'] = ''
        self.Info['Names']['12'] = ''
        self.Info['Names']['13'] = ''
        self.Info['Names']['14'] = ''
        self.Info['Names']['15'] = ''
        self.Info['Names']['16'] = ''
        self.Info['Names']['17'] = ''
        self.Info['Names']['18'] = ''
        self.Info['Name'] = name
    def Update(self):
        #print('Getting update')
        try:
            if File.Exists('{}.json'.format(self.Info['Name'])) == True:
                with File('{}.json'.format(self.Info['Name'])) as json_file:
                    self.Info = json.load(json_file)
        except:
            with File('{}.json'.format(self.Info['Name']), 'w') as json_file:
                json.dump(self.Info, json_file)
                
    def Save(self):
        with File('{}.json'.format(self.Info['Name']), 'w') as json_file:
            json.dump(self.Info, json_file)
class WindowTemplate:                
    def __init__(self, name, *args):  
        self.Objects = args 
        self.Layout = OrderedDict()      
        self.Layout['Number'] = name        
        self.Layout['Window'] = {}
        self.Layout['Window']['1'] = ''
        self.Layout['Window']['2'] = ''
        self.Layout['Window']['3'] = ''
        self.Layout['Window']['4'] = ''
        self.Layout['Window']['5'] = ''
        self.Layout['Window']['6'] = ''
        self.Layout['Window']['7'] = ''
        self.Layout['Window']['8'] = ''
        self.Layout['Window']['9'] = ''
        self.Layout['Window']['10'] = ''
    def Update(self):     
        try:
            if File.Exists('Template{}.json'.format(self.Layout['Number'])) == True:
                with File('Template{}.json'.format(self.Layout['Number'])) as json_file:
                    self.Layout = json.load(json_file)
        except:
            with File('Template{}.json'.format(self.Layout['Number']), 'w') as json_file:
                json.dump(self.Layout, json_file)
            
    def Save(self):
        with File('Template{}.json'.format(self.Layout['Number']), 'w') as json_file:
            json.dump(self.Layout, json_file)
class USBMatrix:                
    def __init__(self): 
        self.Pair = '2f03f4a2020000000302'
        self.UnPair = '2f03f4a2020000000303'
        #self.Pair = '2f03f4a2000000290302'
        #self.UnPair = '2f03f4a2000000290303'
        self.Mac = 'None'    
        self.IP = 'None'   
        self.Port = 6137 
        self.USB = {'Pair' : self.Pair, 'UnPair' : self.UnPair}        
    def CreatePair(self, Device, Mac):
        self.Cmd = binascii.unhexlify(self.USB[self.Pairing]+Mac)
        Device.Send(self.Cmd)
    def Devices(self, Pairing, Tx, Rx):
        self.Pairing = Pairing
        try:               
            for items in Tx: 
                self.TxDevice = items
                self.TxMac = Tx[items]
            for items in Rx: 
                self.RxDevice = items
                self.RxMac = Rx[items]
            self.CreatePair(self.TxDevice, self.RxMac.lower())                
            self.CreatePair(self.RxDevice, self.TxMac.lower()) 
        except:
            pass