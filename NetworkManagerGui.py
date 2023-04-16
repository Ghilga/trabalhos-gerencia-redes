from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import Canvas
from SNMPClient import *
from MonitoringThread import *
from AttacksClassifier import *
import time

class NetworkManagerGui():
    def __init__(self):
        self.networkAttacksClassifier = AttacksClassifier()
        self.deviceInfoFrame = []
        self.bandwidthUsageFrame = []
        self.networkStatusFrame = []
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
        self.networkStatusMIBs = [
            'ifOutOctets.2',
            'ifInUcastPkts.2',
            'tcpInSegs.0',
            'udpOutDatagrams.0',
            'udpInErrors.0',
            'ipInDelivers.0',
            'ipOutDiscards.0',
            'icmpInDestUnreachs.0',
            'icmpOutEchoReps.0'
        ]
        # self.networkStatusMIBs = ['ifInOctets.2', 'ifOutOctets.2', 'ifOutDiscards.2', 'ifInUcastPkts.2',
        #     'ifInNUcastPkts.2', 'ifInDiscards.2', 'ifOutUcastPkts.2',
        #     'ifOutNUcastPkts.2', 'tcpOutRsts.0', 'tcpInSegs.0', 'tcpOutSegs.0',
        #     'tcpPassiveOpens.0', 'tcpRetransSegs.0', 'tcpCurrEstab.0', 'tcpEstabResets.0',
        #     'tcpActiveOpens.0', 'udpInDatagrams.0', 'udpOutDatagrams.0', 'udpInErrors.0',
        #     'udpNoPorts.0', 'ipInReceives.0', 'ipInDelivers.0', 'ipOutRequests.0',
        #     'ipOutDiscards.0', 'ipInDiscards.0', 'ipForwDatagrams.0', 'ipOutNoRoutes.0',
        #     'ipInAddrErrors.0', 'icmpInMsgs.0', 'icmpInDestUnreachs.0', 'icmpOutMsgs.0',
        #     'icmpOutDestUnreachs.0', 'icmpInEchos.0', 'icmpOutEchoReps.0']
        self.chartKeys = {
            'ipInReceives.0' : 0,
            'ipOutRequests.0' : 0,
            'snmpInPkts.0' : 0,
            'snmpOutPkts.0' : 0
        }
          
    def setup (self):
        self.window = Tk()
        self.window.title('Network Manager')
        self.window.geometry('1000x900')
        
        defaultFont = font.nametofont('TkDefaultFont')
        defaultFont.configure(family='futura', size=12)
        authenticationFrame = ttk.Frame(self.window, padding=10)
        mainInfoFrame = ttk.Frame(self.window, padding=10)
        chartFrame = ttk.Frame(self.window, padding=10)
        authenticationFrame.pack(side=TOP)
        mainInfoFrame.pack(side=TOP)
        chartFrame.pack(side=TOP)
        
        self.createLoginSection(authenticationFrame)
        self.createDeviceInfoSection(mainInfoFrame)
        self.createBandwidthUsageSection(mainInfoFrame)
        self.createNetworkStatusSection(mainInfoFrame)
        self.createChartSection(chartFrame)
        
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


        usernameInputString = StringVar(value='MD5DESUser')
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

    def createNetworkStatusSection (self, parent):
        self.networkStatusFrame = ttk.Frame(parent, padding=10, relief=SUNKEN)
        self.networkStatusFrame.pack(side=LEFT, anchor='nw')

        networkStatusLabel = Label(self.networkStatusFrame, text='Network status')
        networkStatusLabel.pack(side=TOP)

    def createChartSection (self, parent): 
        self.chart = ttk.Frame(parent, width=800, height=200, padding=10)
        self.chart.pack(side=BOTTOM)

        chartLabel = Label(self.chart, text='Chart')
        chartLabel.pack(side=TOP)
        self.arrStartY = [0, 80, 130, 180]
        self.colors = ['red', 'blue', 'green', 'yellow']
        self.labels = ['Received IP datagrams', 'Sent IP datagrams', 'SNMP Input Packets', 'SNMP Output Packets']
        self.keys = ['ipInReceives.0', 'ipOutRequests.0', 'snmpInPkts.0', 'snmpOutPkts.0']
        self.valueLabel = {}

        self.chartContainer = Canvas(self.chart, width=800, height=300)
        self.chartContainer.pack(side=TOP)
        # self.drawChartContent()

    def drawChartContent(self):
        for i in range(4): 
            self.drawRectangle(self.keys[i], self.arrStartY[i], self.colors[i])
            self.clearLabels(self.keys[i])
            self.drawLabels(self.keys[i], self.arrStartY[i], self.labels[i])

    def drawRectangle(self, keyIndex, yStart, color):
        maxValues = max([int(val) for val in self.chartKeys.values()])
        itemWidth = int(self.chartKeys[keyIndex]) * 500 / maxValues
        self.chartContainer.create_rectangle(200, yStart+15, itemWidth + 200, yStart + 35, fill=color)

    def drawLabels(self, keyIndex, yStart, label):
        self.chartContainer.create_text(100, yStart + 20, text=label)
        self.valueLabel[keyIndex] = self.chartContainer.create_text(100, yStart + 40, text=self.chartKeys[keyIndex])

    def clearLabels(self, keyIndex):
        if keyIndex in self.valueLabel:
            self.chartContainer.delete(self.valueLabel[keyIndex])

    def registerNewSNMP(self, ip, username, password, recentIpsList=None):
        self.monitoringRefreshTime = int(self.timeEntryString.get())*1000
        self.startMonitoring(ip, username, password, recentIpsList)   

    def getAllInfo(self):
        self.createDeviceInfos(self.deviceInfoFrame, self.snmpClient.clientSession)
        self.createBandwidthInfos(self.bandwidthUsageFrame, self.snmpClient.clientSession)
        self.createNetworkStatusInfos(self.networkStatusFrame, self.snmpClient.clientSession)

    def startMonitoring(self, ip, username, password, recentIpsList=None):
        if (not self.snmpClient or self.snmpClient.ip != ip):
            self.setSNMPClientIp(ip, username, password)
            if (recentIpsList):
                self.setRecentIps(ip, recentIpsList)
        
        self.getAllInfo()

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
        
        parent.after(self.monitoringRefreshTime, self.createDeviceInfos, parent, snmpClient)
    
    def createBandwidthInfos(self, parent, snmpClient):
        self.destroyChildrenWidgets(parent)
        bandwidthInfoLabel = Label(parent, text='Bandwidth Info')
        bandwidthInfoLabel.pack(side=TOP)

        for infoOID in self.bandwidthInfosName:
            data = snmpClient.get(infoOID).value
            if infoOID in self.chartKeys.keys():
                self.chartKeys[infoOID] = data
                # print(infoOID + ': ' + data)
            infoText = self.getFormattedInfoText(infoOID, data, self.bandwidthInfosName[infoOID])
            infoLabel = Label(parent, text=infoText)
            infoLabel.pack(side=TOP, anchor='w')

        self.drawChartContent()
            
        parent.after(self.monitoringRefreshTime, self.createBandwidthInfos, parent, snmpClient)
    
    def createNetworkStatusInfos (self, parent, snmpClient):
        self.destroyChildrenWidgets(parent)
        networkStatusLabel = Label(parent, text='Network status')
        networkStatusLabel.pack(side=TOP)

        networkStatusMIBsValues = self.readNetworkStatusMIBs(snmpClient)
        networkStatusText = self.networkAttacksClassifier.predict(networkStatusMIBsValues)
        textColor = ''
        if (networkStatusText is not ClassesDict.NORMAL):
            textColor = '#f00'

        networkStatus = Label(parent, text=networkStatusText, bg=textColor)
        networkStatus.pack(side=TOP)

        parent.after(self.monitoringRefreshTime, self.createNetworkStatusInfos, parent, snmpClient)

    def getFormattedInfoText (self, infoOID, value, infoTemplateText):
        infoText = ''
        if (infoOID == 'ifSpeed.2'):
            infoText = infoTemplateText + str(int(value)/1000000) + ' MB/s'
        elif (infoOID == 'sysUpTimeInstance'):
            infoText = infoTemplateText + str(int(value)*100) + ' s'
        else:
            infoText = infoTemplateText + value
        return infoText
    
    def readNetworkStatusMIBs (self, snmpClient):
        MIBsValues = []
        for mib in self.networkStatusMIBs:
            MIBsValues.append(int(snmpClient.get(mib).value))
        print(MIBsValues)
        return MIBsValues