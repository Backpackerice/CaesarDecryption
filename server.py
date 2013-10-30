import struct
import time
from socket import *
import sys
import argparse
###################
parser = argparse.ArgumentParser(description='Server receives an encrypted message with Cesar algorithm, using the unknown key, and prints the best encrypted result.')
parser.add_argument('-p','--port',type=int, help='The port the server is listening on.', required=True)
parser.add_argument('-k','--key',type=int, help='The key we encrypt the message with', required=False)
parser.add_argument('-d','--dictionnary', help='The dictionnary we will use to decrypt the message', required=False)
args = vars(parser.parse_args())

isKeyGiven = not(args["key"] is None)
isDictionnaryGiven = not(args["dictionnary"] is None)

if not isKeyGiven:
  print "No key given."
else:
  print "Key given: " + str(args["key"])

if not isDictionnaryGiven:
  print "No dictionnary given."
else:
  print "Dictionnary given: " + args["dictionnary"]

if (not isKeyGiven) and (not isDictionnaryGiven):
  print "You have to give either a key or a dictionnary to be able to decrypt the message."
  sys.exit(0)
###################
characterOccur = {
"a": 7.68,
"b": 0.8,
"c": 3.32,
"d": 3.6,
"e": 17.76,
"f": 1.06,
"g": 1.10,
"h": 0.64,
"i": 7.23,
"j": 0.19,
"k": 0,
"l": 5.89,
"m": 2.72,
"n": 7.61,
"o": 5.34,
"p": 3.24,
"q": 1.34,
"r": 6.81,
"s": 8.23,
"t": 7.30,
"u": 6.05,
"v": 1.27,
"w": 0,
"x": 0.54,
"y": 0.21,
"z": 0.07
}

encryptedCharacters = [
"a",
"b",
"c",
"d",
"e",
"f",
"g",
"h",
"i",
"j",
"k",
"l",
"m",
"n",
"o",
"p",
"q",
"r",
"s",
"t",
"u",
"v",
"w",
"x",
"y",
"z"
]
###################
def decrypt(encryptedMessage,key):
  decryptedMessage = ""
  
  for character in encryptedMessage:
    if character in encryptedCharacters:
      asciiNumberOfCharacter = ord(character) - 96
      asciiNumberOfDecryptedCharacter = (asciiNumberOfCharacter - key) % 26 or 26
      decryptedCharacter = chr(asciiNumberOfDecryptedCharacter + 96)
      decryptedMessage += str( decryptedCharacter)
    else:
      #print "Character to decrypt " + character + " not in encrypted characters, nothing to do."
      decryptedMessage += str( character)
  
  return decryptedMessage

def getOccurencesFromMessage(message):
  occur = {}
  count = 1
  for character1 in message:

    for character2 in message:
      if character1 == character2:
        count += 1

    occur.setdefault(character1,count)
    count = 1
  
  return occur

def getDictionnary(filename):
  with open(filename) as f:
    dictionnary = f.readlines()
  return dictionnary

def tryDecrypt(encryptedMessage):
  decryptedMessages = []
  dictionnary = getDictionnary(args["dictionnary"])
  for possibleKey in range(26):
    possibleMessage = decrypt(encryptedMessage,possibleKey)
   # print "Possible message: " + possibleMessage + " with key: " + str(possibleKey)
    if possibleMessage+"\n" in dictionnary:
      decryptedMessages.append(possibleMessage)

  return decryptedMessages


###################
# IP UDP
sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
# attachenement a ladresse 4242
sock.bind(('', args["port"]))

print "Listening on port " + str(args["port"])

while True:
  try:
    data, address = sock.recvfrom(1024)
    heure = time.asctime( time.localtime(time.time()) )
    print "[*] %s --- Recu : %s de %s" % (heure, data, address[0])
  
    if isKeyGiven:
      decryptedMessage = decrypt(data,args["key"])
      print "Decrypted message: " + decryptedMessage + " with key: " + str(args["key"]) + "."
    else:
      decryptedMessages = tryDecrypt(data)
      print "Decrypted possible messages: \n:" 
      print decryptedMessages
      print " with dictionnary: " + str(args["dictionnary"]) + "."

  except KeyboardInterrupt:
    print "\nThe end.\n"
    sys.exit(0)
