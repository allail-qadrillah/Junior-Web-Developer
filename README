# Aplikasi Inventaris

Aplikasi Inventaris adalah aplikasi berbasis web yang digunakan untuk mengelola barang dan item dalam inventaris. Aplikasi ini memiliki beberapa fitur seperti menambah barang, mengurangi barang, dan menghasilkan laporan mingguan.

## Fitur

1. **Autentikasi**: 
  - Cashier dapat mengurangi jumlah barang.
  - Admin Gudang dapat menambahkan dan mengurangi jumlah barang.
  - Super Admin memiliki akses penuh yaitu edit dan hapus barang.

2. **Tambah Barang**: Menambahkan barang baru dengan form `(Nama, Jumlah, Kategori, Harga Jual, Harga Beli, Struk Pembelian)`. kemudian akan menambahkan item sebanyak jumlah barang yang di-input.

3. **Kurangi Barang**: Mengurangi barang dengan form `(Nama Barang, Jumlah Dikurangi, status)`, jika status yang dipilih adalah sold maka akan menampikann form `Struk Penjualan`. Kemudian akan mengurangi item sebanyak jumlah yang dikurangi.

4. **Filter Tabel**: memfilter data dari tabel dengan Kategori, Status Item, Tanggal item dari barang yang masuk dan Tanggal item dari barang yang keluar (dikurangi)

5. **Laporan Mingguan**: menghasilkan laporan mingguan dalam format PDF.

## Instalasi

1. Buat dan aktifkan virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # Untuk pengguna Unix
    .\env\Scripts\activate  # Untuk pengguna Windows
    ```

2. Instal dependensi:
    ```bash
    pip install -r requirements.txt
    ```

3. Jalankan aplikasi:
    ```bash
    python run.py
    ```

4. Akses Aplikasi:
    - copy url aplikasi dari terminal pada browser
    - pilih role login 
        1. Cashier
            - username = cashier
            - password = cashier
        2. Admin Gudang
            - username = admingudang
            - password = admingudang
        3. Super Admin
            - username = superadmin
            - password = superadmin

## Struktur Direktori Aplikasi

- `app/`
  - `templates/`
    - `base.html`: Template dasar untuk semua halaman.
    - `index.html`: Halaman utama aplikasi.
    - `products.html`: Halaman daftar Barang.
    - `add_product.html`: Formulir untuk menambah Barang baru.
    - `reduce_product.html`: Formulir untuk mengurangi Barang.
    - `edit_product.html`: Formulir untuk mengedit Barang.
    - `items.html`: Halaman detail item.
  - `static/`
    -  `reports/`: Menyimpan file laporan pdf.
    -  `uploads/`: Menyimpan gambar struk.
  - `routes_main.py`: Berisi rute utama aplikasi.
  - `routes_form.py`: Berisi rute untuk formulir.
  - `auth.py`: Berisi authentikasi aplikasi.
  - `database.py`: Berisi manajemen database.
  - `models.py`: Berisi struktur tabel database.
- `config.py`: Berisi konfigurasi database
- `run.py`: Berisi kode menjalankan aplikasi

## Rute Utama

- `/`: Menampilkan Halaman utama sebagai autentikasi.
- `/products`: Menampilkan tabel daftar barang.
- `/products/{id}`: Menampilkan item detail dari barang.
- `/products/add`: Menampilkan formulir penambahan Barang.
- `/products/reduce`: Menampilkan formulir pengurangan Barang.
- `/products/report`: Menghasilkan laporan mingguan dalam format PDF.

# Schema Database
![alt text](/docs/database/schema.png)
Terdapat dua tabel utama: "products" dan "items". Tabel "products" menyimpan informasi umum tentang produk seperti ID, kategori, harga jual, dan harga beli. Sementara itu, tabel "items" melacak item individual dari setiap produk, termasuk waktu masuk dan keluar, status, serta rincian penjualan dan pembelian. Hubungan antara kedua tabel ini dibuat melalui kolom "product_id" yang ada di kedua tabel.

> Mockup aplikasi dapat dilihat di dirketori [./docs/mockup](/docs/mockup/)