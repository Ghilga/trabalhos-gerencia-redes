from tkinter import *
from tkinter import font
from tkinter import ttk

def main ():
    window = Tk()
    window.title('Network Manager')
    # window.geometry('800x600')
    
    defaultFont = font.nametofont('TkDefaultFont')
    defaultFont.configure(family='futura', size=12)

    mainInfoFrame = ttk.Frame(window, padding=10)
    mainInfoFrame.grid(row=1,column=0)
    
    createIpInputSection(window,0,0)
    createDeviceInfoSection(mainInfoFrame,0,0)
    createBandwidthUsageSection(mainInfoFrame,0,1)

    window.mainloop()

def createIpInputSection (parent, row, column):
    ipInputFrame = ttk.Frame(parent, padding=10)
    ipInputFrame.grid(row=row, column=column, sticky='W')
    
    ipLabel = Label(ipInputFrame, text='IP: ')
    ipLabel.grid(row=0,column=0)

    # TODO: use entry to create a SNMP Session
    ipEntry = Entry(ipInputFrame)
    ipEntry.grid(row=0, column=1)

    ipRecentLabel = Label(ipInputFrame, text='Recent IPs: ', padx=20)
    ipRecentLabel.grid(row=0,column=2)

    # TODO: add recent entries to the listbox
    ipRecentList = Listbox(ipInputFrame)
    ipRecentList.insert(0, 'ip 1')
    ipRecentList.grid(row=0, column=3)

def createDeviceInfoSection (parent, row, column):    
    deviceInfoFrame = ttk.Frame(parent, padding=10, relief=SUNKEN)
    deviceInfoFrame.grid(row=row, column=column, sticky='W')

    deviceInfoLabel = Label(deviceInfoFrame, text='Device info')
    deviceInfoLabel.grid(row=0, column=0, sticky='W')

    deviceInfoText = Label(deviceInfoFrame, text='Agent\'s device info goes here')
    deviceInfoText.grid(row=1, column=0)
    
def createBandwidthUsageSection (window, row, column): 
    deviceUsageFrame = ttk.Frame(window, padding=10, relief=SUNKEN)
    deviceUsageFrame.grid(row=row, column=column, sticky='W')

    deviceUsageLabel = Label(deviceUsageFrame, text='Bandwidth Usage')
    deviceUsageLabel.grid(row=0, column=0, sticky='W')

    deviceUsageText = Label(deviceUsageFrame, text='Agent\'s bandwidth usage goes here')
    deviceUsageText.grid(row=1, column=0)
    
if __name__ == '__main__':
    main()