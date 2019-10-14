import threading
import time

from Main.BackEnd.msp430.Communicator.msp430.bsl5.hid import HIDBSL5
import Main.BackEnd.msp430.Library.commands as commands
from Main.BackEnd.msp430.Communicator import translator

DEFAULT_VID = 0x2CDE
DEFAULT_PID = 0xC001

INPUT_TAG = 63
PACKAGE_SIZE = 64
EMPTY_BYTE = 0

COMMUNICATION_DELAY = .2

class msp430Communicator:

    def __init__(self, vid=DEFAULT_VID, pid=DEFAULT_PID):
        self.vid = vid
        self.pid = pid
        self.speaker = HIDBSL5()
        self.PWM_percent = .0

    def connect(self):
        self.speaker.open(vid=self.vid, pid=self.pid)

    def disconnect(self):
        self.speaker.close()

    def receive_data(self):
        return self.speaker.read_report()

    '''
    This method sends a string to the device and returns a decoded string output. You can call it on its own, but ideally 
    you should just make Queries and Commands because the .execute(command) and .evaluate(query) methods call send_string but also contain
    the machinery for parsing the results fully and handling multiple commands at once.
    '''

    def send_string(self, data):
        print(data)
        input=[]
        data_length = len(data)
        input.append(INPUT_TAG)
        input.append(data_length)

        input = self.string_to_byte_array(input=input, string=data, length=len(data))
        input = self.add_padding_bytes(input=input)

        self.speaker.write_report(data=input)
        response = self.speaker.read_report()
        decoded_response = translator.decode_response(response=response, input_data_length=data_length)
        return decoded_response

    def string_to_byte_array(self, input, string, length):
        for i in range(length):
            char = string[i]
            char_as_int = ord(char)
            input.append(char_as_int)
        return input

    def add_padding_bytes(self, input):
        bytes_filled = len(input)
        while bytes_filled < PACKAGE_SIZE:
            input.append(EMPTY_BYTE)
            bytes_filled = len(input)
        return input

    def query(self, query): #function or command works
        strings = query.get_strings()
        for string in strings:
            response = self.send_string(string)
        parsed_response = query.parse(response)
        time.sleep(COMMUNICATION_DELAY)
        return parsed_response

    def execute(self, command):
        strings = command.get_strings()
        for string in strings:
            self.send_string(string)
            time.sleep(COMMUNICATION_DELAY)