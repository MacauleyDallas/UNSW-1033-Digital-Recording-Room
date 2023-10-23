## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.ui import Level
from extronlib.system import Timer, Wait, ProgramLog
from extronlib.device import ProcessorDevice, UIDevice
from extronlib.interface import RelayInterface


print(Version())
ProgramLog(Version(),'info')

from Objects import Btns, Labels
from ObjectsModule import ObjectsInitialize, TP, TPME, Counter, Pressed, Momtry
from ConnectionsModule import TCPConnection, ModuleConnection

# Module Imports
import extr_sm_SMP_300_Series_v1_16_3_0 as SMP351
import smsg_display_QMxxR_v1_1_4_0 as Samsung
import entt_lc_DINODE_EthergateMK3_v1_1_1_2 as Enttec

IPData = {
    "PTZ": "10.230.1.11",
    "DMX": "10.230.1.9"
}

# Devices
Processor = ProcessorDevice('ProcessorAlias')
TLP = UIDevice('PanelAlias')

Recorder = SMP351.SerialClass(Processor, 'COM1', Baud=9600, Model='SMP 351')
Displays = Samsung.SerialClass(Processor, 'IRS1', Model='QM32R')
LightboardPower = RelayInterface(Processor, 'RLY1')
Lights = Enttec.EthernetClass(IPData['DMX'], 6454, Model='DIN-ODE')

BtnTLP = ObjectsInitialize(TLP,Btns,Labels)
InputGroup = TPME(BtnTLP.BtnsList, [4,5,7])
PresetGroup = TPME(BtnTLP.BtnsList, [341,342,343])
LayoutGroup = TPME(BtnTLP.BtnsList, [101,102,103,104])
RecTimeGroup = TPME(BtnTLP.BtnsList, [201,202,203,204])
SourceGroup = TPME(BtnTLP.BtnsList, [34,35])
LightGroup = TPME(BtnTLP.BtnsList, [14,15])
TimeRemainLbl = TP(BtnTLP.LblList, 304) # pass thru button object or id number you want   
TimeDurLbl = TP(BtnTLP.LblList, 306)
USBState = TP(BtnTLP.BtnsList, 2)
RecSetupBtn = TP(BtnTLP.BtnsList, 4)
RecBtn = TP(BtnTLP.BtnsList, 301)
CamBtn = TP(BtnTLP.BtnsList, 6) # option selection
PCBtn = TP(BtnTLP.BtnsList, 7)
CamPos = TP(BtnTLP.BtnsList, 45)

Preset1Btn = TP(BtnTLP.BtnsList, 341) # cam presets
Preset2Btn = TP(BtnTLP.BtnsList, 342)
StopRecBtn = TP(BtnTLP.BtnsList, 302)
AudLvl = Level(TLP, 37)
AudLvl.SetRange(-60, 0)

Recorder.devicePassword = 'extron'
Status = {'RecState' : '', 'USBDrive' : '', 'RecRes' : '', 'Select HD' : '1080p', 'RecMode' : '',
          'Select SD' : '720p', 'WB': '2', 'PC' : '1', 'Start' : 'Red',  'Stop' : 'Off',          
          201 : 300, 202 : 600, 203 : 900, 204 : 1800 , 'TimingRemain' : None, 'TimingDur' : None, 
          'State' : {'Start':'Resume'}, '1' : CamBtn.TPbtn, '2' : PCBtn.TPbtn,
          712 : 3, 713 : 4, 714 : 1, 715 : 2, 710 : 'Zoom', 711 : 'Zoom', 'Recorder' : 'Connected',
          341 : Preset1Btn.TPbtn, 342 : Preset2Btn.TPbtn, 14 : 255, 15 : 0, 'Type' : ''}
TLP.ShowPage('1 Welcome')
BtnTLP.LblList[7].SetText('Recorder Ready')


def DisplayPower(state):
    dispStr = 'On' if state else 'Off'
    print('disp pwr', dispStr)
    Displays.Set('Power', dispStr, {'Device ID': '0'})

#@SMPConnect.ConnectionStatus
#def SMPConnection(status):
    #if status[0] == 'SMP':
        #Status['Recorder'] = status
        #if Status['Recorder'][1] in ('Connected','ConnectedAlready'):
            #
        #else:
            #BtnTLP.LblList[7].SetText('Recorder Offline')
@Timer(2)
def StatusPolling(timer, count):
    Recorder.Update('RemainingRecordingTime', {'Drive': 'Primary'})
    Recorder.Update('RemainingRecordingTime', {'Drive': 'Secondary'})
    RecTime = Recorder.ReadStatus('RemainingRecordingTime', {'Drive': 'Primary'})
    RecTimeSec = Recorder.ReadStatus('RemainingRecordingTime', {'Drive': 'Secondary'})
    BtnTLP.LblList[2].SetText(str(RecTime))
    Recorder.Update('RemainingRearUSBStorage')
    Recorder.Update('FileDestination')
    
def BarMeter(timer, count):
    Recorder.Update('AudioLevel', {'L/R': 'Left'})    

def Initialize():
    Recorder.SubscribeStatus('FileDestination', None, SMPStatus)
    Recorder.SubscribeStatus('Record', None, SMPStatus)
    Recorder.SubscribeStatus('RemainingRearUSBStorage', None, SMPStatus)
    Recorder.SubscribeStatus('RemainingFrontUSBStorage', None, SMPStatus)
    Recorder.SubscribeStatus('RemainingRecordingTime', None, SMPStatus)
    Recorder.SubscribeStatus('AudioLevel', None, SMPStatus)
    Displays.SubscribeStatus('Power', None, DisplayStatus)
    Displays.Update('Power', {'Device ID' : 0})
    #Recorder.SubscribeStatus('InputA', None, SMPStatus)
    #Recorder.SubscribeStatus('InputB', None, SMPStatus)
    #Recorder.Update('InputStatus') 
    #Recorder.SubscribeStatus('InputStatus', None, SMPStatus)
    InputGroup.MEGroup.SetCurrent(Status['1'])
    Recorder.Set('InputA', '1')
    Recorder.Update('Record')
    Recorder.Update('FileDestination')
    Recorder.Update('RemainingRearUSBStorage')
    Recorder.Update('RemainingRecordingTime', {'Drive': 'Primary'})
    Recorder.Update('AudioLevel', {'L/R': 'Left'})
    ResetSettings()
    TLP.HideAllPopups()
    print('startup')

def TimerSave(timer, count):
    if count == 30:
        TLP.HideAllPopups()
        TLP.ShowPage('1 Welcome')
        SavingTimer.Stop()
        

SavingTimer = Timer(1, TimerSave)
if SavingTimer.State == 'Running':
    SavingTimer.Stop()



def ReadyCount(timer, count):  
    BtnTLP.LblList[8].SetText(str(10 - count))    
    if count == 3:
        Recorder.Set('Record', 'Start')
    if count == 10:
        TLP.HidePopup('Countdown')
        if Status['RecMode'] != '':
            TLP.SetLEDState(65533, 'Red')
            Status['TimingRemain'].CounterState('Start')
            VUTimer.Restart()
            @Wait(1)
            def StartDur():                    
                Status['TimingDur'].CounterState('Start') 
            RecBtn.TPbtn.SetState(1)                   
            StopRecBtn.TPbtn.SetVisible(True)
            ReadyTimer.Stop()

             
            
ReadyTimer = Timer(1, ReadyCount)
if SavingTimer.State == 'Running':
    SavingTimer.Stop()

#def Shutdown(timer, count):
    #if count == 1:
        #SystemShutdown()
def SystemShutdown():
    Recorder.Set('Record', 'Stop')
    LightboardPower.SetState(0)
    DisplayPower(False)
    ResetSettings()        
    TLP.HideAllPopups()
    TLP.ShowPage('1 Welcome')
    InputGroup.MEGroup.SetCurrent(RecSetupBtn.TPbtn)
    Lights.Set('SendDMX512Data',255, {'Slot': '1'})
    Lights.Set('SendDMX512Data',0, {'Slot': '1'})
    LightsOnTimer.Stop()
    LightsOffTimer.Restart()

def LightsOn(timer, count):
    Lights.Set('SendDMX512Data',255, {'Slot': '1'})

LightsOnTimer = Timer(3, LightsOn)   
LightsOnTimer.Stop()

def LightsOff(timer, count):
    Lights.Set('SendDMX512Data',0, {'Slot': '1'})
    
LightsOffTimer = Timer(3, LightsOff)   
LightsOffTimer.Stop()

def ResetSettings():
    RecBtn.TPbtn.SetState(0)
    TimeRemainLbl.TPbtn.SetText('00:00:00')
    TimeDurLbl.TPbtn.SetText('00:00:00')
    TLP.SetLEDState(65533, 'Off')
    StopRecBtn.TPbtn.SetVisible(False)
    SavingTimer.Stop()
    Status['RecMode'] = ''
    Status['Type'] = ''
    RecTimeGroup.MEGroup.SetCurrent(None)
    if Status['TimingRemain'] != None:
        Status['TimingRemain'].CounterState('Stop') 

def DisplayStatus(Command, Value , Qualifier):
    print('Display', Command, Value , Qualifier)
    
def SMPStatus(Command, Value , Qualifier):
    print(Command, Value , Qualifier)
    if Command == 'FileDestination':            
        if Qualifier['Drive'] == 'Secondary':
        #if Qualifier['Drive'] == 'Primary':
            Status['USBDrive'] = Value
            if Status['USBDrive'] == 'Rear USB':
                USBState.TPbtn.SetState(1)
                BtnTLP.LblList[1].SetText('Press to Begin')
                BtnTLP.LblList[0].SetText('Ready To Record')
                BtnTLP.LblList[6].SetText('')
            else:
                USBState.TPbtn.SetState(0)
                BtnTLP.LblList[1].SetText('Insert USB Drive to Begin')
                BtnTLP.LblList[0].SetText('No USB Drive Connected')
                BtnTLP.LblList[6].SetText('Wait upto 10 seconds for USB to Load')
    elif Command == 'RemainingRearUSBStorage':
        BtnTLP.LblList[3].SetText(str(Value)+Qualifier['Unit'])
    elif Command == 'Record':
        Status['RecState'] = Value       
        if Status['RecState'] == 'Pause':
            Status['TimingRemain'].CounterState(Value) 
            Status['TimingDur'].CounterState(Value)
            TLP.SetLEDBlinking(65533, 'Medium', ['Off', 'Red'])
        elif Status['RecState'] == 'Stop':
            TLP.SetLEDState(65533, Status[Value])
            StopRecBtn.TPbtn.SetVisible(False)
            if  Status['TimingRemain'] != None:
                Status['TimingRemain'].CounterState(Value) 
            if  Status['TimingDur'] != None:
                Status['TimingDur'].CounterState(Value)
            RecBtn.TPbtn.SetState(0)
            TimeRemainLbl.TPbtn.SetText('00:00:00')
            TimeDurLbl.TPbtn.SetText('00:00:00')
        elif Status['RecState'] == 'Start':
            Status['State']['Start']
            TLP.SetLEDState(65533, Status[Value])
            StopRecBtn.TPbtn.SetVisible(True)
    elif Command == 'AudioLevel':
        if Value > -60:
            AudLvl.SetLevel(Value)    
            
#@event(TLP, 'MotionDetected')
#def TLPMotionDetected(interface, state):
    #if state == 'Motion':
        #SleepTimer.Restart()
@event(BtnTLP.BtnsList, ['Pressed','Tapped','Held','Released'])
def TLPBtnsPressed(button, state):
    #SleepTimer.Restart()
    if state == 'Pressed':
        if button.ID == Btns['Panopto']: #Panopto selected
            Status['Type'] = 'Panopto'
            #if Status['Recorder'][1] in ('Connected','ConnectedAlready')
            if Status['Recorder'] in ('Connected','ConnectedAlready'):
                LightsOffTimer.Stop()
                LightsOnTimer.Restart()
                TLP.ShowPage('2 RecordSetup')
                TLP.ShowPopup('RecordSetup')
                InputGroup.MEGroup.SetCurrent(RecSetupBtn.TPbtn)
                DisplayPower(True)
                LightboardPower.SetState(1)

        elif button.ID == Btns['USB']: #usb selected
            #if Status['Recorder'][1] in ('Connected','ConnectedAlready'):
            Status['Type'] = 'USB'
            if Status['Recorder'] in ('Connected','ConnectedAlready'):
                TLP.ShowPage('USB')
        elif button.ID == Btns['Start']:  #usb recording - check usb status before proceeding
            LightsOffTimer.Stop()
            LightsOnTimer.Restart()
            DisplayPower(True)
            LightboardPower.SetState(1)
            
            if Status['USBDrive'] == 'Rear USB':
                TLP.ShowPage('2 RecordSetup')
                TLP.ShowPopup('RecordSetup')
                InputGroup.MEGroup.SetCurrent(RecSetupBtn.TPbtn)                
        elif button.ID in range(101,105): 
            LayoutGroup.MEGroup.SetCurrent(button)
            Recorder.Set('RecallLayoutPreset', button.Name[-1:], {'Inputs': 'Without Inputs'})              
        elif button.ID in range(4,8):
            InputGroup.MEGroup.SetCurrent(button) 
            TLP.ShowPopup(button.Name)            
        elif button.ID == 10:   # quick record
            Pressed(BtnTLP.BtnsList, 34) # camera input
            Pressed(BtnTLP.BtnsList, 5)   # select record controls
            Pressed(BtnTLP.BtnsList, 201) # select 5 minute record
            Pressed(BtnTLP.BtnsList, 301) # start recording
            # # Camera.Set('PresetRecall', '2')  # medium close up

        elif button.ID in range(201,205):
            RecTimeGroup.MEGroup.SetCurrent(button)
            Status['RecMode'] = button.Name        
            if button.ID != 204:           
                print(Status[button.ID])
                Status['TimingRemain'] = Counter(Status[button.ID], 'Down', TLP, TimeRemainLbl.TPbtn)  
            else:
                print(1, 'Up', TLP, TimeRemainLbl.TPbtn)
                Status['TimingRemain'] = Counter(1, 'Up', TLP, TimeRemainLbl.TPbtn)         
            Status['TimingDur'] = Counter(1, 'Up', TLP, TimeDurLbl.TPbtn)            
            global TestStatus
            if Status['TimingRemain'] != None:            
                RemainStatus = Status['TimingRemain']
                @RemainStatus.CounterStatus
                def OnTimeElapsed(TimeState):
                    if TimeState == 'TimeElapsed':              
                        Status['TimingDur'].CounterState('Stop')
                        Recorder.Set('Record', 'Stop')
                        TLP.ShowPopup('Saving')
                        if Status['Type'] == 'USB' :
                            BtnTLP.LblList[9].SetText('Please wait.....Do not remove USB flash drive')
                        else:
                            BtnTLP.LblList[9].SetText('Please wait.....')
                        VUTimer.Stop()
                        RecBtn.TPbtn.SetState(0)
                        StopRecBtn.TPbtn.SetVisible(False)
                        TimeRemainLbl.TPbtn.SetText('00:00:00')
                        TimeDurLbl.TPbtn.SetText('00:00:00')
                        Status['TimingRemain'].CounterState('Stop') 
                        Status['TimingDur'].CounterState('Stop')
                        @Wait(3.8)
                        def SaveWait():
                            TLP.ShowPopup('Finished')
                            if Status['Type'] == 'USB' :
                                BtnTLP.LblList[10].SetText('It is safe to remove USB flash drive')
                            else:
                                BtnTLP.LblList[10].SetText('Recording Saved to Panopto')
                            SavingTimer.Restart()                                     
        elif button.ID == Btns['Extend']:
            if Status['RecState'] in ('Start', 'Pause'):
                if Status['RecMode']  != 'Continuous':            
                    Status['TimingRemain'].CounterState('Add-300')                    
        elif button.ID == 13: # marker
            Recorder.Set(button.Name, None)
            Momtry(button, 0.3)
        elif button.ID == 8: # end session
            SystemShutdown()
            TLP.ShowPage('1 Welcome')
        elif button.ID == 27: # shutdown
            SystemShutdown()
        elif button.ID == 22: # back from usb
            TLP.ShowPage('1 Welcome')
        elif button.ID == 21: #  shutdown?
            TLP.ShowPopup('Shutdown')
        elif button.ID == 23: # cancel shutdown
            TLP.HidePopup('Shutdown')
        elif button.ID == 12: # record again
            TLP.HidePopup('Finished')
            TLP.HidePopup('Saving')
            SavingTimer.Stop()
            TLP.ShowPopup('RecordControls')
        elif button.ID == 20: # redo
            TLP.HidePopup('Finished')
            TLP.HidePopup('Saving')
            SavingTimer.Stop()
            TLP.ShowPopup('RecordSetup')
            #InputGroup.MEGroup.SetCurrent(Status['1])
            InputGroup.MEGroup.SetCurrent(RecSetupBtn.TPbtn)
            
        elif button.ID in (14,15): # lights
            LightGroup.MEGroup.SetCurrent(button)
            if button.ID == 14:
                Lights.Set('SendDMX512Data', 0, {'Slot': '1'})
                Lights.Set('SendDMX512Data', 255, {'Slot': '1'})
                LightsOffTimer.Stop()
                LightsOnTimer.Restart()
            elif button.ID == 15:
                Lights.Set('SendDMX512Data',255, {'Slot': '1'})
                Lights.Set('SendDMX512Data',0, {'Slot': '1'})
                LightsOnTimer.Stop()
                LightsOffTimer.Restart()
                
            #Lights.Set('SendDMX512Data',Status[button.ID], {'Slot': '1'})
            
        elif button.ID in (34,35): # smp inputs
            Recorder.Set('InputA', button.Name)
            SourceGroup.MEGroup.SetCurrent(button)
        elif button.ID == 301: # record button
            if Status['RecState'] == 'Start':
                TLP.SetLEDBlinking(65533, 'Medium', ['Off', 'Red'])
                Recorder.Set('Record', 'Pause') 
                Status['TimingRemain'].CounterState('Pause') 
                Status['TimingDur'].CounterState('Pause')
                button.SetBlinking('Medium', [1, 2]) 
                VUTimer.Pause()
            else:
                if Status['RecState'] == 'Pause':
                    Recorder.Set('Record', 'Start')
                    Status['TimingRemain'].CounterState('Resume')
                    Status['TimingDur'].CounterState('Resume')
                    TLP.SetLEDState(65533, 'Red')
                    button.SetState(1)
                    VUTimer.Restart()
                else:
                    if Status['RecMode'] == '':
                        BtnTLP.LblList[8].SetText('Recording cannot start\nSelect Recording Length in recording setup' ) 
                        TLP.ShowPopup('Countdown',5)
                    else:
                        BtnTLP.LblList[8].SetText('10')
                        ReadyTimer.Restart()
                        TLP.ShowPopup('Countdown')                    
                    #if Status['RecMode'] != '':
                        #Recorder.Set('Record', 'Start')
                        #TLP.SetLEDState(65533, 'Red')
                        #Status['TimingRemain'].CounterState('Start')
                        #VUTimer.Restart()
                        #@Wait(1)
                        #def StartDur():                    
                            #Status['TimingDur'].CounterState('Start') 
                        #button.SetState(1)                   
                        #StopRecBtn.TPbtn.SetVisible(True)
        elif button.ID == 302: #stop record button
            Recorder.Set('Record', 'Stop')
            RecBtn.TPbtn.SetState(0)
            StopRecBtn.TPbtn.SetVisible(False)
            TimeRemainLbl.TPbtn.SetText('00:00:00')
            TimeDurLbl.TPbtn.SetText('00:00:00')
            Status['TimingRemain'].CounterState('Stop') 
            Status['TimingDur'].CounterState('Stop')
            VUTimer.Stop()
            TLP.ShowPopup('Saving')
            if Status['Type'] == 'USB' :
                BtnTLP.LblList[9].SetText('Please wait.....Do not remove USB flash drive')
            else:
                BtnTLP.LblList[9].SetText('Please wait.....')
            @Wait(3.8)
            def SaveWait():
                TLP.ShowPopup('Finished')
                if Status['Type'] == 'USB' :
                    BtnTLP.LblList[10].SetText('It is safe to remove USB flash drive')
                else:
                    BtnTLP.LblList[10].SetText('Recording Saved to Panopto')
                SavingTimer.Restart()
        elif button.ID in range(710,712):   # camera zooming
            button.SetState(1)
            # Camera.Set('Zoom', button.Name, {'Zoom Speed': 35})             
        elif button.ID in range(712,716):   # camera control
            CamPos.TPbtn.SetState(Status[button.ID]) 
            # Camera.Set('PanTilt', button.Name, {'Pan Tilt Speed': 35})        
    elif state == 'Held': 
        if button.ID in(341,342): # camera preset save
            button.SetBlinking('Fast', [0, 1])
            button.SetText('Saved') 
            # Camera.Set('PresetSave', str(button.ID - 340))            
    elif state == 'Tapped':     
        if button.ID in range(710,716):   # camera control
            CamPos.TPbtn.SetState(0)
            button.SetState(0)
            # Camera.Set('PanTilt', 'Stop', {'Pan Tilt Speed': 35})   
            # Camera.Set('Zoom', 'Stop', {'Zoom Speed': 35})
        elif button.ID in(341,342):
            PresetGroup.MEGroup.SetCurrent(Status[button.ID])
            # Camera.Set('PresetRecall', str(button.ID-340)) 
            
        elif button.ID in (14,15): # lights
            LightGroup.MEGroup.SetCurrent(button)
            #print(Status[button.ID])
            Lights.Set('SendDMX512Data',Status[button.ID], {'Slot': '1'})   
    elif state == 'Released': 
        if button.ID in(341,342):
            # Camera.Set('PresetSave', str(button.ID-340))

            button.SetText(button.Name)
            PresetGroup.MEGroup.SetCurrent(Status[button.ID])
        elif button.ID in range(710,712):   # camera zooming
            button.SetState(0)
            # Camera.Set('Zoom', 'Stop', {'Zoom Speed': 35})
        elif button.ID in range(712,716):   # camera control
            CamPos.TPbtn.SetState(0)
            # Camera.Set('PanTilt', 'Stop', {'Pan Tilt Speed': 35}) 

VUTimer = Timer(0.2, BarMeter)
VUTimer.Stop()
#SleepTimer = Timer(3600, Shutdown)
ReadyTimer = Timer(1, ReadyCount)
ReadyTimer.Stop()
Lights.Connect()

Initialize()