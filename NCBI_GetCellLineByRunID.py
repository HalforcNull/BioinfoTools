# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 12:11:24 2019

@author: runan.yao
"""

import requests
import re

def main():
    idfilename = 'runID.txt'
    try:
        with open(idfilename) as f:
            ids = f.read().splitlines()
    except FileNotFoundError:
        return()
    
    cellLines = []
    for id in ids:
        keyResponse = GetKeyInfo(id)
        key = ParseKey(keyResponse)
        traceResponse = GetTraceInfo(key)
        cellLine = PasrseCellLine(traceResponse)
        cellLines.append(cellLine)
    
    with open('output.txt', 'w') as f:
        for item in cellLines:
            f.write("%s\n" % item)
        
    return()
    

# 1d9b3b98da5c548d2a087be584d181f7
def GetTraceInfo(key):
    url = "https://trace.ncbi.nlm.nih.gov/Traces/study/proxy/run_selector.cgi"
    querystring = {"wt":"json","indent":"true","omitHeader":"true","":""}
    payload = "start=0&rows=1&q=recordset%3A" + key + "&undefined="
    headers = { 'cache-control': "no-cache",'Postman-Token': "216d0d1a-26da-4382-b0ce-9685627ba89d" }
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    return(response.text)

def PasrseCellLine(traceResponse):
    pattern = "cell_line_s\":[ ]*\"(?P<cellline>[\S]+)\""
    m = re.search(pattern, traceResponse)
    cellline = m.group('cellline')
    return(cellline)

# DRR000212
def GetKeyInfo(DRR_id):
    url = "https://trace.ncbi.nlm.nih.gov/Traces/study/"
    querystring = {"acc":DRR_id,"go":"go"}
    payload = ""
    headers = {    'cache-control': "no-cache",    'Postman-Token': "7569a1f7-bac7-4ded-8e46-fbbfc065c9f6"    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    return(response.text)

def ParseKey(keyResponse):
    pattern = "key:\"(?P<key>[\S]+)\""
    m = re.search(pattern, keyResponse)
    key = m.group('key')
    return(key)




if __name__ == '__main__':
    main()
    