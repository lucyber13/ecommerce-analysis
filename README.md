# 🛒 E-Commerce Analytics Dashboard
**Proyek Analisis Data · Revolusi Al-Ghifari**

Dashboard interaktif berbasis Streamlit untuk menganalisis dataset e-commerce publik (Olist Brazil), menjawab 4 pertanyaan bisnis utama melalui visualisasi interaktif.

---

## 📌 Pertanyaan Bisnis yang Dijawab

1. **Tren Penjualan** — Apakah penjualan komputer dan aksesoris komputer bergerak linear?
2. **Korelasi Kategori** — Bagaimana preferensi pelanggan berdasarkan korelasi antar kategori?
3. **Revenue 2017–2018** — Kategori mana yang menghasilkan pendapatan terbesar?
4. **Sentimen Pelanggan** — Kategori mana yang paling disukai dan paling tidak disukai?


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


## 👤 Author

**Revolusi Al-Ghifari**  
📧 revo.bili0912@gmail.com  
🆔 ID Dicoding: `evolusi`
