from easysnmp import Session
from tkinter import messagebox

class SNMPClient():
    def __init__(self, ip):
        self.sysName = ''
        self.clientIp = ip
        self.clientSession = self.initiateSNMPSession(ip, True)
    
    def initiateSNMPSession(self, ip, v3=False):
        try:
            if (v3):
                session = Session(hostname=ip, community='public', version=3,
                security_level='auth_with_privacy', security_username='MD5DESUser',
                auth_protocol='MD5', auth_password='minhasenha',
                privacy_protocol='DES', privacy_password='minhasenha')
            else:
                session = Session(hostname=ip, community='public', version=2)
            self.sysName = session.get('sysName.0')
            return session
        except Exception as ex:
            self.showIpErrorMessage(ex)
            return ex
       
    def showIpErrorMessage(self, message='This IP is invalid'):
        messagebox.showerror(title='Error', message=message)