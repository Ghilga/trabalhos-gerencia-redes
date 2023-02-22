# from easysnmp import Session
from tkinter import messagebox

class SNMPClient():
    def __init__(self, ip):
        self.clientIp = ip
        self.clientSession = self.initiateSNMPSession(ip)
    
    def initiateSNMPSession(self, ip):
        #TODO: start SNMPv3 session and return any exception found to show the error
        try:
            # return Session(hostname=ip, community='public', version=3)
            raise Exception('Timeout')
        except Exception as ex:
            self.showIpErrorMessage(ex)
       
    def showIpErrorMessage(self, message='This IP is invalid'):
        messagebox.showerror(title='Error', message=message)
