# CIDR Calculator - Tugas Kecil Jaringan Komputer (IF3130)

**Oleh Roland Hartanto - 13515107**

### Petunjuk Penggunaan Program
Program yang dibuat berupa file bernama `client.py` yang terdapat pada direktori `src`.
Untuk menjalankan program, pada direktori *root* ketikkan:
```
$ make run
```
Program tidak memerlukan kompilasi karena bahasa python akan diinterpretasi secara otomatis oleh *interpreter*.

### Penjelasan Setiap *Phase*
Pada tugas ini, terdapat 3 *phase*. Berikut ini ketiga *phase* tersebut.

**1. *Phase* 1 - Menentukan *subnet* yang sesuai dengan *host***

Untuk menentukan *subnet* yang sesuai dengan *host*, *subnet* yang dibuat sebaiknya yang dapat mencakup *host* tersebut. Pada program yang dibuat, implementasi yang dilakukan adalah dengan mengubah *byte* terakhir dari *host* menjadi 0 dengan *subnet mask* 24.

Solusi lain yang mungkin adalah dengan membuat *subnet mask* menjadi `0.0.0.0/0`.

**2. *Phase* 2 - Menentukan jumlah *host* yang tersedia dalam subnet**

Jumlah *host* yang tersedia dalam sebuah *subnet* adalah sebagai berikut.
$$
jumlahHost = 2^{32-n}
$$
Pada rumus di atas, n adalah jumlah *bit subnet mask*. Perhitungan tersebut dapat dijelaskan sebagai berikut. Bila ukuran dari IP adalah 4 *byte* (32 *bit*) berarti sisa *bit* 0 adalah 32-n. Karena setiap *bit* dapat berupa angka 0 atau 1, maka jumlah kemungkinannya menjadi 2^(32-n).
 
**3. *Phase* 3 - Menentukan sebuah *host* ada dalam dalam *subnet* atau tidak**

Untuk menentukan sebuah *host* berada dalam sebuah *subnet*, maka dapat dilakukan pemeriksaan dengan menerapkan XOR pada *subnet* dan *host*. Karena dalam 1 *subnet*, seluruh *host* memiliki 1 *subnet* mask dan *subnet* number yang sama, setelah menerapkan XOR, bandingkan nilai hasil perhitungan tersebut dengan jumlah *host* yang mungkin dalam sebuah *subnet*. Apabila jumlahnya lebih sedikit, berarti *host* tersebut berada pada *subnet* tersebut. Selain itu, *host* berada di luar *subnet*.

Untuk mempermudah perhitungan XOR, dilakukan konversi IP *subnet* dan *host* menjadi *integer*.
Misal, untuk IP A.B.C.D, maka konversinya adalah sebagai berikut.
$$
IPtoInt(IP) = 2^{24} * A + 2^{16} * B + 2^{8} * C + D 
$$
Setelah itu, dilakukan XOR *subnet* dengan *host*.
```
result = IPtoInt(subnet) ^ IPtoInt(host)
```
Jika hasil kurang dari jumlah *host* yang mungkin dalam *subnet* tersebut (sesuai dengan perhitungan pada *phase* 2), maka keluaran yang diperoleh adalah 'T'. Kondisi selain itu akan menghasilkan keluaran 'F'.
