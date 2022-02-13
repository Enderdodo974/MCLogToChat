#!/usr/bin/env python3

#
#   This script allows you to print chat logs from an old session directly in-game
#   with the help of MCRcon (and by setting up a server)
#   
#   usage: python3 mcrcon-log-to-chat.py [-h|--help] [-P|--password PASSWORD] [-p|--port PORT] LOGFILE HOST
#   see 'help mcrcon' or 'mcrcon --help' in a terminal for more infos 
#   
#   positional arguments:
#   LOGFILE                     The log file or log archive or log directory to access log at
#   HOST                        The host to connect to
#   
#   optional arguments:
#   -h, --help                  Show this help message and exit
#   -p, --port                  The port to connect to (default 25575)
#   -P, --password              The password to connect with
#   -i, --input                 If this option is active, you must press enter
#                               in the command line manually to go to next line

from mcrcon import MCRcon
import gzip
from sys import argv
from os import listdir

argv.remove(__file__) # Remove 'mcrcon_log_to_chat.py' to avoid problems with options

class LogToChat():

    def __init__(self) -> None:
        ''' Initialize variables'''
        self.host = None
        self.port = 25575
        self.password = None
        self.logfiles = None
        self.needInput = False
        
    def printUsages(self) -> None:
        ''' Print usage of this script'''
        print('usage: python3 mcrcon-log-to-chat.py [OPTIONS...] LOGFILE HOST\n')

    def getCLArguments(self) -> None :
        ''' Get command line argument (via sys.argv)'''

        if '-h' in argv or '--help' in argv: # Show help and exit
            self.printUsages()
            print('this script allows you to read a log file or a log archive and print the chat logs in a minecraft server using mcrcon')
            print("see 'help mcrcon' or 'mcrcon --help' for more informations\n")
            print('\tpositional arguments:')
            print('\tLOGFILE\t\t\t\tThe log file or log archive or log directory to access log at')
            print('\tHOST\t\t\t\tThe host to connect to\n')
            print('\toptional arguments:')
            print('\t-h, --help\t\t\t\tShow this help message and exit')
            print('\t-p, --port\t\t\t\tThe port to connect to (default 25575)')
            print('\t-P, --password\t\t\t\tThe password to connect with')
            print('\t-i, --input\t\t\t\tIf this option is active, you must manually press enter')
            print('\t\t\t\t\t\tin the command line to go to next line')
            exit(0)
        
        if len(argv) == 0 or len(argv) == 1: # No arguments
            self.printUsages()
            print('Error: you must provide at least two arguments: LOGFILE and HOST')
            exit(0)

        if '-p' in argv or '--port' in argv: # Set rcon port
            try:
                _port = argv.index('-p')
            except ValueError:
                _port = argv.index('--port')
            self.port = argv[_port + 1]

        if '-P' in argv or '--password' in argv: # Set rcon password
            try:
                _password = argv.index('-P')
            except ValueError:
                _password = argv.index('--password')
            self.password = argv[_password + 1]
        
        if '-i' in argv or '--input' in argv: # Press enter to print the next line
            self.needInput = True
        
        if not (argv[-2] == argv[_password + 1] or # Set log files location
                argv[-2] == argv[_port + 1] or 
                argv[-2] in ('-p', '-P', '--port', '--password', '-h',
                             '--help', '-i', '--input')):
            self.logfiles = argv[-2]
        
        if not (argv[-1] == argv[_password + 1] or # Set host to connect to with rcon
                argv[-1] == argv[_port + 1] or 
                argv[-1] in ('-p', '-P', '--port', '--password', '-h',
                             '--help', 'i', '--input')):
            self.host = argv[-1]
    
    def getRcon(self) -> MCRcon:
        ''' Start a Rcon thread'''
        return MCRcon(self.host, self.password, int(self.port))
    
    def listFiles(self) -> list:
        ''' List all files in a directory, or return a file path'''
        
        if self.logfiles.endswith("*"):
            return listdir(self.logfiles[:-1])

        return [self.logfiles]
            
    def logToChat(self) -> None:
        ''' Connect to a Minecraft server console and print chat logs.
        To print the next line you have to manually press enter in the console'''
        
        rcon = self.getRcon()
        rcon.connect() # Connect to the server
        print(f"Connected to {self.host}:{self.port}")
        filesPath = self.listFiles()
        for file in filesPath:
            try:
                if file.endswith('.log.gz'):
                    fileData: gzip.GzipFile = gzip.open(file, 'rt') # Open the archive with gzip
                elif file.endswith('.log'):
                    fileData = open(file, 'r')
            except FileNotFoundError as e:
                print(e)
                exit(0)
            _data = fileData.readlines()
            print(f"Current log file contains {len(_data)} lines")
            
            index = 0
            while index < len(_data):
                if '[CHAT]' not in _data[index]:
                    _data.pop(index)
                    index -= 1
                index += 1
            print(f'Current log file contains {len(_data)} chat lines')
            
            for line in _data:
                commandResult = rcon.command(f'tellraw @a [{{"text":"{line[40:].strip()}"}}]') # Send the tellraw command to the minecraft server
                if len(commandResult) > 1: # Print the error if the command fail
                    print(commandResult)
                
                try:
                    if self.needInput:
                        input(f'{_data.index(line)}: ')
                except KeyboardInterrupt or EOFError:
                    print(f"\nDisconnecting from {self.host}:{self.port}...")
                    rcon.disconnect()
                    fileData.close()
                    exit(0)
            fileData.close()
            print("Opening next archive and closing current opened log file")
        rcon.disconnect()

if __name__ == '__main__':
    Log = LogToChat()
    Log.getCLArguments()
    Log.logToChat()