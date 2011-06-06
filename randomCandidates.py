#!/usr/bin/env python

import unicodedata
import random

dnihash = "TRWAGMYFPDXBNJZSQVHLCKE"
dir = 'dataCandidates/'

# For troubles with Spanish names
def strip_accents(string):
  return unicodedata.normalize('NFKD',
        unicode(string, 'ISO-8859-1')).encode('ASCII','ignore')


def getRandomDNI():
    num = random.randint(10000000,99999999)
    letra = dnihash[num%23]
    return str(num)+letra

def getRandomName(lines):
    name = random.choice(lines)
    name = strip_accents(name)
    return name.rstrip().title()


def getRandomCode():
    return '5J'+str(random.randint(100,999))+'/'+str(random.randint(100,999))


def generate():
  with open(dir+'nombres.txt','r') as fnom:
    nombres  = fnom.readlines()

  with open(dir+'apellidos.txt','r') as fapp:  
    apellidos = fapp.readlines()

  with open(dir+'ucos.txt','r') as fuco:
    ucos = fuco.readlines()

  codes = [getRandomCode() for i in ucos]
      
  with open(dir+'candid.txt','w') as fcan:
    for i in range(1,100):
      
      fecha = (str(random.randint(1,28))+";"+
               str(random.randint(1,12))+";"+
               str(random.randint(1950,1985)))

      nombrecompleto = (getRandomName(apellidos)+";"+
                        getRandomName(apellidos)+";"+
                        getRandomName(nombres))
      
      nota = str(random.randint(5,9))+"."+str(random.randint(0,9))

      prefs = random.sample(codes,3)
      pstring = str(prefs[1])+";"+str(prefs[2])+";"+str(prefs[0])
      linea = getRandomDNI()+";"+nombrecompleto+";"+fecha+";"+nota+";"+pstring+";"

      print linea
      fcan.write(linea+"\n")

  with open(dir+'puest.txt','w') as fp:
    i=0;
    for uco in ucos:
      fp.write(codes[i]+";"+uco.rstrip()+";\n")
      i=i+1
      
if __name__ == "__main__":
    generate()
