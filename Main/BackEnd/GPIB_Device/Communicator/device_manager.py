'''
Created on May 21, 2019

@author: Daniel
'''
import importlib
import os

import pyvisa as visa

from Main.BackEnd.GPIB_Device.Communicator import translator
from Main.BackEnd.GPIB_Device.Library import errors
import Main.BackEnd.GPIB_Device.Library as Lib

PLACEHOLDER = "PLACEHOLDER"
GPIB_IDENTIFIER = 'GPIB0::' + PLACEHOLDER + '::INSTR'
LIB_PATH = Lib.__name__
print(LIB_PATH)

def connected(rm, name):
    resources = rm.list_resources()
    return name in resources

def id_to_name(id):
    return GPIB_IDENTIFIER.replace(PLACEHOLDER, id)


class GPIB_Device:

    def __init__(self, id, device_type):
        self.inst = self.connect(id)
        self.configure_library(device_type)

    def connect(self, id):
        id = str(id)
        name = id_to_name(id)
        rm = visa.ResourceManager()

        if not connected(rm, name):
            raise Exception(errors.NOT_CONNECTED_ERROR)

        inst = rm.open_resource(name)
        return inst

    def configure_library(self, device_type):
        device_lib_path = LIB_PATH + "." + device_type
        self.lib_module = importlib.import_module(device_lib_path)
        self.command_lib = self.lib_module.commands
        self.query_lib = self.lib_module.queries
        self.keyword_lib = self.lib_module.keywords

    def write(self, string):
        self.inst.write(string)

    def query(self, query):
        return self.inst.query(query)

    #public methods:

    def execute(self, function, leave_on=False):
        commands = function.get_commands(self.lib_module)

        for command in commands:
            self.write(command)

        self.write(self.command_lib.OUTPUT_ON)
        response = self.query(self.query_lib.READ)
        if not leave_on:
           self.write(self.command_lib.OUTPUT_OFF)
        parsed_response = translator.translate(response)
        return parsed_response

    def output_off(self):
        self.write(self.command_lib.OUTPUT_OFF)
