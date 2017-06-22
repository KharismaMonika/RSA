import socket
import sys
import math
import pickle
import random

server_address = ('', 11000)

def is_prime(num):
    if num > 1:
        # check for factors
        for i in range(2, num):
            if (num % i) == 0:
                # print(num, "is not a prime number")
                # print(i, "times", num // i, "is", num)
                return False
                break
        else:
            # print(num, "is a prime number")
            return True
    elif num==2:
        return True
    elif num < 2:
        return False

# ini cari FPB dengan algoritma Euclidian,
def fpb(a, b):
    cek = is_prime(a)
    if cek is True:
        hasil = b % a
        return hasil
    elif cek is not True:
        hasil = 0
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
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]  # konversi huruf ke angka per huruf
    # Return the array of bytes
    return cipher

def dekrip(pk, ciphertext):
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)

def sign(kode, prk):
    private_key, n = prk
    signature = (kode ** int(private_key)) % int(n)
    return signature

def verify(rho, public):
    public_key, n = public
    M_aksen = (rho ** int(public_key)) % int(n)
    return M_aksen

mess = input('Masukkan kode digital signature Anda : ')
p = int(raw_input("masukkan bilangan prima q (17, 19, 23): "))
q = int(raw_input("Masukkan bilangan prima p harus berbeda dengan bilangan q: "))

public, private = generate_keypair(p, q)
rho = sign(mess, private)
rho2 = str(rho)
print public
print private
mess2=str(mess)
pstr1 = str(public[0])
pstr2 = str(public[1])

public2 = (mess2, pstr1, pstr2)
data_public=pickle.dumps(public2)

print >> sys.stderr, 'starting up on %s port %s' % server_address
cekpoin=0
while True:
    cekpoin+=1
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(server_address)
    sock.listen(1)

    # print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    if cekpoin==1:
        print >> sys.stderr, 'connection from', client_address
        connection.send(data_public)
        datu = connection.recv(4096)
        data_arr = pickle.loads(datu)

        print 'Received autentikasi dan public key client', repr(data_arr)
        global authc
        authc = int(data_arr[0])
        global p1
        global q1
        p1 = int(data_arr[1])
        q1 = int(data_arr[2])
        global publicc
        publicc = (p1, q1)

    try:
        while True:
            data = connection.recv(4096)
            data_client = pickle.loads(data)
            berapa=len(data_client)

            # print berapa
            autc2 = int(data_client[0])

            print autc2
            public2 = (p1,q1)
            verifikasi = verify(autc2, public2)
            data_client.pop(0)
            data_client = map(int, data_client)
            dekrips = dekrip(private, data_client)
            if verifikasi == authc:
                print 'Data autentikasi sama! yaitu "%d"' % verifikasi
                print >> sys.stderr, 'received dari Risma : "%s"' % dekrips
            else:
                print 'Data autentikasi berbeda!'
                print >> sys.stderr, 'Bukan dari Risma : "%s"' % dekrips

            if dekrip:
                message = raw_input('Risma : ')
                encrypted_msg = enkrip(publicc, message)
                panjang = len(message)
                i = 0
                isi = []
                isi.append(rho2)
                while i < panjang:
                    isi.append(str(encrypted_msg[i]))
                    i += 1
                # print isi
                # print panjang
                # print encrypted_msg
                data_pesan = pickle.dumps(isi)
                connection.send(data_pesan)
                # print >> sys.stderr, 'sending "%s"' % message
            else:
                print >>sys.stderr, 'no more data from', client_address
            break
    finally:
        connection.close()