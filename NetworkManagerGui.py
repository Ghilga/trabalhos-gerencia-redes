from tkinter import *
from tkinter import font
from tkinter import ttk
from SNMPClient import *
from MonitoringThread import *
import time

class NetworkManagerGui():
    def __init__(self):
        self.deviceInfoFrame = []
        self.bandwidthUsageFrame = []
        self.ipEntryValue = ''
        self.snmpClient = []
        self.deviceInfosName = {
            'sysName.0' : 'System Name: ',
            'sysUpTimeInstance' : 'Uptime: ',
            'ifNumber.0' : 'Available Interfaces Quantity: ',
            'sysServices.0' : 'Available Services: ',
            'sysContact.0' : 'Admin Contact: '
        }
        self.bandwidthInfosName = {
            'ifSpeed.2' : 'Transmission Speed: ',
            'ifOperStatus.2' : 'Interface operational status: ',
            'ifOutErrors.2' : 'Outbound packets with error: ',
            'ifInErrors.2' : 'Inbound packets with error: ',
            'ifInOctets.2' : 'Input Octets: ',
            'ifOutOctets.2' : 'Output Octets: ',
            'ipInReceives.0' : 'Received IP datagrams: ',
            'ipOutRequests.0' : 'Sent IP datagrams: ',
            'snmpInPkts.0' : 'SNMP Input Packets: ',
            'snmpOutPkts.0' : 'SNMP Output Packets: '
        }
          
    def setup (self):
        self.window = Tk()
        self.window.title('Network Manager')
        self.window.geometry('800x600')
        
        defaultFont = font.nametofont('TkDefaultFont')
        defaultFont.configure(family='futura', size=12)
        authenticationFrame = ttk.Frame(self.window, padding=10)
        mainInfoFrame = ttk.Frame(self.window, padding=10)
        authenticationFrame.pack(side=TOP)
        mainInfoFrame.pack(side=TOP)
        
        self.createLoginSection(authenticationFrame)
        self.createDeviceInfoSection(mainInfoFrame)
        self.createBandwidthUsageSection(mainInfoFrame)
        
    def start (self):
        self.window.mainloop()
    
    def createLoginSection (self, parent):
        loginFrame = ttk.Frame(parent, padding=10)
        ipLabel = Label(loginFrame, text='IP: ')
        ipEntryString = StringVar()
        ipEntry = Entry(loginFrame, textvariable=ipEntryString)
        ipEntry.bind('<Return>', lambda event: self.registerNewSNMP(ipEntry.get(), usernameInput.get(),passwordInput.get(), ipRecentList))
      
        timeLabel = Label(loginFrame, text='Monitoring Time (s): ')
        self.timeEntryString = StringVar()
        self.timeEntryString = Entry(loginFrame, textvariable=self.timeEntryString)
        self.timeEntryString.bind('<Return>', lambda event: self.registerNewSNMP(ipEntry.get(), usernameInput.get(),passwordInput.get(), ipRecentList))


        usernameInputString = StringVar()
        usernameInputLabel = Label(loginFrame, text='Username: ')
        usernameInput = Entry(loginFrame, textvariable=usernameInputString)
        usernameInput.bind('<Return>', lambda event: self.registerNewSNMP(ipEntry.get(), usernameInput.get(),passwordInput.get(), ipRecentList))

        passwordInputString = StringVar()
        passwordInputLabel = Label(loginFrame, text='Password: ')
        passwordInput = Entry(loginFrame, textvariable=passwordInputString, show='*')
        passwordInput.bind('<Return>', lambda event: self.registerNewSNMP(ipEntry.get(), usernameInput.get(),passwordInput.get(), ipRecentList))

        ipRecentFrame = ttk.Frame(parent, padding=10)
        ipRecentLabel = Label(ipRecentFrame, text='Recent IPs: ', padx=10)
        ipRecentList = Listbox(ipRecentFrame)
        ipRecentList.bind('<Double-1>', lambda event: self.registerNewSNMP(ipRecentList.selection_get(), usernameInput.get(),passwordInput.get()))
        ipRecentList.bind('<Return>', lambda event: self.registerNewSNMP(ipRecentList.selection_get(), usernameInput.get(),passwordInput.get()), add='+')
        
        # Login inputs frame
        loginFrame.pack(side=LEFT)
        usernameInputLabel.grid(row=0, column=0)
        usernameInput.grid(row=0, column=1)
        passwordInputLabel.grid(row=1, column=0)
        passwordInput.grid(row=1, column=1)
        ipLabel.grid(row=2, column=0)
        ipEntry.grid(row=2, column=1)
        timeLabel.grid(row=3, column=0)
        self.timeEntryString.grid(row=3, column=1)

        # Recent ips frame
        ipRecentFrame.pack(side=RIGHT)
        ipRecentLabel.grid(row=0, column=0)
        ipRecentList.grid(row=0, column=1)


    def createDeviceInfoSection (self, parent):    
        self.deviceInfoFrame = ttk.Frame(parent, padding=10, relief=SUNKEN)
        self.deviceInfoFrame.pack(side=LEFT, anchor='nw')

        deviceInfoLabel = Label(self.deviceInfoFrame, text='Device info')
        deviceInfoLabel.pack(side=TOP)

    def createBandwidthUsageSection (self, parent): 
        self.bandwidthUsageFrame = ttk.Frame(parent, padding=10, relief=SUNKEN)
        self.bandwidthUsageFrame.pack(side=RIGHT, anchor='ne')

        deviceUsageLabel = Label(self.bandwidthUsageFrame, text='Bandwidth Info')
        deviceUsageLabel.pack(side=TOP)

    def registerNewSNMP(self, ip, username, password, recentIpsList=None):
        self.startMonitoring(ip, username, password, recentIpsList)   

    def getDevicesInfo(self):
        print('get devices info')
        self.createDeviceInfos(self.deviceInfoFrame, self.snmpClient.clientSession)
        self.createBandwidthInfos(self.bandwidthUsageFrame, self.snmpClient.clientSession)

    def startMonitoring(self, ip, username, password, recentIpsList=None):
        currentTime = 0
        if (not self.snmpClient or self.snmpClient.ip != ip):
            self.setSNMPClientIp(ip, username, password)
            if (recentIpsList):
                self.setRecentIps(ip, recentIpsList)
        self.getDevicesInfo()

        # while currentTime < int(self.timeEntryString.get()): 
            # try:
            # except Exception as ex:
                # print(ex)
                # time.sleep(1)
        # self.setSNMPClientIp(ip, username, password)
            
            # time.sleep(1)S
            # currentTime += 1
        #self.monitoringThread = MonitoringThread(int(self.timeEntryString.get()), self.getDevicesInfo)
        #self.monitoringThread.start()
        #self.monitoringThread.join()

    def setSNMPClientIp (self, ip, username, password):
        self.snmpClient = SNMPClient(ip, username, password)
        
    def setRecentIps (self, ip, recentIpsList):
        recentIpsList.insert(0,ip)

    def destroyChildrenWidgets (self, parent):
        for widget in parent.winfo_children():
            widget.destroy()

    def createDeviceInfos (self, parent, snmpClient):
        self.destroyChildrenWidgets(parent)
        deviceInfoLabel = Label(parent, text='Device info')
        deviceInfoLabel.pack(side=TOP)

        for infoOID in self.deviceInfosName:
            infoText = self.getFormattedInfoText(infoOID, snmpClient.get(infoOID).value, self.deviceInfosName[infoOID])
            infoLabel = Label(parent, text=infoText)
            infoLabel.pack(side=TOP, anchor='w')
        
        parent.after(2000, self.createDeviceInfos, parent, snmpClient)
    
    def createBandwidthInfos(self, parent, snmpClient):
        self.destroyChildrenWidgets(parent)
        bandwidthInfoLabel = Label(parent, text='Bandwidth Info')
        bandwidthInfoLabel.pack(side=TOP)

        for infoOID in self.bandwidthInfosName:
            infoText = self.getFormattedInfoText(infoOID, snmpClient.get(infoOID).value, self.bandwidthInfosName[infoOID])
            infoLabel = Label(parent, text=infoText)
            infoLabel.pack(side=TOP, anchor='w')
            
        parent.after(2000, self.createBandwidthInfos, parent, snmpClient)

    def getFormattedInfoText (self, infoOID, value, infoTemplateText):
        infoText = ''
        if (infoOID == 'ifSpeed.2'):
            infoText = infoTemplateText + str(int(value)/1000000) + ' MB/s'
        elif (infoOID == 'sysUpTimeInstance'):
            infoText = infoTemplateText + str(int(value)*100) + ' s'
        else:
            infoText = infoTemplateText + value
        return infoText