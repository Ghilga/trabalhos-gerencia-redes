from tkinter import *
from tkinter import font
from tkinter import ttk
from SNMPClient import *

class NetworkManagerGui():
    def __init__(self):
        self.deviceInfoFrame = []
        self.bandwidthUsageFrame = []
        self.ipEntryValue = ''
        self.snmpClient = []
        self.deviceInfosOID = ['sysName.0',
            'sysUpTimeInstance',
            'ifNumber.0',
            'sysServices.0',
            'sysContact.0',
        ]
        self.deviceInfosName = { 'sysName.0' : 'System Name: ',
            'sysUpTimeInstance' : 'Uptime: ',
            'ifNumber.0' : 'Available Interfaces Quantity: ',
            'sysServices.0' : 'Available Services: ',
            'sysContact.0' : 'Admin Contact: '
        }
        self.bandwidthInfosOID = ['ifSpeed.2',
            'snmpInPkts.0',
            'snmpOutPkts.0',
            'ifInOctets.2',
            'ifOutOctets.2'
        ]
        self.bandwidthInfosName = {'ifSpeed.2' : 'Transmission Speed: ',
            'snmpInPkts.0' : 'Input Packets: ',
            'snmpOutPkts.0' : 'Output Packets: ',
            'ifInOctets.2' : 'Input Octets: ',
            'ifOutOctets.2' : 'Output Octets: '
        }
          
    def setup (self):
        self.window = Tk()
        self.window.title('Network Manager')
        self.window.geometry('800x600')
        
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
        ipRecentList = Listbox(ipInputFrame)
        ipRecentList.bind('<Double-1>', lambda event: self.receiveIpInput(ipRecentList.selection_get()))
        ipRecentList.bind('<Return>', lambda event: self.receiveIpInput(ipRecentList.selection_get()), add='+')
        
        ipLabel = Label(ipInputFrame, text='IP: ')

        ipEntryString = StringVar()
        ipEntry = Entry(ipInputFrame, textvariable=ipEntryString)
        ipEntry.bind('<Return>', lambda event: self.receiveIpInput(ipEntry.get(), ipRecentList))
        
        ipLabel.pack(side=LEFT)
        ipEntry.pack(side=LEFT)
        ipRecentList.pack(side=RIGHT)
        ipRecentLabel.pack(side=RIGHT)

    def createDeviceInfoSection (self, parent, row, column):    
        self.deviceInfoFrame = ttk.Frame(parent, padding=10, relief=SUNKEN)
        self.deviceInfoFrame.grid(row=row, column=column, sticky='W')

        deviceInfoLabel = Label(self.deviceInfoFrame, text='Device info')
        deviceInfoLabel.pack(side=TOP)

    def createBandwidthUsageSection (self, parent, row, column): 
        self.bandwidthUsageFrame = ttk.Frame(parent, padding=10, relief=SUNKEN)
        self.bandwidthUsageFrame.grid(row=row, column=column, sticky='W')

        deviceUsageLabel = Label(self.bandwidthUsageFrame, text='Bandwidth Info')
        deviceUsageLabel.pack(side=TOP)

    def receiveIpInput(self, input, recentIpsList=None):
        self.setSNMPClientIp(input)
        
        if (recentIpsList):
            self.setRecentIps(input, recentIpsList)
        
        self.createDeviceInfos(self.deviceInfoFrame, self.snmpClient.clientSession)
        self.createBandwidthInfos(self.bandwidthUsageFrame, self.snmpClient.clientSession)
    
    def setSNMPClientIp (self, ip):
        self.snmpClient = SNMPClient(ip)
        
    def setRecentIps (self, ip, recentIpsList):
        recentIpsList.insert(0,ip)

    def destroyChildrenWidgets (self, parent):
        for widget in parent.winfo_children():
            widget.destroy()

    def createDeviceInfos (self, parent, snmpClient):
        self.destroyChildrenWidgets(parent)
        deviceInfoLabel = Label(parent, text='Device info')
        deviceInfoLabel.pack(side=TOP)

        for infoOID in self.deviceInfosOID:
            infoText = self.getFormattedInfoText(infoOID, snmpClient.get(infoOID).value, self.deviceInfosName)
            infoLabel = Label(parent, text=infoText)
            infoLabel.pack(side=TOP, anchor='w')
    
    def createBandwidthInfos(self, parent, snmpClient):
        self.destroyChildrenWidgets(parent)
        bandwidthInfoLabel = Label(parent, text='Bandwidth Info')
        bandwidthInfoLabel.pack(side=TOP)

        for infoOID in self.bandwidthInfosOID:
            infoText = self.getFormattedInfoText(infoOID, snmpClient.get(infoOID).value, self.bandwidthInfosName)
            infoLabel = Label(parent, text=infoText)
            infoLabel.pack(side=TOP, anchor='w')

    def getFormattedInfoText (self, infoOID, value, nameMap):
        infoText = ''
        if (infoOID == 'ifSpeed.2'):
            infoText = nameMap[infoOID] + str(int(value)/1000000) + ' MB/s'
        elif (infoOID == 'sysUpTimeInstance'):
            infoText = nameMap[infoOID] + str(int(value)*100) + ' s'
        else:
            infoText = nameMap[infoOID] + value
        return infoText