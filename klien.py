import socket
import sys
import math
import pickle
import random

def is_prime(num):
    if num > 1:
        # check for factors
        for i in range(2, num):
            if (num % i) == 0:
                # print(i, "times", num // i, "is", num)
                return False
                break
        else:
            return True
    elif num == 2:
        return True
    elif num < 2:
        return False

# ini cari FPB dengan algoritma Euclidian,
def fpb(a, b):
    cek=is_prime(a)
    if cek is True:
        hasil = b % a
    # while b != 0:
    #     a, b = b, a % b
        return hasil
    elif cek is not True:
        hasil=0
        return hasil

def nyarid(e,phi):
    d=0
    while d!=1:
        e2 = random.randrange(1, phi)
        d = (e2*e)%phi
    return e2

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Bilangan harus prima.')  # kalo di javascript itu notif gtu
    elif p == q:
        raise ValueError('nilai p dan q tidak boleh sama')
    # Menghitung nilai n
    n = p * q

    # Phi adalah o(n)
    phi = (p - 1) * (q - 1)

    # pilih nilai random e
    e = random.randrange(1, phi)

    # setelah memilih random, memastikan bahwa FPB e dan o(n) = 1
    g = fpb(e, phi)
    while g != 1:  # ketika ternyata != 1 maka cari lagi
        e = random.randrange(1, phi)
        g = fpb(e, phi)

    d=nyarid(e,phi)
    return ((e, n), (d, n))

def enkrip(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]  # konversi huruf ke angka per huruf
    # Return the array of bytes
    return cipher

def dekrip(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)

def sign(kode, prk):
    private_key, n = prk
    signature = kode ** int(private_key) % int(n)
    return signature

def verify(rho, public):
    public_key, n = public
    M_aksen = (rho ** int(public_key)) % int(n)
    return M_aksen

kode_sign = int(raw_input("Masukkan kode digital signature Anda : "))
p = int(raw_input("masukkan bilangan prima q (17, 19, 23): "))
q = int(raw_input("Masukkan bilangan prima p harus berbeda dengan bilangan q: "))

public, private = generate_keypair(p, q)
rho = sign(kode_sign, private)
print public
print private
rho2 = str(rho)

sign2 = str(kode_sign)
pstr1 = str(public[0])
pstr2 = str(public[1])

public2 = (sign2, pstr1, pstr2)
data_public=pickle.dumps(public2)
cekpoin=0

while True:
    cekpoin += 1
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = ('127.0.0.1', 11000)
        #print >> sys.stderr, 'connecting to %s port %s' % server_address
        sock.connect(server_address)
        # Send data
        if cekpoin==1:
            data = sock.recv(4096)
            data_arr = pickle.loads(data)

            print 'Received autentikasi dan public key server', repr(data_arr)
            auths = int(data_arr[0])
            p1 = int(data_arr[1])
            q1 = int(data_arr[2])

            sock.send(data_public)
            global publicc
            publicc = (p1,q1)

        message = raw_input('Faishal : ')
        encrypted_msg = enkrip(publicc, message)
        panjang = len(message)
        i=0
        isi = []
        isi.append(rho2)
        while i<panjang:
            isi.append(str(encrypted_msg[i]))
            i+=1

        # print isi
        # print panjang
        # print encrypted_msg
        data_pesan = pickle.dumps(isi)
        sock.send(data_pesan)

        data = sock.recv(4096)
        data_server = pickle.loads(data)
        berapa = len(data_server)

        # print berapa
        autc2 = int(data_server[0])

        # print autc2
        public2 = (p1, q1)
        verifikasi = verify(autc2, public2)
        data_server.pop(0)
        data_server = map(int, data_server)
        dekrips = dekrip(private, data_server)
        if verifikasi == auths:
            print 'Data autentikasi sama! yaitu "%d"' % verifikasi
            print >> sys.stderr, 'received dari Risma : "%s"' % dekrips
        else:
            print 'Data autentikasi berbeda!'
            print >> sys.stderr, 'Bukan dari Risma : "%s"' % dekrips

    finally:
        sock.close()
