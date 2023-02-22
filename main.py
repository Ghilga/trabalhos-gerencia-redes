from SNMPClient import *
from NetworkManagerGui import *

def main ():
    appMainWindow = NetworkManagerGui()
    appMainWindow.setup()
    appMainWindow.start()
    
if __name__ == '__main__':
    main()