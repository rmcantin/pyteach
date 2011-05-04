#!/usr/bin/env python
# File to extract id numbers for moodle assignments. Then it generates
# a shell or bat script to rename the subfolders of the assignments.
#
# Author : Ruben Martinez-Cantin
# Date   : 03-26-2011


import re
import sys
import os
import unicodedata

inputfile = 'fundinfo.htm'
urlmoodle = 'https:\/\/moodle\.unizar\.es'
outputfile = 'rename_all'

# For troubles with Spanish names
def strip_accents(string):
  return unicodedata.normalize('NFKD', unicode(string, 'ISO-8859-1')).encode('ASCII', 'ignore')

def cleanupName(name):
    name = strip_accents(name)
    name = name.title()
    return name.replace(' ','')

with open(inputfile,'r') as f:
    # print source
    source = f.read()
    values = re.findall('<strong><a href="' + urlmoodle +
                        '\/user\/view\.php\?id=' +
                        '([0-9]{5})&amp;course=[0-9]{4}">' +
                        '(.*?)<\/a><\/strong>',
                        source)
    if os.name == 'posix':
        # Linux or Mac OS
        outputfile = outputfile + '.sh'
        header = '#!/bin/sh \n'
        mvcommand = 'mv'
    elif os.name == 'nt':
        # Windows
        outputfile = outputfile + '.bat'
        header = ''
        mvcommand = 'move'
    else:
        sys.exit("Operating system not supported")
        
    with open(outputfile,'w') as fw:
        fw.write(header)
                
        for value in values:
          name = cleanupName(value[1])
          fw.write(mvcommand + ' ' + value[0] + ' ')
          fw.write(name + '\n')
          print name, 'corresponds to ID =', value[0]
 
