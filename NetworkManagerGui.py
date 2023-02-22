from tkinter import *
from tkinter import font
from tkinter import ttk
from SNMPClient import *

class NetworkManagerGui():
    def __init__(self):
        # TODO: refactor name
        self.ipEntryValue = ''
        self.snmpClient = []
          
    def setup (self):
        self.window = Tk()
        self.window.title('Network Manager')
        # self.window.geometry('800x600')
        
        defaultFont = font.nametofont('TkDefaultFont')
        defaultFont.configure(family='futura', size=12)
        mainInfoFrame = ttk.Frame(self.window, padding=10)
        mainInfoFrame.grid(row=1,column=0)
        
        self.createIpInputSection(self.window,0,0)
        self.createDeviceInfoSection(mainInfoFrame,0,0)
        self.createBandwidthUsageSection(mainInfoFrame,0,1)
        
    def start (self):
        self.window.mainloop()
    
    def createIpInputSection (self, parent, row, column):
        ipInputFrame = ttk.Frame(parent, padding=10)
        ipInputFrame.grid(row=row, column=column, sticky='W')
        
        ipRecentLabel = Label(ipInputFrame, text='Recent IPs: ', padx=10)
        # TODO: add recent entries to the listbox
        ipRecentList = Listbox(ipInputFrame)
        
        ipLabel = Label(ipInputFrame, text='IP: ')

        # TODO: use entry to create a SNMP Session
        ipEntryString = StringVar()
        ipEntry = Entry(ipInputFrame, textvariable=ipEntryString)
        ipEntry.bind('<Return>', lambda event: self.receiveIpInput(ipEntry.get(), ipRecentList))
        

        
        ipLabel.pack(side=LEFT)
        ipEntry.pack(side=LEFT)
        ipRecentList.pack(side=RIGHT)
        ipRecentLabel.pack(side=RIGHT)

    def createDeviceInfoSection (self, parent, row, column):    
        deviceInfoFrame = ttk.Frame(parent, padding=10, relief=SUNKEN)
        deviceInfoFrame.grid(row=row, column=column, sticky='W')

        deviceInfoLabel = Label(deviceInfoFrame, text='Device info')
        deviceInfoLabel.grid(row=0, column=0, sticky='W')

        deviceInfoText = Label(deviceInfoFrame, text='Agent\'s device info goes here')
        deviceInfoText.grid(row=1, column=0)
        
    def createBandwidthUsageSection (self, window, row, column): 
        deviceUsageFrame = ttk.Frame(window, padding=10, relief=SUNKEN)
        deviceUsageFrame.grid(row=row, column=column, sticky='W')

        deviceUsageLabel = Label(deviceUsageFrame, text='Bandwidth Usage')
        deviceUsageLabel.grid(row=0, column=0, sticky='W')

        deviceUsageText = Label(deviceUsageFrame, text='Agent\'s bandwidth usage goes here')
        deviceUsageText.grid(row=1, column=0)

 
    def receiveIpInput(self, input, recentIpsList):
        self.setSNMPClientIp(input)
        self.setRecentIps(input, recentIpsList)
    
    def setSNMPClientIp (self, ip):
        self.snmpClient = SNMPClient(ip)
        
    def setRecentIps (self, ip, recentIpsList):
        recentIpsList.insert(0,ip)