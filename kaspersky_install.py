#!/usr/bin/env python

import os
import subprocess
import wget

def downloadPacket(file):
    print ('Downloading ' + file + ' from ksc')
# TODO: install kaspersky web server
    url = srv + file + ver + '.' + packet
    wget.download(url, '/tmp/')

def installPacket(file):
    if "rpm" in packet:
        installCommand = 'rpm -i /tmp/' + file + ver + '.' + packet
    else:
        installCommand = 'dpkg -i /tmp/' + file + ver + '.' + packet
    os.system(installCommand)

def autoinstall(file):
    if ('appdata' in file) and ('x86_64' in ver):
        dirPath = '/opt/kaspersky/klnagent64/lib/bin/setup/'
        os.rename(dirPath + file, dirPath + file + '.orig')
    elif ('appdata' in file) and ('x86_64' not in ver):
        dirPath = '/opt/kaspersky/klnagent/lib/bin/setup/'
        os.rename(dirPath + file, dirPath + file + '.orig')
    elif 'autoinstall' in file:
        dirPath = '/opt/kaspersky/kesl/doc/'
        os.rename(dirPath + file, dirPath + file + '.orig')  
    urlAutoinstall = 'http://mksc.bops.local/' + file
    wget.download(urlAutoinstall, dirPath)
  
def postinstall(file):
    if 'kesl' in file:
        keslPostinstallCommand = "/opt/kaspersky/kesl/bin/kesl-setup.pl"
        os.system(keslPostinstallCommand)
    elif ('klnagent' in file) and ('x86_64' in ver):
        agentPostinstallCommand = "/opt/kaspersky/klnagent64/lib/bin/setup/postinstall.pl"
        os.system(agentPostinstallCommand)
    elif ('klnagent' in file) and ('x86_64' not in ver):
        agentPostinstallCommand = "/opt/kaspersky/klnagent/lib/bin/setup/postinstall.pl"
        os.system(agentPostinstallCommand)
 

ver = os.uname()[-1]

if os.path.isfile("/etc/redhat-release") and ('x86_64' in ver):
    packet = "rpm"
    agentName = "klnagent64-10.5.0-42."
    keslName = "kesl-10.1.0-5960."
elif (not os.path.isfile("/etc/redhat-release")) and ('x86_64' in ver):
    packet = "deb"
    agentName = "klnagent64_10.5.0-42_"
    keslName = "kesl_10.1.0-5960_"
    ver = 'amd_64'
elif os.path.isfile("/etc/redhat-release") and ('x86_64' not in ver):
    packet = "rpm"
    agentName = "klnagent-10.5.1-7."
    keslName = "kesl-10.1.0-5960."
    ver = 'i386'
elif (not os.path.isfile("/etc/redhat-release")) and ('x86_64' not in ver):
    packet = "deb"
    agentName = "klnagent_10.5.1-7_"
    keslName = "kesl_10.1.0-5960_"
    ver = 'i386'

downloadPacket(agentName)
downloadPacket(keslName)

installPacket(agentName)
installPacket(keslName)

autoinstall(appdata.pm)
autoinstall(autoinstall.ini)

postinstall(agentName)
postinstall(keslName)

# downloading & installing key
srv = 'http://mksc.bops.local/'
key = '56CAAC33.key'
keyUrl = srv + key
wget.download(keyUrl, '/tmp/')
keyInstallCommand = '/opt/kaspersky/kesl/bin/kesl-control --install-active-key ' + key
os.system(keyInstallCommand)