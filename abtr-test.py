import uuid
import time
import socket

# Constants
PTMP_IDENTIFIER = "PTMP"
PTMP_VERSION = 1
DEFAULT_IPC_PORT = 39000
TEXT_ENCODING = 1
BINARY_ENCODING = 2
ENCRYPTION_NONE = 1
COMPRESSION_NONE = 1
AUTHENTICATION_CLEARTEXT = 1
AUTHENTICATION_SIMPLE = 2
AUTHENTICATION_MD5 = 4
KEEP_ALIVE_PERIOD = 60  # seconds, note not implemented in this example, keep alives are PTMP message type 6

# Internal Call ID needs to be kept to differentiate between calls
call_id = 0

constants = {
    PTMP_IDENTIFIER: "PTMP", PTMP_VERSION: 1, DEFAULT_IPC_PORT: 39000, TEXT_ENCODING: 1, BINARY_ENCODING: 2, ENCRYPTION_NONE: 1, COMPRESSION_NONE: 1, AUTHENTICATION_CLEARTEXT: 1, AUTHENTICATION_SIMPLE: 2, AUTHENTICATION_MD5: 4, KEEP_ALIVE_PERIOD: 60  # seconds, note not implemented in this example, keep alives are PTMP message type 6
}

class AutoPT:
    def __init__(self, constants, server_address, username, password):
        self.protocol = constants[PTMP_IDENTIFIER]
        self.version = constants[PTMP_VERSION]
        self.port = constants[DEFAULT_IPC_PORT]
        self.t_encoding = constants[TEXT_ENCODING]
        self.b_encoding = constants[BINARY_ENCODING]
        self.encryption = constants[ENCRYPTION_NONE]
        self.compression = constants[COMPRESSION_NONE]
        self.auth_clear = constants[AUTHENTICATION_CLEARTEXT]
        self.auth_simple = constants[AUTHENTICATION_SIMPLE]
        self.auth_md5 = constants[AUTHENTICATION_MD5]
        self.keep_alive = constants[KEEP_ALIVE_PERIOD]

        self.server_address = (server_address, self.port)
        self.username = username
        self.password = password
        self.total_calls = 0

        # On creation of an AutoPT object it'll initialize a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    def connect(self):
            self.sock.connect(self.server_address)
            self.sock.settimeout(1) #timeout waiting for data after 1 second
            print("Connected.")

            # Negotiation
            print("Sending negotiation request...")
            timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
            app_id = str(uuid.uuid4())
            reserved = ":PTVER9.0.0.0000"
            negotiation_string = f"{self.protocol}\0{self.version}\0{app_id}\0{self.t_encoding}\0{self.encryption}\0{self.compression}\0{self.auth_clear}\0{timestamp}\0{self.keep_alive}\0{reserved}\0"
            encoded_value = negotiation_string.encode('utf-8') + b'\0'
            type = str(0).encode('utf-8') + b'\0' # type is 0 for negotiation request message
            length = str(len(type+encoded_value)).encode('utf-8') + b'\0'
            request = length+type+encoded_value
            print(request)
            self.sock.sendall(request)
            print("Negotiation request sent.")
            print("Receiving negotiation response...")
            """Receives a text-encoded message from the socket."""
            try:
                while True:
                    data = self.sock.recv(1024)
                    if not data:
                        break
                    print(f"Received: {data}")
            except socket.timeout:
                pass

            # Authentication
            print("Sending authentication request...")
            username = self.username
            authentication_request_string = f"{username}"
            encoded_value = authentication_request_string.encode('utf-8') + b'\0'
            type = str(2).encode('utf-8') + b'\0' # type is 2 for authentication request message
            length = str(len(type+encoded_value)).encode('utf-8') + b'\0'
            request = length+type+encoded_value
            print(request)
            self.sock.sendall(request)
            print("Authentication request sent.")
            print("Receiving authentication challenge...")
            try:
                while True:
                    data = self.sock.recv(1024)
                    if not data:
                        break
                    print(f"Received: {data}")
            except socket.timeout:
                pass
            print("Sending authentication response...")
            password = self.password 
            reserved = "" # currently unused
            authentication_response_string = f"{username}\0{password}\0{reserved}\0"
            encoded_value = authentication_response_string.encode('utf-8') + b'\0'
            type = str(4).encode('utf-8') + b'\0' # type is 4 for authentication response message
            length = str(len(type+encoded_value)).encode('utf-8') + b'\0'
            request = length+type+encoded_value
            print(request)
            self.sock.sendall(request)
            print("Authentication response sent.")
            print("Receiving authentication status...")
            try:
                while True:
                    data = self.sock.recv(1024)
                    if not data:
                        break
                    print(f"Received: {data}")
            except socket.timeout:
                pass

    # Utilities

    def send_packet(self, ipc_call_string):
        # This function just formats the IPC calls you make into a packet for CPT 
        encoded_value = ipc_call_string.encode('utf-8')
        type = str(100).encode('utf-8') + b'\0' # PTMP message type is between 100 and 199 for IPC call messages
        length = str(len(type+encoded_value)).encode('utf-8') + b'\0'
        request = length+type+encoded_value
        
        
        print(request)
        print("IPC call sent.")
        self.sock.sendall(request)
        print("Receiving IPC Response...")
        try:
            while True:
                data = self.sock.recv(1024)
                if not data:
                    break
                print(f"Received: {data}")
                return data
        except socket.timeout:
            pass

    # API
    def console_log(self, msg):
        self.total_calls = self.total_calls + 1
        call_id = self.total_calls
        
        # This will change for each command in the API
        # appWindow [STOP] 0 [STOP] writeToPT
        call_name = "appWindow\0 0 \0writeToPT"

        arg_type = 9 # Tells PT to interperet the incoming info as a string
        args = msg
        ipc_call_string = f"{call_id}\0{call_name}\0{arg_type}\0{args}\0 0 \0"  # the extra   "0 \0"   at the end (not including the \0 after args) tells PT the command ends.
        self.send_packet(ipc_call_string)

server_address = '127.0.0.1'
username = "net.ihitc.ptmptest"  # Replace with your registered ExApp ID
password = "cisco"  # Replace with your ExApp key

PT = AutoPT(constants, server_address, username, password)
PT.connect()
PT.console_log("HELLO WORLD!")