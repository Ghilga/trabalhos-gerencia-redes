from easysnmp import Session
from tkinter import messagebox

class SNMPClient():
    def __init__(self, ip, username=None, password=None):
        self.clientSession = self.initiateSNMPSession(ip, username, password, True)
    
    def initiateSNMPSession(self, ip, username=None, password=None, v3=False):
        try:
            if (v3):
                session = Session(hostname=ip, community='public', version=3,
                security_level='auth_with_privacy', security_username=username,
                auth_protocol='MD5', auth_password=password,
                privacy_protocol='DES', privacy_password=password)
            else:
                session = Session(hostname=ip, community='public', version=2)
            
            session.get('sysName.0')
            return session
        except Exception as ex:
            self.showIpErrorMessage(ex)
            return ex
       
    def showIpErrorMessage(self, message='This IP is invalid'):
        messagebox.showerror(title='Error', message=message)