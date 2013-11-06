import struct
import time
from socket import *
import sys
import argparse
import re
###################
parser = argparse.ArgumentParser(description='Server receives an encrypted message with Cesar algorithm, using the unknown key, and prints the best encrypted result.')
parser.add_argument('-p','--port',type=int, help='The port the server is listening on.', required=True)
parser.add_argument('-k','--key',type=int, help='The key we encrypt the message with', required=False)
parser.add_argument('-d','--dictionary', help='The dictionary we will use to decrypt the message', required=False)
args = vars(parser.parse_args())

isKeyGiven = not(args["key"] is None)
isDictionaryGiven = not(args["dictionary"] is None)

if not isKeyGiven:
  print "No key given."
else:
  print "Key given: " + str(args["key"])

if not isDictionaryGiven:
  print "No dictionary given."
else:
  print "Dictionary given: " + args["dictionary"]

if (not isKeyGiven) and (not isDictionaryGiven):
  print "You have to give either a key or a dictionary to be able to decrypt the message."
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

def getDictionary(filename):
  with open(filename) as f:
    dictionary = f.readlines()
  return dictionary

def isWordInDictionary(word):
  dictionary = getDictionary(args["dictionary"])
  if word + "\n" in dictionary:
    return True
  else:
    return False

def getBestKey(encryptedMessage):
  encryptedWords = re.split("\W+", encryptedMessage)
  possibleKeys = {}
  keyScore = 0
  for encryptedWord in encryptedWords:
    for possibleKey in range(26):
      possibleDecryptedWord = decrypt(encryptedWord, possibleKey)
      if isWordInDictionary(possibleDecryptedWord):
        keyScore += 1
        possibleKeys[possibleKey] = keyScore
    
    score = 0

  return max(possibleKeys, key = possibleKeys.get)

def tryDecrypt(encryptedMessage):
  key = getBestKey(encryptedMessage)
  decryptedMessage = decrypt(encryptedMessage,key)
  return (decryptedMessage, key)


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
      (decryptedMessage,key) = tryDecrypt(data)
      print "Decrypted message: '" + decryptedMessage + "' with key " + str(key) + " determined with dictionary '" + args["dictionary"] + "'"

  except KeyboardInterrupt:
    print "\nThe end.\n"
    sys.exit(0)
