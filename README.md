# Proyek Analisis Data: Brazilian E-Commerce Public Dataset (Olist) 🛍️

Proyek akhir analisis data ini dikembangkan untuk memenuhi kriteria kelulusan kelas **"Belajar Fundamental Analisis Data"** di **Dicoding Indonesia**. Proyek ini mencakup seluruh siklus analisis data mulai dari *Data Wrangling*, *Exploratory Data Analysis* (EDA), *Data Visualization*, hingga pengembangan *Interactive Dashboard* berbasis **Streamlit**.

---

## 📌 Biodata Pengembang
- **Nama:** Gilbert Finsen Zakaria Lian
- **Email:** glian6020@gmail.com
- **ID Dicoding:** ds269b6y0676

---

## 🎯 Pertanyaan Bisnis (SMART Question Framework)

1. **Pertanyaan 1 (Kategori Produk & Revenue):**
   > *Kategori produk apa saja yang menghasilkan total pendapatan (revenue) tertinggi dan terendah pada platform e-commerce Olist sepanjang periode 2017 hingga 2018, dan bagaimana dinamika penjualannya?*
   - **Specific:** Mengidentifikasi 5 kategori teratas dan 5 kategori terbawah berdasarkan total revenue di platform Olist.
   - **Measurable:** Dihitung dari total nilai pesanan (*Gross Merchandise Value* / GMV) dalam mata uang Brazilian Real (BRL).
   - **Action-Oriented:** Manajemen dapat mengalokasikan anggaran promosi dan kemitraan penjual ke kategori unggulan, serta merestrukturisasi kategori yang tidak produktif.
   - **Relevant:** Berdampak langsung pada strategi kurasi katalog produk dan pertumbuhan pendapatan perusahaan.
   - **Time-bound:** Dibatasi secara spesifik pada periode transaksi tahun 2017 hingga 2018.

2. **Pertanyaan 2 (Logistik & Kepuasan Pelanggan):**
   > *Bagaimana pengaruh selisih waktu pengiriman aktual terhadap estimasi pengiriman (delivery delay) terhadap skor kepuasan pelanggan (review score) pada pesanan berstatus delivered selama tahun 2017-2018?*
   - **Specific:** Meneliti disparitas ulasan ulasan pelanggan antara pesanan yang tiba tepat waktu (*On-Time / Early*) vs pesanan yang terlambat (*Late*).
   - **Measurable:** Diukur dengan rata-rata skor ulasan (skala 1 s/d 5) dan proporsi distribusi bintang ulasan.
   - **Action-Oriented:** Menjadi dasar peninjauan SLA ekspedisi logistik, pembaruan algoritma estimasi tiba, dan otomasi kompensasi keterlambatan.
   - **Relevant:** Kepuasan pengiriman merupakan pilar utama retensi pengguna dan reputasi platform e-commerce.
   - **Time-bound:** Dianalisis pada pesanan berstatus *delivered* sepanjang 2017 hingga 2018.

---

## 🚀 Fitur Analisis Lanjutan (Kriteria Bintang 5)
Proyek ini mengimplementasikan teknik analisis lanjutan relevan tanpa algoritma machine learning:
1. **RFM Analysis (Recency, Frequency, Monetary):** Segmentasi perilaku bertransaksi konsumen untuk mengidentifikasi pelanggan paling aktif, bernilai tinggi, dan berisiko churn.
2. **Geospatial Analysis:** Menganalisis konsentrasi geografis pembeli dan penjual di seluruh negara bagian (*Federative Units*) Brazil serta disparitas kecepatan logistik antarwilayah.
3. **Clustering / Manual Binning:** Pengelompokan kelompok pengeluaran (*Spending Buckets*) dan klasifikasi durasi keterlambatan logistik.

---

## 📂 Struktur Direktori Proyek

```text
submission/
├── dashboard/
│   ├── main_data.csv       # Dataset terintegrasi & bersih untuk dashboard
│   └── dashboard.py        # Kode utama dashboard interaktif Streamlit
├── data/
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── notebook.ipynb          # Berkas Jupyter Notebook (sudah tereksekusi lengkap)
├── README.md               # Dokumentasi proyek dan panduan instalasi
├── requirements.txt        # Daftar dependensi library Python
└── url.txt                 # Tautan dashboard live di Streamlit Community Cloud
```

---

## 💻 Panduan Menjalankan Dashboard Secara Lokal

### 1. Prasyarat Sistem
- Python versi 3.9 atau lebih baru.
- Terminal / PowerShell / Command Prompt.

### 2. Kloning / Ekstrak Berkas Proyek
Buka direktori proyek:
```bash
cd "Fundamental Analisis Data"
```

### 3. Membuat dan Mengaktifkan Virtual Environment (Disarankan)
- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 4. Instalasi Dependensi
Jalankan perintah berikut untuk menginstal seluruh pustaka yang dibutuhkan:
```bash
pip install -r requirements.txt
```

### 5. Menjalankan Dashboard Streamlit
Jalankan aplikasi streamlit dari folder utama:
```bash
streamlit run dashboard/dashboard.py
```
Aplikasi dashboard akan otomatis terbuka di peramban web default Anda pada alamat `http://localhost:8501`.

---

## 🌐 Deployment ke Streamlit Community Cloud

Proyek ini telah dikonfigurasi agar siap di-deploy langsung ke **Streamlit Community Cloud**:
1. Unggah berkas proyek ke repositori GitHub Anda.
2. Buka [share.streamlit.io](https://share.streamlit.io/) dan hubungkan dengan akun GitHub Anda.
3. Pilih repositori, branch `main`, dan set *Main file path* ke: `dashboard/dashboard.py`.
4. Klik **Deploy**!
5. Tautan dashboard dapat dituliskan ke dalam berkas `url.txt`.

---

## 📊 Rangkuman Kesimpulan & Rekomendasi Aksi

### Kesimpulan Utama
1. **Dominasi Kategori Revenue:** Tiga kategori dengan pendapatan tertinggi adalah `health_beauty` (R$ 1,22 Juta), `watches_gifts` (R$ 1,16 Juta), dan `bed_bath_table` (R$ 1,02 Juta). Sebaliknya, kategori terbawah seperti `security_and_services` hanya mencatatkan pendapatan R$ 283.
2. **Dampak Keterlambatan Logistik:** Pengiriman tepat waktu menghasilkan kepuasan rata-rata **4,29 / 5,0** (62,5% bintang 5). Namun, keterlambatan pengiriman merontokkan skor kepuasan hingga **2,57 / 5,0**, di mana **46,2%** konsumen memberikan bintang 1.
3. **Pola Perilaku RFM & Geografis:** Mayoritas pelanggan adalah pembeli satu kali (frekuensi 1,03), namun pembeli berulang memiliki nilai transaksi sangat tinggi. Wilayah São Paulo (SP) mendominasi lebih dari 41% total transaksi e-commerce.

### Rekomendasi Action Items
1. **Fokus Alokasi Anggaran:** Lipatgandakan investasi kampanye dan kemitraan penjual pada kategori pilar (*health_beauty*, *watches_gifts*, *bed_bath_table*). Lakukan bundling produk untuk kategori dengan transaksi mini.
2. **Otomasi Kompensasi Logistik:** Bangun sistem peringatan dini keterlambatan dan secara otomatis berikan voucher diskon/cashback sebelum paket tiba jika terjadi keterlambatan kurir, guna memitigasi risiko review bintang 1.
3. **Program Loyalitas Pengguna:** Buat program membership bertingkat (*Tiered Loyalty Club*) yang menargetkan segmen pelanggan *Medium* dan *High Spender* dengan penawaran gratis ongkir bersyarat guna meningkatkan *repeat order rate*.
