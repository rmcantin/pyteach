#!/usr/bin/env python
# File to extract id numbers for moodle assignments. Then it generates
# a shell or bat script to rename the subfolders of the assignments.
#
# Author : Ruben Martinez-Cantin
# Date   : 03-26-2011

import optparse
import re
import sys
import os
import unicodedata

# For troubles with Spanish names
def strip_accents(string,encoding):
  return unicodedata.normalize('NFKD', unicode(string, encoding)).encode('ASCII', 'ignore')

def cleanupName(name,encoding):
    name = strip_accents(name,encoding)
    name = name.title()
    return name.replace(' ','')

def generatefiles(inputfile,encoding,urlmoodle,outputfile):
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
      name = cleanupName(value[1],encoding)
      fw.write(mvcommand + ' ' + value[0] + ' ')
      fw.write(name + '\n')
      print name, 'corresponds to ID =', value[0]

def run():
  parser = optparse.OptionParser()
  parser.add_option('-i', '--inputfile', default = 'fundinfo.htm')
  parser.add_option('-e', '--encoding', default = 'utf-8')
  parser.add_option('-u', '--url', default = 'https:\/\/moodle\.unizar\.es')
  parser.add_option('-o', '--outputfile', default = 'rename_all')
  (options, args) = parser.parse_args()
  generatefiles(options.inputfile,options.encoding,options.url,options.outputfile)

if __name__ == "__main__":
  run()
