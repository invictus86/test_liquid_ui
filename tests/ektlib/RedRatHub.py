#
# Simple Python script to send commands to the RedRatHubCmd application via a socket.
#
# Ethan Johnson, David Blight, Chris Dodge - RedRat Ltd.
#
import socket
import EktError


ip = "192.168.1.96"
port = 40000


class RedRatHub(object):
    def __init__(self):
        self.sock = socket.socket()
        self.sock.settimeout(20)
        # self.socketOpen = False
        try:
            self.sock.connect((ip, port))
        except Exception :
            print "Timeout Error:connect to redrathub timed out ,make sure the redrathub service is started"
            raise EktError.TimeoutError
        self.socketOpen = True

    #
    # Opens the socket to RedRatHubCmd.
    #
    # def OpenSocket(self, ip, port):
    #     self.sock.connect((ip, port))
    #     self.socketOpen = True

    #
    # Closes the RedRatHubCmd socket.
    #

    def CloseSocket(self):
        if self.socketOpen:
            self.sock.close()
            self.socketOpen = False
        else:
            print("Socket failed to close.")

    #
    # Sends a message to the ReadData() function
    #
    def press(self, device_name="RedRat-X 22687",dataset=None,key="KEY_POWER",output="4"):
        if dataset == None:
            dataset_unicode = self.ReadData('hubquery="list datasets"')
            dataset = str(dataset_unicode).split('\n')[1]
            if not dataset:
                raise ValueError('redrathub missing dataset name ')
        message = 'name="%s" dataset="%s" signal="%s" output="%s"' % (device_name,dataset,key,output)
        self.ReadData(message)


    #
    # Reads data back from RedRatHub.
    #
    def ReadData(self, message):
        if not self.socketOpen:
            print("\tSocket has not been opened. Call 'OpenSocket()' first.")
            exit
            
        # Send message
        self.sock.send((message + '\n').encode())
        received = ""

        # Check response. This is either a single line, e.g. "OK\n", or a multi-line response with 
        # '{' and '}' start/end delimiters.
        while True:
            # Receives data
            received += self.sock.recv(64).decode()
            if self.CheckEOM(received):
                return received

                
    #
    # Checks for the end of a message
    #
    def CheckEOM(self, message):
        # Multi-line message
        if ('{' in message):
            return ('}' in message)
        
        # Single line message
        if ("\n" in message):
            return True


redrathub = RedRatHub()

