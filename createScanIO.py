# 	author:  	https://github.com/m0nkeyplay/
# 	file Date: 	2019-07-10
#
# 	purpose: 	Create a new scan based on a json file
#               Use pytenable to create the file
#   Requires:   https://github.com/tenable/pyTenable
#
#   notes:      fill in the following variables as needed per environment
#               ak              <-- Access Key
#               sk              <-- Secret Key
#               proxies         <-- If you use a proxy, set it here.
#               iUser           <-- If you need to impersonate a user fill in username here
#                                   and uncomment tio.users.impersonate(iUser) at the end of the script
import logging
import requests
import json
import os
import time
import datetime
import sys
import signal
from tenable.io import TenableIO

#logging.basicConfig(level=logging.DEBUG)

hello = '##########################################################################\n'
hello +='#\n'
hello +='#                     ^^^^Tenable IO Scan Creator^^^^\n'
hello +='#\n'
hello +='#                     Gather data...\n'
hello +='#                          Create a json template...\n'
hello +='#                              Stop all those clicks in the GUI :-) \n'
hello +='##########################################################################\n'

holdOnCowboy = '++++ It looks like the environment isn\'t set up yet.'
holdOnCowboy +='\nPlease set up the environmental variables first. (ak and sk)\n'
holdOnCowboy +='Once those are set you should be on your way.'

lameCreateError = 'Fatal Error.  Scan was not created.'
lameCreateError += 'Hopefully there is a more indepth error message above this?'

#   CTRL+C handler - from https:/gist.github.com/mikerr/6389549
def handler(signum, frame):
    print("\n^^^^^^Task aborted by user.  Some cleanup may be necessary.")
    exit(0)

signal.signal(signal.SIGINT,handler)

# Environment Variables
log_time = datetime.datetime.now().strftime('%Y%B%d%H%M%p')
cwd = os.getcwd()
ak = ''
sk = ''
iUser = ''

proxies = {}
proxies['https']= ''
proxies['http']= ''

try:
    ak
    sk
    tio = TenableIO(ak,sk,proxies=proxies)
except:
    print(holdOnCowboy)
    exit()

h_key_data = 'accessKey='+ak+'; secretKey='+sk

headers = {}
headers['content-type']= 'application/json'
headers['x-apikeys']= h_key_data

#   URLs for environment data
scan_template_url = 'https://cloud.tenable.com/editor/scan/templates'
policy_template_url = 'https://cloud.tenable.com/editor/policy/templates'
scanners_url = 'https://cloud.tenable.com/scanners'
credentials_url = 'https://cloud.tenable.com/credentials'
policy_url = 'https://cloud.tenable.com/policies'
folders_url = 'https://cloud.tenable.com/folders'
agent_groups_url = 'https://cloud.tenable.com/scanners/0/agent-groups'
timeZones_url = 'https://cloud.tenable.com/scans/timezones'


#   Loopy functions
def explode_dictionary(item):
    for k,v in item.items():
        if type(v) is dict:
            explode_dictionary(v)
        else:
            print(str(k)+': '+str(v))

def print_data(log_file,**kwargs):
    for k, v in kwargs.items():
        if type(v) is dict:
            log_file.write(k+':\n')
            print_data(log_file,**v)
        else:
            log_file.write("{}: {}\n".format(k,v))

def create_log(url,loopThrough):
    log_name = 'IO_'+loopThrough+'-'+log_time+'.txt'
    log  = open(cwd+'/logs/'+log_name, 'w')
    r = requests.get(url, proxies=proxies, headers=headers)
    data = r.json()
    for d in data[loopThrough]:
        print_data(log,**d)
        log.write("***********************\n")
    log.close()
    print(log_name+" was successfully written to logs/ ")

#   Check for the json file
#   This does not check if it's valid - just that it exists
def check_jsonFile():
    theJSON = True
    print("We will need a valid json.")
    while theJSON:
        scanFile = input("Path to your JSON file please:")
        if os.path.exists(scanFile):
            print("File exists. Loading it up...")
            return scanFile
        else:
            print("Please provide the correct path to the json file.")

#   Here we go - get interactive
print(hello)
prep = True
print("The environment files creator will allow you to look for data to populate your JSON file.")
while prep:
    choice = input("Do you want to run environment files creator? y/n: ")
    if choice.lower() == 'y' or choice == 'n':
        seePrep = choice
        break
    else:
        print("^^^^^ y or n please ^^^^^")

if seePrep == 'y':
    print("Creating your environment files.  Please be patient.\n")
    create_log(policy_template_url,'templates')
    create_log(scanners_url,'scanners')
    create_log(policy_url,'policies')
    create_log(folders_url,'folders')
    create_log(credentials_url,'credentials')
    create_log(agent_groups_url,'groups')
    create_log(timeZones_url,'timezones')
    print("\nFiles are complete.\nTake your time.  Look at the files then...\nCreate your json.")
    scanFile = check_jsonFile()
else:
    print("Okay.  Let's get moving with the JSON file.")
    scanFile = check_jsonFile()

#   Open and show the data in json for verification
scanJson = open(scanFile, 'r')
data = json.load(scanJson)
print("Here is what you will be submitting:\n")
for d in data['newScan']:
    explode_dictionary(d)

#   Send it
go = input("\nLook good?\nY to go.  Any other key to quit.")
if go.lower() == 'y':
    print("Attempting to create the scan.")
    for d in data['newScan']:
        template = (d['template'])
        try:
            creds = (d['credentials'])
        except:
            creds = ''
        try:
            compliance = (d['audits'])
        except:
            compliance = ''
        try:
            # Uncommnet below if using impersonation
            #tio.users.impersonate(iUser)
            if compliance and creds:
                #Compliance Scan
                scan = tio.scans.create(template=template,credentials=creds,compliance=compliance,**d["settings"])
            elif creds and not compliance:
                #A scan with Credentials
                scan = tio.scans.create(template=template,credentials=creds,**d["settings"])
            else:
                #A Basic Scan
                scan = tio.scans.create(template=template,**d["settings"])
            newScanName = 'newScan-'+log_time+'.txt'
            newScanLog = open(cwd+'/logs/'+newScanName, 'w')
            for k,v in scan.items():
                newScanLog.write(k+': '+str(v)+'\n')
            print("New Scan created.  Log file: "+newScanName)
            newScanLog.close()
        except:
            exit(lameCreateError)
else:
    exit("That's cool. Fix that json and we can try another time.\Bye.")
