import requests
import requests.auth
import os
from pprint import pformat  # here only for aesthetic
import time
import datetime
import splunk.clilib.cli_common
import json
import ast
import signal
import sys

class Unbuffered:
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

def get_devices(access_token):
        req = requests.get('https://api.lifx.com/v1/lights/all',headers={'Authorization': 'Bearer '+access_token})
        jsonLights = json.loads(req.text)

        for light in jsonLights:
                sys.stdout.write(json.dumps(light)+'\r\n')
                sys.stdout.write('\r\n')
        return True

#Set stdout to Unbuffered Version
sys.stdout = Unbuffered(sys.stdout)

#Get Splunk Home
splunk_home = os.path.expandvars("$SPLUNK_HOME")


#Read in all Access Tokens from LIFX_tokens.conf
settings = splunk.clilib.cli_common.readConfFile(splunk_home+"/etc/apps/LIFXAddonforSplunk/local/LIFX_tokens.conf")
for item in settings.iteritems():
        for key in item[1].iteritems():
                token = key[1]
                #Create a new process for each access_token
                get_devices(token)
