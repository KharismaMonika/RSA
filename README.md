# RSA
Tugas 4 Keamanan Jaringan Implementasi Algoritma RSA

### Kelompok 8 KIJ F
+ 5114100076 M. Faishal Ilham
+ 5114100092 Kharisma Monika D. P.

### Pengertian RSA 
     RSA di bidang kriptografi adalah sebuah algoritma pada enkripsi public key. RSA merupakan algoritma pertama yang cocok untuk digital signature seperti halnya ekripsi, dan salah satu yang paling maju dalam bidang kriptografi public key. RSA masih digunakan secara luas dalam protokol electronic commerce, dan dipercaya dalam mengamnkan dengan menggunakan kunci yang cukup panjang.
     Kekuatan algoritma ini terletak pada proses eksponensial, dan pemfaktoran bilangan menjadi 2 bilangan prima yang hingga kini perlu waktu yang lama untuk melakukan pemfaktorannya. Algoritma ini dinamakan sesuai dengan nama penemunya, Ron Rivest, Adi Shamir dan Adleman(Rivest-Shamir-Adleman) yang dipublikasikan pada tahun 1977 di MIT, menjawab tantangan yang diberikan algoritma pertukaran kunci Diffie Hellman.

### Pembuatan Kunci 
- Semisal Alice berkeinginan untuk mengizinkan Bob untuk mengirimkan kepadanya sebuah pesan pribadi (private message) melalui media transmisi yang tidak aman (insecure). Alice melakukan langkah-langkah berikut untuk membuat pasangan kunci public key dan private key:

    - Pilih dua bilangan prima p ≠ q secara acak dan terpisah untuk tiap-tiap p dan q. Hitung N = p q. N hasil perkalian dari p dikalikan dengan q.
    - Hitung φ = (p-1)(q-1).
    - Pilih bilangan bulat (integer) antara satu dan φ (1 < e < φ) yang juga merupakan koprima dari φ.
    - Hitung d hingga d e ≡ 1 (mod φ).
- bilangan prima dapat diuji probabilitasnya menggunakan Fermat's little theorem- a^(n-1) mod n = 1 jika n adalah bilangan prima, diuji dengan beberapa nilai a menghasilkan kemungkinan yang tinggi bahwa n ialah bilangan prima. Carmichael numbers (angka-angka Carmichael) dapat melalui pengujian dari seluruh a, tetapi hal ini sangatlah langka.
- langkah 3 dan 4 dapat dihasilkan dengan algoritma extended Euclidean; lihat juga aritmetika modular.
- langkah 4 dapat dihasilkan dengan menemukan integer x sehingga d = (x(p-1)(q-1) + 1)/e menghasilkan bilangan bulat, kemudian menggunakan nilai dari d (mod (p-1)(q-1));
- langkah 2 PKCS#1 v2.1 menggunakan &lamda; = lcm(p-1, q-1) selain daripada φ = (p-1)(q-1)).


- Pada public key terdiri atas:

    N, modulus yang digunakan.
    e, eksponen publik (sering juga disebut eksponen enkripsi).


- Pada private key terdiri atas:

    N, modulus yang digunakan, digunakan pula pada public key.
    d, eksponen pribadi (sering juga disebut eksponen dekripsi), yang harus dijaga kerahasiaannya.

- Biasanya, berbeda dari bentuk private key (termasuk parameter CRT):

    p dan q, bilangan prima dari pembangkitan kunci.
    d mod (p-1) dan d mod (q-1) (dikenal sebagai dmp1 dan dmq1).
    (1/q) mod p (dikenal sebagai iqmp).

- Bentuk ini membuat proses dekripsi lebih cepat dan signing menggunakan Chinese Remainder Theorem (CRT). Dalam bentuk ini, seluruh bagian dari private key harus dijaga kerahasiaannya.

- Alice mengirimkan public key kepada Bob, dan tetap merahasiakan private key yang digunakan. p dan q sangat sensitif dikarenakan merupakan faktorial dari N, dan membuat perhitungan dari d menghasilkan e. Jika p dan q tidak disimpan dalam bentuk CRT dari private key, maka p dan q telah terhapus bersama nilai-nilai lain dari proses pembangkitan kunci.

### Proses Enkripsi
- Misalkan Bob ingin mengirim pesan m ke Alice. Bob mengubah m menjadi angka n < N, menggunakan protokol yang sebelumnya telah disepakati dan dikenal sebagai padding scheme.

- Maka Bob memiliki n dan mengetahui N dan e, yang telah diumumkan oleh Alice. Bob kemudian menghitung ciphertext c yang terkait pada n:

         {\displaystyle c=n^{e}\mod {N}} {\displaystyle c=n^{e}\mod {N}}
- Perhitungan tersebut dapat diselesaikan dengan cepat menggunakan metode exponentiation by squaring. Bob kemudian mengirimkan c kepada Alice.

### Proses Dekripsi 
