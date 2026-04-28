# 🛒 E-Commerce Analytics Dashboard
**Proyek Analisis Data · Revolusi Al-Ghifari**

Dashboard interaktif berbasis Streamlit untuk menganalisis dataset e-commerce publik (Olist Brazil), menjawab 4 pertanyaan bisnis utama melalui visualisasi interaktif.

---

## 📌 Pertanyaan Bisnis yang Dijawab

1. **Tren Penjualan** — Apakah penjualan komputer dan aksesoris komputer bergerak linear?
2. **Korelasi Kategori** — Bagaimana preferensi pelanggan berdasarkan korelasi antar kategori?
3. **Revenue 2017–2018** — Kategori mana yang menghasilkan pendapatan terbesar?
4. **Sentimen Pelanggan** — Kategori mana yang paling disukai dan paling tidak disukai?

---

## 🗂️ Struktur Proyek

```
ecommerce_dashboard/
├── dashboard.py              # Aplikasi utama Streamlit
├── requirements.txt          # Dependensi Python
├── README.md                 # Dokumentasi ini
└── .streamlit/
    └── config.toml           # Konfigurasi tema Streamlit
```

---

## 🖥️ Menjalankan Secara Lokal

### Prasyarat
- Python 3.9 atau lebih baru
- pip (Python package manager)

### Langkah 1 — Clone / Siapkan Folder Proyek

```bash
# Jika menggunakan git
git clone https://github.com/<username>/ecommerce-dashboard.git
cd ecommerce-dashboard

# Atau buat folder baru dan salin file
mkdir ecommerce-dashboard && cd ecommerce-dashboard
# Salin dashboard.py, requirements.txt, dan folder .streamlit ke sini
```

### Langkah 2 — Buat Virtual Environment (Rekomendasi)

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan (Windows)
venv\Scripts\activate

# Aktifkan (Mac/Linux)
source venv/bin/activate
```

### Langkah 3 — Install Dependensi

```bash
pip install -r requirements.txt
```

### Langkah 4 — Jalankan Dashboard

```bash
streamlit run dashboard.py
```

Dashboard akan otomatis terbuka di browser pada `http://localhost:8501`

### Langkah 5 (Opsional) — Gunakan Dataset Asli

Dashboard berjalan dengan **data sampel** secara default. Untuk menggunakan dataset Olist asli:

1. Download dari Kaggle: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
2. Ekstrak file ZIP
3. Di sidebar dashboard, **matikan toggle "Gunakan Data Sampel"**
4. Upload 5 file CSV yang diperlukan:
   - `orders_dataset.csv`
   - `order_items_dataset.csv`
   - `products_dataset.csv`
   - `order_reviews_dataset.csv`
   - `product_category_name_translation.csv`

---

## ☁️ Deploy ke Streamlit Cloud

### Prasyarat
- Akun GitHub (gratis): https://github.com
- Akun Streamlit Community Cloud (gratis): https://streamlit.io/cloud

### Langkah 1 — Push ke GitHub

```bash
# Inisialisasi git repository
git init
git add .
git commit -m "Initial commit: E-Commerce Analytics Dashboard"

# Buat repo baru di GitHub, lalu:
git remote add origin https://github.com/<username>/ecommerce-dashboard.git
git branch -M main
git push -u origin main
```

> **Penting:** Pastikan struktur folder di GitHub adalah:
> ```
> /
> ├── dashboard.py
> ├── requirements.txt
> ├── README.md
> └── .streamlit/
>     └── config.toml
> ```

### Langkah 2 — Login ke Streamlit Cloud

1. Buka https://share.streamlit.io
2. Klik **"Sign in with GitHub"**
3. Authorize akses ke akun GitHub Anda

### Langkah 3 — Deploy Aplikasi

1. Klik tombol **"New app"** (pojok kanan atas)
2. Isi form deployment:

   | Field | Value |
   |-------|-------|
   | **Repository** | `<username>/ecommerce-dashboard` |
   | **Branch** | `main` |
   | **Main file path** | `dashboard.py` |
   | **App URL** | `<nama-app-pilihan>` (opsional) |

3. Klik **"Deploy!"**
4. Tunggu proses build selesai (±2–3 menit pertama kali)
5. Aplikasi akan live di: `https://<nama-app>.streamlit.app`

### Langkah 4 — Verifikasi Deployment

Setelah berhasil deploy, cek:
- ✅ Dashboard terbuka tanpa error
- ✅ KPI cards tampil di bagian atas
- ✅ Semua 5 menu navigasi di sidebar berfungsi
- ✅ Chart interaktif (hover, zoom) berjalan

---

## 🔧 Troubleshooting

### Error: `ModuleNotFoundError`
```bash
# Pastikan requirements.txt sudah benar dan ter-push ke GitHub
# Cek versi Python yang digunakan Streamlit Cloud (3.9+)
```

### Error: `FileNotFoundError` saat upload CSV
- Pastikan nama file CSV **persis sama** dengan yang tertera di sidebar
- Jangan rename file dari Kaggle

### Dashboard lambat loading
- Data sampel di-cache otomatis (`@st.cache_data`) — reload pertama lebih lambat
- Setelah cache terisi, loading sangat cepat

### Chart tidak tampil
- Cek koneksi internet (Google Fonts di-load dari CDN)
- Coba hard refresh browser: `Ctrl+Shift+R` (Windows) / `Cmd+Shift+R` (Mac)

---

## 📊 Fitur Dashboard

| Halaman | Visualisasi | Deskripsi |
|---------|-------------|-----------|
| 🏠 Overview | Line chart + Bar mini | Ringkasan total revenue dan quick insights |
| 📈 Tren Penjualan | Line chart interaktif | Perbandingan bulanan computers vs accessories |
| 🔗 Korelasi | Heatmap korelasi | Matriks korelasi 9 kategori utama |
| 💰 Revenue | Bar chart horizontal | Top N kategori by revenue 2017–2018 |
| ⭐ Sentimen | Dual bar chart | Top/bottom kategori by review score |

---

## 🛠️ Tech Stack

- **Streamlit** `1.40.0` — Web framework
- **Plotly** `5.24.1` — Visualisasi interaktif
- **Pandas** `2.2.3` — Data manipulation
- **NumPy** `1.26.4` — Komputasi numerik

---

## 👤 Author

**Revolusi Al-Ghifari**  
📧 revo.bili0912@gmail.com  
🆔 ID Dicoding: `evolusi`
