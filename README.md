# MCLogToChat
---
   This script allows you to print chat logs from an old session directly in-game
   with the help of MCRcon (and by setting up a server)
---
   _usage: python3 mcrcon_log_to_chat.py [-h|--help] [-P|--password PASSWORD] [-p|--port PORT] LOGFILE HOST_

   see 'help mcrcon' or 'mcrcon --help' in a terminal for more infos.
   
   _**positional arguments**_:
   ```
   LOGFILE                     The log file or log archive or log directory to access log at
   HOST                        The host to connect to
   ```
   _optional arguments:_
   ```
   -h, --help                  Show this help message and exit
   -p, --port                  The Rcon port to connect to (default 25575)
   -P, --password              The password to connect with
   -i, --input                 If this option is active, you must press enter
                               in the command line manually to go to next line
   ```
   ## Examples:
   ```
   python3 mcrcon_log_to_chat.py --help
   
   python3 mcrcon_log_to_chat.py -p 25575 -P minecraft ~/.minecraft/logs/latest.log 127.0.0.1
   
   python3 mcrcon_log_to_chat.py --port 25575 --password minecraft -i ~/Documents/logs/* 192.168.0.2
   
   ./mcrcon_log_to_chat.py latest.log 127.0.0.1
   ```
   # Tests and bugs
   
   This script has been tested on Linux (Ubuntu 20.04) and work perfectly fine.
   If you have an error, like this:
   ```
   Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  NameError: name 'mcrcon' is not defined
   ```
   Try install the mcrcon module (via pip or manually):
   `pip install mcrcon` or https://pypi.org/project/mcrcon/
   
   Also, if you want to execute the script directly (`./mcrcon_log_to_chat.py`), 
   make sure to have the file executable:
   
   `chmod +x mcrcon_log_to_chat.py`
   
   **If you find another bug, you can report it in the 'Issues' section https://github.com/Enderdodo974/MCLogToChat/issues**
