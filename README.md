CaesarDecryption
================

Server receiving an encrypted message with Caesar method from a client and decrypting this message.

###Example

	python server.py -p 60000 -d dico.txt

Or:

	python server.py -p 60000 -d dico.txt -k 1
	
Or:

	python server.py -p 60000 -k 1
	
Or:

	python server.py --port 60000 --dictionary dico.txt --key 1