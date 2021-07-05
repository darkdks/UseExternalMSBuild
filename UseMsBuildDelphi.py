# Script to use external MSBuild in Delphi X7 projects (not tested on other version)
# Created by: Samuel RC 
# Date: 04/07/2021

import sys, os

try: 
    os.path.exists(sys.argv[1])
    xmlFilePath = sys.argv[1]
except:
    print("Error: Invalid path. \nUse script.py <pathToProjectd.proj>")
    sys.exit()

tagOpenPGroup = "<PropertyGroup Condition=\"'$(Cfg_2_Win32)'!=''\">"
tagClosePGroup = "</PropertyGroup>"
tagRemoteDebug = ["<DCC_RemoteDebug>true</DCC_RemoteDebug>\n", "<DCC_RemoteDebug>"]         
tagUseMSBuild = ["<DCC_UseMSBuildExternally>true</DCC_UseMSBuildExternally>\n","<DCC_UseMSBuildExternally>"]

xmlFile = open(xmlFilePath,'r')
xmlText = xmlFile.readlines()
xmlFile.close()

def findTag(axmlText, aTag, startIndex, endIndex):
    for index, line in enumerate(axmlText):
        if index < startIndex: 
            continue
        if index > endIndex:
            break
        if aTag in line: 
            return index

idxOpenPGroup = findTag(xmlText, tagOpenPGroup, 0, len(xmlText))
idxClosePGroup = findTag(xmlText, tagClosePGroup, idxOpenPGroup, len(xmlText))
idxTagRemoteDebug = findTag(xmlText, tagRemoteDebug[1], idxOpenPGroup, idxClosePGroup)
idxUseMSBuild = findTag(xmlText, tagUseMSBuild[1], idxOpenPGroup, idxClosePGroup)
indentSpaceCount = len(xmlText[idxOpenPGroup]) -  len(xmlText[idxOpenPGroup].lstrip()) + 4

if idxTagRemoteDebug:  
    xmlText[idxTagRemoteDebug] = (' ' * indentSpaceCount) + tagRemoteDebug[0]
    print('tagRemoteDebug updating...')
else:
    xmlText.insert(idxOpenPGroup + 1, (' ' * indentSpaceCount) + tagRemoteDebug[0])
    print('tagRemoteDebug inserting...')

if idxUseMSBuild:  
    xmlText[idxUseMSBuild] = (' ' * indentSpaceCount) + tagUseMSBuild[0]
    print('tagUseMSBuild updating...') 
else:
    xmlText.insert(idxOpenPGroup + 1, (' ' * indentSpaceCount) + tagUseMSBuild[0])
    print('tagUseMSBuild inserting...')  

xmlFile = open(xmlFilePath,'w')
xmlFile.write(''.join(xmlText))
xmlFile.close()
print('Done.')  