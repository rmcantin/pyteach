#!/usr/bin/env python

import unicodedata
import random

dnihash = "TRWAGMYFPDXBNJZSQVHLCKE"

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
    return ''


def generate():
  with open('nombres.txt','r') as fnom:
      nombres  = fnom.readlines()

  with open('apellidos.txt','r') as fapp:  
      apellidos = fapp.readlines()

  with open('ucos.txt','r') as fuco:
    ucos = fuco.readlines()
      
  with open('candid.txt','w') as fcan:
    for i in range(1,100):
      
      fecha = (str(random.randint(1,28))+";"+
               str(random.randint(1,12))+";"+
               str(random.randint(1950,1985)))

      nombrecompleto = (getRandomName(apellidos)+";"+
                        getRandomName(apellidos)+";"+
                        getRandomName(nombres))
      
      nota = str(random.randint(5,9))+"."+str(random.randint(0,9))

      linea = getRandomDNI()+";"+nombrecompleto+";"+fecha+";"+nota

      print linea
      fcan.write(linea+"\n")

  with open('puestos.txt','w') as fp:
    for i in range(1,50):
      pass

if __name__ == "__main__":
    generate()
