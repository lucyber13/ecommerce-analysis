import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

#[cite: 1]
# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Analytics · Revolusi Al-Ghifari",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Main background */
.main { background: #0a0f1e; }
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1930 100%);
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #1e293b 0%, #162032 100%);
    border: 1px solid #2d3f5a;
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.kpi-card.teal::before { background: linear-gradient(90deg, #0d9488, #14b8a6); }
.kpi-card.blue::before { background: linear-gradient(90deg, #1d4ed8, #3b82f6); }
.kpi-card.violet::before { background: linear-gradient(90deg, #7c3aed, #8b5cf6); }
.kpi-card.amber::before { background: linear-gradient(90deg, #d97706, #f59e0b); }

.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #f0f9ff;
    line-height: 1.1;
    font-family: 'DM Mono', monospace;
}
.kpi-label {
    font-size: 0.78rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 6px;
}

/* Section headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 32px 0 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #1e293b;
}
.section-number {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #0d9488, #06b6d4);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 700; color: white;
}
.section-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #e2e8f0;
}

/* Insight boxes */
.insight-box {
    background: linear-gradient(135deg, rgba(13,148,136,0.08), rgba(6,182,212,0.05));
    border: 1px solid rgba(13,148,136,0.25);
    border-left: 3px solid #0d9488;
    border-radius: 10px;
    padding: 16px 18px;
    margin: 12px 0;
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.65;
}

/* Page title */
.page-title {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #14b8a6, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  DATA GENERATOR
# ─────────────────────────────────────────────
@st.cache_data
def generate_sample_data():
    """Generate realistic synthetic Olist-like data."""
    np.random.seed(42)
    categories_en = [
        'health_beauty', 'bed_bath_table', 'sports_leisure', 'furniture_decor',
        'computers_accessories', 'housewares', 'watches_gifts', 'telephony',
        'auto', 'toys', 'computers', 'garden_tools', 'cool_stuff',
        'pet_shop', 'baby', 'office_furniture', 'food_drink', 'electronics'
    ]
    
    months = pd.period_range(start='2016-09', end='2018-08', freq='M')
    growth = np.linspace(0.5, 1.2, len(months))
    
    monthly_sales = {}
    for m_idx, month in enumerate(months):
        row = {}
        for cat in categories_en:
            base = 50_000 + np.random.randint(0, 100_000)
            seasonal = 1.0 + 0.2 * np.sin(2 * np.pi * (m_idx % 12) / 12)
            row[cat] = max(0, base * growth[m_idx] * seasonal)
        monthly_sales[month] = row
    
    df = pd.DataFrame(monthly_sales).T
    df.index = df.index.to_timestamp()
    
    review_scores = {cat: np.random.uniform(3.5, 4.8) for cat in categories_en}
    review_df = pd.DataFrame(list(review_scores.items()), columns=['category', 'review_score'])
    
    return df, review_df

# ─────────────────────────────────────────────
#  LOAD & FILTER DATA (NEW: Interaction Logic)
# ─────────────────────────────────────────────
raw_monthly_df, review_df = generate_sample_data()

# ─────────────────────────────────────────────
#  SIDEBAR FILTERS (Kriteria Interaktif)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-size:1.4rem; font-weight:700; color:#14b8a6;'>🛒 E-Commerce</div>", unsafe_allow_html=True)
    
    st.markdown("### 🧭 Navigasi")
    page = st.radio("", ["🏠 Overview", "📈 Tren Penjualan", "💰 Revenue Analysis", "⭐ Sentimen"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### 🛠️ Filter Global")
    
    # 1. Filter Tanggal (Langsung memengaruhi visualisasi)
    min_date = raw_monthly_df.index.min().date()
    max_date = raw_monthly_df.index.max().date()
    
    date_range = st.date_input(
        "Rentang Waktu",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Validasi input tanggal
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    # Apply Filtering
    filtered_df = raw_monthly_df[(raw_monthly_df.index.date >= start_date) & (raw_monthly_df.index.date <= end_date)]

# ─────────────────────────────────────────────
#  HEADER & KPI
# ─────────────────────────────────────────────
st.markdown("<div class='page-title'>E-Commerce Analytics</div>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:#1e293b;'>", unsafe_allow_html=True)

k1, k2, k3 = st.columns(3)
total_rev = filtered_df.sum().sum()
total_cats = len(filtered_df.columns)
avg_monthly = total_rev / max(1, len(filtered_df))

with k1:
    st.markdown(f"<div class='kpi-card teal'><div class='kpi-value'>R$ {total_rev/1e6:.2f}M</div><div class='kpi-label'>Total Revenue</div></div>", unsafe_allow_html=True)
with k2:
    st.markdown(f"<div class='kpi-card blue'><div class='kpi-value'>{total_cats}</div><div class='kpi-label'>Kategori Aktif</div></div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='kpi-card violet'><div class='kpi-value'>R$ {avg_monthly/1e3:.1f}K</div><div class='kpi-label'>Rata-rata Bulanan</div></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGE CONTENT
# ─────────────────────────────────────────────

if "Overview" in page:
    st.markdown("### 📊 Ringkasan Performa")
    # Plotly Chart
    fig = px.area(filtered_df.sum(axis=1), title="Total Revenue Trend", color_discrete_sequence=['#14b8a6'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#94a3b8")
    st.plotly_chart(fig, use_container_width=True)

elif "Tren" in page:
    st.markdown("### 📈 Perbandingan Tren Kategori")
    
    # 2. Filter Interaktif: Multiselect Kategori
    selected_cats = st.multiselect(
        "Pilih Kategori untuk Dibandingkan:",
        options=filtered_df.columns,
        default=['computers', 'computers_accessories']
    )
    
    if selected_cats:
        fig_trend = px.line(filtered_df[selected_cats], markers=True)
        fig_trend.update_layout(hovermode="x unified", template="plotly_dark")
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.warning("Pilih setidaknya satu kategori untuk menampilkan grafik.")

elif "Revenue" in page:
    st.markdown("### 💰 Analisis Pendapatan")
    
    # 3. Filter Interaktif: Slider Top N
    top_n = st.slider("Tampilkan Top N Kategori", 5, 15, 10)
    
    rev_data = filtered_df.sum().sort_values(ascending=False).head(top_n)
    fig_rev = px.bar(rev_data, orientation='h', color=rev_data.values, color_continuous_scale='Teals')
    st.plotly_chart(fig_rev, use_container_width=True)

elif "Sentimen" in page:
    st.markdown("### ⭐ Kepuasan Pelanggan")
    # Filter review data based on categories present in filtered_df
    current_cats = filtered_df.columns
    filtered_reviews = review_df[review_df['category'].isin(current_cats)]
    
    fig_sent = px.scatter(filtered_reviews, x='category', y='review_score', size='review_score', color='review_score')
    st.plotly_chart(fig_sent, use_container_width=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.caption(f"Menampilkan data dari {start_date} hingga {end_date} · Author: Revolusi Al-Ghifari")
