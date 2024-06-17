import random
import math

import cv2

# A set will be the collection of prime numbers,
# where we can select random primes p and q
prime = set()

public_key = None
private_key = None
n = None

# We will run the function only once to fill the set of
# prime numbers
def primefiller():
	# Method used to fill the primes set is Sieve of
	# Eratosthenes (a method to collect prime numbers)
	seive = [True] * 250
	seive[0] = False
	seive[1] = False
	for i in range(2, 250):
		for j in range(i * 2, 250, i):
			seive[j] = False

	# Filling the prime numbers
	for i in range(len(seive)):
		if seive[i]:
			prime.add(i)


# Picking a random prime number and erasing that prime
# number from list because p!=q
def pickrandomprime():
	global prime
	k = random.randint(0, len(prime) - 1)
	it = iter(prime)
	for _ in range(k):
		next(it)

	ret = next(it)
	prime.remove(ret)
	return ret


def setkeys():
	global public_key, private_key, n
	prime1 = pickrandomprime() # First prime number
	prime2 = pickrandomprime() # Second prime number

	n = prime1 * prime2 # n = P * Q
	print("n: ", n)
	fi = (prime1 - 1) * (prime2 - 1) # phi(n) = (P - 1) * (Q - 1)

	e = 2
	while True:
		if math.gcd(e, fi) == 1:
			break
		e += 1
		

	print("e ", e)

	# d = (k*Φ(n) + 1) / e for some integer k
	public_key = e

	d = 2
	while True:
		if (d * e) % fi == 1:
			break
		d += 1

	private_key = d


# To encrypt the given number
def encrypt(message):
	global public_key, n
	e = public_key
	encrypted_text = 1
	while e > 0:
		if e%2==1:
			encrypted_text = ((encrypted_text%n)*(message%n))%n
		message = ((message%n)*(message%n))%n
		e >>= 1
	return encrypted_text


# To decrypt the given number
def decrypt(encrypted_text):
	global private_key, n
	d = private_key
	decrypted = 1
	while d > 0:
		if d%2==1:
			decrypted = ((decrypted%n)*(encrypted_text%n))%n
		encrypted_text = ((encrypted_text%n)*(encrypted_text%n))%n
		d >>= 1
	return decrypted


# First converting each character to its ASCII value and
# then encoding it then decoding the number to get the
# ASCII and converting it to character
def message_Encoder(message):
	encoded = []
	# Calling the encrypting function in encoding function
	for letter in message:
		encoded.append(encrypt(ord(letter)))
	return encoded


def message_Decoder(encoded):
	s = ''
	# Calling the decrypting function decoding function
	for num in encoded:
		s += chr(decrypt(num))
	return s


# Extract the R,G,B from each pixel and then encode it.
def image_Encoder(image, row, col):
	print("Starting Image Encryption...")
	for i in range(row):
		for j in range(col):
			r,g,b = image[i, j]
			E1 = encrypt(r)
			E2 = encrypt(g)
			E3 = encrypt(b)
			enc[i][j]=[E1,E2,E3]
			E1=E1%256
			E2=E2%256
			E3=E3%256
			image[i,j]=[E1,E2,E3]
	print("Ending Image Encryption...")

# Decode the encrypted R,G,B of each pixel to get original back.
def image_Decoder(enc_img, row, col):
	print("Starting Image Decryption...")
	for i in range(row):
		for j in range(col):
			r,g,b = enc_img[i][j]
			D1 = decrypt(r)
			D2 = decrypt(g)
			D3 = decrypt(b)
			my_img[i,j] = [D1, D2, D3]
	print("Ending Image Decryption...")






if __name__ == '__main__':
	# create set of prime number
	primefiller()
	
	print(prime)

	setkeys()
	message = "Test Mes sage9999tuyuyuy>"
	# Uncomment below for manual input
	# message = input("Enter the message\n")
	# Calling the encoding function
	coded = message_Encoder(message)

	print("Initial message:")
	print(message)
	print("\n\nThe encoded message(encrypted by public key)\n")
	print(''.join(str(p) for p in coded))
	print("\n\nThe decoded message(decrypted by public key)\n")
	print(''.join(str(p) for p in message_Decoder(coded)))
	print("\n")	



	# Image Encryption and Decryption
	
	my_img = cv2.imread(r'data/LookupCat.png')  
	row,col = my_img.shape[0], my_img.shape[1]

	#The Encoded Image
	enc = [[0 for x in range(col)] for y in range(row)]

	image_Encoder(my_img, row, col)
	image_Decoder(enc, row, col)

	cv2.imshow('cat', my_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()