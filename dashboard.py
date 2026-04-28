import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

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
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.9rem;
    padding: 6px 0;
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

.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 12px 32px rgba(13,148,136,0.15); }
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
.kpi-delta {
    font-size: 0.82rem;
    color: #34d399;
    margin-top: 8px;
    font-weight: 500;
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
    flex-shrink: 0;
}
.section-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #e2e8f0;
}
.section-subtitle {
    font-size: 0.82rem;
    color: #64748b;
    margin-top: 2px;
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
.insight-box strong { color: #5eead4; }

/* Upload area */
.upload-zone {
    background: #1e293b;
    border: 2px dashed #334155;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    color: #64748b;
    font-size: 0.85rem;
}

/* Page title */
.page-title {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #14b8a6, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
}
.page-subtitle {
    font-size: 0.92rem;
    color: #64748b;
    margin-top: 6px;
}

/* Data badge */
.data-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(52,211,153,0.12);
    border: 1px solid rgba(52,211,153,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    color: #34d399;
    font-weight: 500;
}

/* Divider */
hr { border-color: #1e293b; }

/* Plotly chart container */
.stPlotlyChart { border-radius: 12px; overflow: hidden; }

/* Metrics overide */
[data-testid="metric-container"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SAMPLE DATA GENERATOR (fallback)
# ─────────────────────────────────────────────
@st.cache_data
def generate_sample_data():
    """Generate realistic synthetic Olist-like data for demo purposes."""
    np.random.seed(42)
    n_orders = 12_000
    
    categories_en = [
        'health_beauty', 'bed_bath_table', 'sports_leisure', 'furniture_decor',
        'computers_accessories', 'housewares', 'watches_gifts', 'telephony',
        'auto', 'toys', 'computers', 'garden_tools', 'cool_stuff',
        'pet_shop', 'baby', 'office_furniture', 'food_drink',
        'electronics', 'luggage_accessories', 'stationery',
        'cds_dvds_musicals', 'books_general_interest', 'fashion_bags_accessories',
        'musical_instruments', 'industry_commerce_and_business',
        'construction_tools_safety', 'security_and_services', 'la_cuisine',
        'small_appliances', 'fashion_male_clothing',
    ]
    
    # Monthly sales simulation: 2016-09 to 2018-08
    months = pd.period_range(start='2016-09', end='2018-08', freq='M')
    
    # Revenue weights per category (realistic distribution)
    rev_weights = {
        'health_beauty': 0.14, 'bed_bath_table': 0.12, 'sports_leisure': 0.09,
        'furniture_decor': 0.08, 'computers_accessories': 0.07, 'housewares': 0.06,
        'watches_gifts': 0.06, 'telephony': 0.05, 'auto': 0.05, 'toys': 0.04,
        'computers': 0.04, 'garden_tools': 0.03, 'cool_stuff': 0.03,
        'pet_shop': 0.025, 'baby': 0.025, 'office_furniture': 0.02,
        'food_drink': 0.02, 'electronics': 0.02, 'luggage_accessories': 0.015,
        'stationery': 0.015, 'cds_dvds_musicals': 0.01, 'books_general_interest': 0.01,
        'fashion_bags_accessories': 0.01, 'musical_instruments': 0.008,
        'industry_commerce_and_business': 0.008, 'construction_tools_safety': 0.006,
        'security_and_services': 0.005, 'la_cuisine': 0.005,
        'small_appliances': 0.004, 'fashion_male_clothing': 0.003,
    }
    
    # Growth trend: e-commerce growing over time
    growth = np.linspace(0.5, 1.0, len(months))
    
    monthly_sales = {}
    for m_idx, month in enumerate(months):
        row = {}
        for cat in categories_en:
            base = rev_weights.get(cat, 0.01) * 500_000
            noise = np.random.normal(1.0, 0.25)
            seasonal = 1.0 + 0.3 * np.sin(2 * np.pi * (m_idx % 12) / 12)
            row[cat] = max(0, base * growth[m_idx] * noise * seasonal)
        monthly_sales[month] = row
    
    monthly_df = pd.DataFrame(monthly_sales).T
    monthly_df.index.name = 'sale_month_year'
    
    # ── review scores ──
    review_scores = {
        'cds_dvds_musicals': 4.64, 'books_general_interest': 4.55,
        'fashion_bags_accessories': 4.52, 'musical_instruments': 4.50,
        'la_cuisine': 4.48, 'small_appliances': 4.42,
        'health_beauty': 4.38, 'baby': 4.35, 'food_drink': 4.33,
        'stationery': 4.30, 'pet_shop': 4.27, 'sports_leisure': 4.25,
        'watches_gifts': 4.22, 'toys': 4.19, 'luggage_accessories': 4.15,
        'housewares': 4.12, 'bed_bath_table': 4.10, 'garden_tools': 4.08,
        'electronics': 4.03, 'cool_stuff': 3.98, 'telephony': 3.90,
        'auto': 3.88, 'office_furniture': 3.82, 'computers': 3.79,
        'computers_accessories': 3.75, 'furniture_decor': 3.72,
        'industry_commerce_and_business': 3.68, 'construction_tools_safety': 3.60,
        'fashion_male_clothing': 3.45, 'security_and_services': 2.85,
    }
    
    # ── correlation matrix (realistic) ──
    selected_cats = [
        'health_beauty', 'housewares', 'auto', 'bed_bath_table',
        'furniture_decor', 'computers_accessories', 'sports_leisure',
        'pet_shop', 'watches_gifts',
    ]
    corr_matrix = monthly_df[selected_cats].corr()
    
    # ── summary stats ──
    # 2017-2018 revenue
    period_mask = [(m.year in [2017, 2018]) for m in monthly_df.index]
    rev_2017_2018 = monthly_df[period_mask].sum().sort_values(ascending=False)
    
    # Computers vs accessories monthly
    comp_acc = monthly_df[['computers', 'computers_accessories']].reset_index()
    comp_acc['sale_month_year'] = comp_acc['sale_month_year'].astype(str)
    
    total_revenue = monthly_df.sum().sum()
    total_orders = n_orders
    
    review_df = pd.DataFrame({
        'product_category_name_english': list(review_scores.keys()),
        'review_score': list(review_scores.values()),
    })
    
    return {
        'monthly_df': monthly_df,
        'corr_matrix': corr_matrix,
        'rev_2017_2018': rev_2017_2018,
        'comp_acc': comp_acc,
        'review_df': review_df,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'n_categories': len(categories_en),
        'selected_cats': selected_cats,
    }


# ─────────────────────────────────────────────
#  DATA LOADER (real CSVs if available)
# ─────────────────────────────────────────────
@st.cache_data
def load_real_data(uploaded_files: dict):
    try:
        orders = pd.read_csv(uploaded_files['orders_dataset.csv'])
        order_items = pd.read_csv(uploaded_files['order_items_dataset.csv'])
        products = pd.read_csv(uploaded_files['products_dataset.csv'])
        order_reviews = pd.read_csv(uploaded_files['order_reviews_dataset.csv'])
        translation = pd.read_csv(uploaded_files['product_category_name_translation.csv'])

        # Merge products with translation
        merged_products = products.merge(translation, on='product_category_name', how='left')
        order_items_products = order_items.merge(merged_products, on='product_id', how='left')
        full_sales = order_items_products.merge(orders, on='order_id', how='left')
        full_sales['order_purchase_timestamp'] = pd.to_datetime(full_sales['order_purchase_timestamp'], errors='coerce')
        full_sales['sale_month_year'] = full_sales['order_purchase_timestamp'].dt.to_period('M')

        monthly_df = full_sales.groupby(['sale_month_year', 'product_category_name_english'])['price'].sum().unstack().fillna(0)

        selected_cats = [
            'health_beauty', 'housewares', 'auto', 'bed_bath_table',
            'furniture_decor', 'computers_accessories', 'sports_leisure',
            'pet_shop', 'watches_gifts',
        ]
        valid_cats = [c for c in selected_cats if c in monthly_df.columns]
        corr_matrix = monthly_df[valid_cats].corr()

        period_mask = [(m.year in [2017, 2018]) for m in monthly_df.index]
        rev_2017_2018 = monthly_df[period_mask].sum().sort_values(ascending=False)

        comp_acc_cols = [c for c in ['computers', 'computers_accessories'] if c in monthly_df.columns]
        comp_acc = monthly_df[comp_acc_cols].reset_index()
        comp_acc['sale_month_year'] = comp_acc['sale_month_year'].astype(str)

        order_reviews['review_score'] = pd.to_numeric(order_reviews['review_score'], errors='coerce')
        reviews_merged = order_reviews.merge(full_sales[['order_id', 'product_category_name_english']], on='order_id', how='left')
        review_df = reviews_merged.groupby('product_category_name_english')['review_score'].mean().reset_index()

        return {
            'monthly_df': monthly_df,
            'corr_matrix': corr_matrix,
            'rev_2017_2018': rev_2017_2018,
            'comp_acc': comp_acc,
            'review_df': review_df,
            'total_revenue': full_sales['price'].sum(),
            'total_orders': full_sales['order_id'].nunique(),
            'n_categories': full_sales['product_category_name_english'].nunique(),
            'selected_cats': valid_cats,
        }, None
    except Exception as e:
        return None, str(e)


# ─────────────────────────────────────────────
#  PLOT HELPERS
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(15,23,42,0.6)',
    font=dict(family='DM Sans', color='#94a3b8', size=12),
    xaxis=dict(gridcolor='#1e293b', linecolor='#334155', zerolinecolor='#1e293b'),
    yaxis=dict(gridcolor='#1e293b', linecolor='#334155', zerolinecolor='#1e293b'),
    legend=dict(bgcolor='rgba(15,23,42,0.8)', bordercolor='#334155', borderwidth=1),
)

def pl(**overrides):
    """Safely merge PLOTLY_LAYOUT with per-chart overrides (prevents duplicate-kwarg TypeError)."""
    merged = {**PLOTLY_LAYOUT, **overrides}
    # Default margin if not specified
    merged.setdefault('margin', dict(t=50, b=40, l=10, r=10))
    return merged


def plot_line_trend(comp_acc_df):
    fig = go.Figure()
    line_colors = {'computers': '#14b8a6', 'computers_accessories': '#f59e0b'}
    fill_colors = {'computers': 'rgba(20,184,166,0.06)', 'computers_accessories': 'rgba(245,158,11,0.06)'}
    labels = {'computers': 'Computers', 'computers_accessories': 'Computer Accessories'}

    for col in [c for c in ['computers', 'computers_accessories'] if c in comp_acc_df.columns]:
        fig.add_trace(go.Scatter(
            x=comp_acc_df['sale_month_year'],
            y=comp_acc_df[col],
            mode='lines+markers',
            name=labels.get(col, col),
            line=dict(color=line_colors.get(col, '#818cf8'), width=2.5),
            marker=dict(size=5, color=line_colors.get(col, '#818cf8')),
            fill='tozeroy',
            fillcolor=fill_colors.get(col, 'rgba(129,140,248,0.06)'),
        ))

    fig.update_layout(**pl(
        title=dict(text='Tren Penjualan Bulanan: Computers vs Accessories', font=dict(color='#e2e8f0', size=15)),
        xaxis_title='Bulan',
        yaxis_title='Total Penjualan (BRL)',
        height=400,
        hovermode='x unified',
    ))
    fig.update_xaxes(tickangle=-35, tickfont=dict(size=10))
    return fig


def plot_corr_heatmap(corr_matrix):
    labels = [c.replace('_', ' ').title() for c in corr_matrix.columns]
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=labels,
        y=labels,
        colorscale=[
            [0.0, '#1e3a5f'], [0.3, '#1d4ed8'],
            [0.5, '#475569'], [0.7, '#0d9488'],
            [1.0, '#14b8a6'],
        ],
        zmin=-1, zmax=1,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont=dict(size=10, color='white'),
        hoverongaps=False,
        showscale=True,
        colorbar=dict(
            tickfont=dict(color='#94a3b8'),
            outlinecolor='#334155',
            thickness=14,
        )
    ))
    fig.update_layout(**pl(
        title=dict(text='Heatmap Korelasi Antar Kategori Produk', font=dict(color='#e2e8f0', size=15)),
        height=480,
        xaxis=dict(tickfont=dict(size=10), tickangle=-30, gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(tickfont=dict(size=10), gridcolor='rgba(0,0,0,0)'),
    ))
    return fig


def plot_revenue_bar(rev_series, top_n=10):
    df = rev_series.head(top_n).reset_index()
    df.columns = ['category', 'revenue']
    df['label'] = df['category'].str.replace('_', ' ').str.title()
    df = df.sort_values('revenue')

    palette = px.colors.sequential.Teal
    colors_list = [palette[int(i * (len(palette) - 1) / (len(df) - 1))] for i in range(len(df))]

    fig = go.Figure(go.Bar(
        x=df['revenue'],
        y=df['label'],
        orientation='h',
        marker=dict(color=colors_list, line=dict(width=0)),
        text=[f"R$ {v/1e6:.2f}M" for v in df['revenue']],
        textposition='outside',
        textfont=dict(color='#94a3b8', size=10),
    ))
    fig.update_layout(**pl(
        title=dict(text=f'Top {top_n} Kategori Produk · Revenue 2017–2018', font=dict(color='#e2e8f0', size=15)),
        xaxis_title='Total Revenue (BRL)',
        yaxis_title='',
        height=420,
        xaxis=dict(gridcolor='#1e293b', tickformat=',.0f'),
    ))
    return fig


def plot_sentiment(review_df, top_n=10, best=True):
    df = review_df.dropna(subset=['review_score', 'product_category_name_english'])
    df = df.sort_values('review_score', ascending=not best).head(top_n).copy()
    df['label'] = df['product_category_name_english'].str.replace('_', ' ').str.title()
    df = df.sort_values('review_score', ascending=best)

    color = '#14b8a6' if best else '#f87171'
    colorscale = 'Teal' if best else 'Reds'

    fig = go.Figure(go.Bar(
        x=df['review_score'],
        y=df['label'],
        orientation='h',
        marker=dict(
            color=df['review_score'],
            colorscale=colorscale,
            cmin=1, cmax=5,
            line=dict(width=0),
        ),
        text=[f"{v:.2f} ★" for v in df['review_score']],
        textposition='outside',
        textfont=dict(color='#94a3b8', size=10),
    ))
    label = 'Terbaik 🏆' if best else 'Terburuk ⚠️'
    fig.update_layout(**pl(
        title=dict(text=f'Top {top_n} Sentimen {label} · Avg Review Score', font=dict(color='#e2e8f0', size=15)),
        xaxis=dict(range=[0, 5.5], tickfont=dict(size=10), gridcolor='#1e293b'),
        yaxis_title='',
        height=400,
    ))
    return fig


def plot_monthly_overview(monthly_df):
    total_monthly = monthly_df.sum(axis=1).reset_index()
    total_monthly.columns = ['month', 'revenue']
    total_monthly['month_str'] = total_monthly['month'].astype(str)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=total_monthly['month_str'],
        y=total_monthly['revenue'],
        mode='lines',
        fill='tozeroy',
        fillcolor='rgba(13,148,136,0.12)',
        line=dict(color='#0d9488', width=2.5),
        name='Total Revenue',
    ))
    fig.update_layout(**pl(
        title=dict(text='Total Revenue Bulanan (Seluruh Kategori)', font=dict(color='#e2e8f0', size=15)),
        xaxis_title='Bulan', yaxis_title='Revenue (BRL)',
        height=300,
        hovermode='x unified',
    ))
    fig.update_xaxes(tickangle=-35, tickfont=dict(size=9))
    return fig


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 20px;'>
        <div style='font-size:1.4rem; font-weight:700; color:#14b8a6; letter-spacing:-0.02em;'>🛒 E-Commerce</div>
        <div style='font-size:0.75rem; color:#475569; margin-top:2px;'>Analytics Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.7rem; color:#475569; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;'>Navigasi</div>", unsafe_allow_html=True)
    
    page = st.radio(
        "",
        ["🏠  Overview", "📈  Tren Penjualan", "🔗  Korelasi Kategori",
         "💰  Revenue 2017–2018", "⭐  Sentimen Pelanggan"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#1e293b; margin: 20px 0;'>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.7rem; color:#475569; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:10px;'>Unggah Dataset</div>", unsafe_allow_html=True)

    use_sample = st.toggle("Gunakan Data Sampel", value=True, help="Aktifkan untuk menggunakan data sintetis. Nonaktifkan untuk mengunggah dataset asli.")

    uploaded = {}
    real_data = None

    if not use_sample:
        required_files = [
            'orders_dataset.csv', 'order_items_dataset.csv',
            'products_dataset.csv', 'order_reviews_dataset.csv',
            'product_category_name_translation.csv',
        ]
        st.markdown(f"<div style='font-size:0.78rem; color:#94a3b8; margin-bottom:8px;'>Upload {len(required_files)} file CSV dari dataset Olist:</div>", unsafe_allow_html=True)
        
        for fname in required_files:
            f = st.file_uploader(fname, type='csv', key=fname, label_visibility="collapsed")
            if f:
                uploaded[fname] = f

        if len(uploaded) == len(required_files):
            real_data, err = load_real_data(uploaded)
            if err:
                st.error(f"Error: {err}")
                real_data = None
            else:
                st.success("✅ Dataset berhasil dimuat!")
        elif uploaded:
            st.warning(f"Upload {len(required_files) - len(uploaded)} file lagi")

    st.markdown("<hr style='border-color:#1e293b; margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.75rem; color:#475569; line-height:1.7;'>
        <div style='color:#94a3b8; font-weight:600; margin-bottom:6px;'>Proyek</div>
        E-Commerce Public Dataset Analysis
        <div style='margin-top:10px; color:#94a3b8; font-weight:600;'>Author</div>
        Revolusi Al-Ghifari
        <div style='color:#475569; font-size:0.7rem;'>revo.bili0912@gmail.com</div>
        <div style='margin-top:10px; color:#475569; font-size:0.7rem;'>ID Dicoding: evolusi</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
if real_data:
    data = real_data
    data_source = "Dataset Asli (Olist)"
else:
    data = generate_sample_data()
    data_source = "Data Sampel (Demo)"

monthly_df = data['monthly_df']
corr_matrix = data['corr_matrix']
rev_2017_2018 = data['rev_2017_2018']
comp_acc = data['comp_acc']
review_df = data['review_df']


# ─────────────────────────────────────────────
#  HEADER (always shown)
# ─────────────────────────────────────────────
col_title, col_badge = st.columns([4, 1])
with col_title:
    st.markdown(f"""
    <div class='page-title'>E-Commerce Analytics</div>
    <div class='page-subtitle'>Brazilian E-Commerce Public Dataset · Proyek Analisis Data</div>
    """, unsafe_allow_html=True)
with col_badge:
    st.markdown(f"""
    <div style='text-align:right; padding-top:12px;'>
        <span class='data-badge'>{'🟢' if real_data else '🔵'} {data_source}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border-color:#1e293b; margin: 16px 0 24px;'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  KPI CARDS
# ─────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

total_rev = data['total_revenue']
total_orders = data['total_orders']
n_cats = data['n_categories']
top_cat = rev_2017_2018.index[0].replace('_', ' ').title() if len(rev_2017_2018) > 0 else "—"

with k1:
    st.markdown(f"""
    <div class='kpi-card teal'>
        <div class='kpi-value'>R$ {total_rev/1e6:.1f}M</div>
        <div class='kpi-label'>Total Revenue</div>
        <div class='kpi-delta'>↑ Semua periode</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class='kpi-card blue'>
        <div class='kpi-value'>{total_orders:,}</div>
        <div class='kpi-label'>Total Pesanan</div>
        <div class='kpi-delta'>↑ Sepanjang dataset</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class='kpi-card violet'>
        <div class='kpi-value'>{n_cats}</div>
        <div class='kpi-label'>Kategori Produk</div>
        <div class='kpi-delta'>Aktif dalam dataset</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class='kpi-card amber'>
        <div class='kpi-value' style='font-size:1.2rem;'>{top_cat[:18]}</div>
        <div class='kpi-label'>Top Revenue Category</div>
        <div class='kpi-delta'>↑ 2017–2018</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGE CONTENT
# ─────────────────────────────────────────────

# ── OVERVIEW ──────────────────────────────────
if "Overview" in page:
    st.markdown("""
    <div class='section-header'>
        <div class='section-number'>📊</div>
        <div>
            <div class='section-title'>Ringkasan & Pertanyaan Bisnis</div>
            <div class='section-subtitle'>Gambaran umum proyek analisis data e-commerce</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.plotly_chart(plot_monthly_overview(monthly_df), use_container_width=True, config={'displayModeBar': False})

    st.markdown("""
    <div class='insight-box'>
        📌 Dashboard ini menjawab <strong>4 pertanyaan bisnis utama</strong> dari dataset e-commerce publik (Olist Brazil):<br><br>
        <strong>1. Tren Penjualan</strong> — Apakah penjualan komputer dan aksesoris komputer bergerak secara linear?<br>
        <strong>2. Korelasi Kategori</strong> — Bagaimana preferensi pelanggan berdasarkan korelasi antar kategori produk?<br>
        <strong>3. Revenue 2017–2018</strong> — Kategori produk apa yang menghasilkan pendapatan terbesar?<br>
        <strong>4. Sentimen Pelanggan</strong> — Kategori mana yang paling disukai dan paling tidak disukai pelanggan?
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    
    # Quick stats grid
    st.markdown("<div style='font-size:0.85rem; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:12px;'>Quick Insights</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        top5_rev = rev_2017_2018.head(5)
        df_top5 = pd.DataFrame({'Kategori': [c.replace('_', ' ').title() for c in top5_rev.index], 'Revenue': top5_rev.values})
        fig_mini = px.bar(df_top5, x='Revenue', y='Kategori', orientation='h',
                          color_discrete_sequence=['#0d9488'], title='Top 5 Revenue 2017–2018')
        fig_mini.update_layout(**pl(height=260, margin=dict(t=40, b=20, l=5, r=5)))
        fig_mini.update_xaxes(tickformat=',.0f')
        st.plotly_chart(fig_mini, use_container_width=True, config={'displayModeBar': False})

    with c2:
        top5_sent = review_df.dropna().sort_values('review_score', ascending=False).head(5)
        top5_sent['label'] = top5_sent['product_category_name_english'].str.replace('_', ' ').str.title()
        fig_sent = px.bar(top5_sent, x='review_score', y='label', orientation='h',
                          color_discrete_sequence=['#818cf8'], title='Top 5 Rating Pelanggan')
        fig_sent.update_layout(**pl(height=260, margin=dict(t=40, b=20, l=5, r=5)))
        fig_sent.update_xaxes(range=[0, 5.5])
        st.plotly_chart(fig_sent, use_container_width=True, config={'displayModeBar': False})


# ── TREN PENJUALAN ────────────────────────────
elif "Tren" in page:
    st.markdown("""
    <div class='section-header'>
        <div class='section-number'>1</div>
        <div>
            <div class='section-title'>Tren Penjualan Bulanan</div>
            <div class='section-subtitle'>Apakah penjualan komputer dan aksesoris komputer bergerak secara linear?</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.plotly_chart(plot_line_trend(comp_acc), use_container_width=True, config={'displayModeBar': False})

    st.markdown("""
    <div class='insight-box'>
        🔍 <strong>Insight:</strong> Penjualan produk kategori <strong>computers</strong> dan <strong>computers_accessories</strong>
        <strong>tidak sepenuhnya linear</strong>. Aksesoris komputer jauh lebih fluktuatif dibanding komputer itu sendiri.
        Terdapat lonjakan signifikan pada pertengahan 2017 (Juli–Oktober), kemungkinan dipicu oleh kampanye promosi
        atau musim belanja. Kategori <em>computers</em> cenderung lebih stabil dengan pertumbuhan moderat.
    </div>""", unsafe_allow_html=True)

    with st.expander("📋 Lihat Data Tabel"):
        st.dataframe(comp_acc.set_index('sale_month_year').style.format("{:,.0f}"), use_container_width=True)


# ── KORELASI KATEGORI ─────────────────────────
elif "Korelasi" in page:
    st.markdown("""
    <div class='section-header'>
        <div class='section-number'>2</div>
        <div>
            <div class='section-title'>Korelasi Antar Kategori Produk</div>
            <div class='section-subtitle'>Bagaimana preferensi pelanggan berdasarkan pola korelasi penjualan?</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.plotly_chart(plot_corr_heatmap(corr_matrix), use_container_width=True, config={'displayModeBar': False})

    st.markdown("""
    <div class='insight-box'>
        🔍 <strong>Insight:</strong> Heatmap menunjukkan korelasi penjualan antar kategori produk pilihan.
        Pasangan kategori dengan korelasi <strong>> 0.93</strong> mengindikasikan bahwa pelanggan yang membeli
        dari satu kategori sangat mungkin juga membeli dari kategori pasangannya — pola ideal untuk strategi
        <em>bundle product</em> dan <em>cross-selling</em>. Warna <strong>teal</strong> menunjukkan korelasi positif kuat.
    </div>""", unsafe_allow_html=True)

    # Highly correlated pairs table
    st.markdown("<div style='margin-top:20px; font-size:0.85rem; color:#64748b; font-weight:600;'>Pasangan Kategori Berkorelasi Tinggi (> 0.75)</div>", unsafe_allow_html=True)

    pairs = []
    cm = corr_matrix
    for i in range(len(cm.columns)):
        for j in range(i + 1, len(cm.columns)):
            val = cm.iloc[i, j]
            if val > 0.75:
                pairs.append({
                    'Kategori 1': cm.columns[i].replace('_', ' ').title(),
                    'Kategori 2': cm.columns[j].replace('_', ' ').title(),
                    'Korelasi': round(val, 4),
                })
    if pairs:
        df_pairs = pd.DataFrame(pairs).sort_values('Korelasi', ascending=False)
        st.dataframe(df_pairs, use_container_width=True, hide_index=True)
    else:
        st.info("Tidak ada pasangan dengan korelasi > 0.75 pada dataset ini.")


# ── REVENUE 2017–2018 ─────────────────────────
elif "Revenue" in page:
    st.markdown("""
    <div class='section-header'>
        <div class='section-number'>3</div>
        <div>
            <div class='section-title'>Revenue Terbesar 2017–2018</div>
            <div class='section-subtitle'>Kategori produk apa yang menghasilkan pendapatan terbesar?</div>
        </div>
    </div>""", unsafe_allow_html=True)

    top_n = st.slider("Tampilkan Top N Kategori", min_value=5, max_value=20, value=10, step=1)
    st.plotly_chart(plot_revenue_bar(rev_2017_2018, top_n=top_n), use_container_width=True, config={'displayModeBar': False})

    top_cat_name = rev_2017_2018.index[0].replace('_', ' ').title()
    top_cat_rev = rev_2017_2018.iloc[0]
    pct = top_cat_rev / rev_2017_2018.sum() * 100

    st.markdown(f"""
    <div class='insight-box'>
        🔍 <strong>Insight:</strong> Kategori <strong>{top_cat_name}</strong> mendominasi dengan revenue tertinggi
        (R$ {top_cat_rev/1e6:.2f}M, sekitar {pct:.1f}% dari total top-{top_n}).
        Ini mengindikasikan produk kecantikan & kesehatan adalah segmen terkuat di platform ini.
        Kategori-kategori ini harus menjadi prioritas dalam strategi promosi, manajemen stok, dan pengembangan produk.
    </div>""", unsafe_allow_html=True)

    with st.expander("📋 Lihat Semua Kategori"):
        all_rev = rev_2017_2018.reset_index()
        all_rev.columns = ['Kategori', 'Revenue (BRL)']
        all_rev['Kategori'] = all_rev['Kategori'].str.replace('_', ' ').str.title()
        all_rev['Revenue (BRL)'] = all_rev['Revenue (BRL)'].map('{:,.0f}'.format)
        all_rev['Rank'] = range(1, len(all_rev) + 1)
        st.dataframe(all_rev[['Rank', 'Kategori', 'Revenue (BRL)']], use_container_width=True, hide_index=True)


# ── SENTIMEN PELANGGAN ─────────────────────────
elif "Sentimen" in page:
    st.markdown("""
    <div class='section-header'>
        <div class='section-number'>4</div>
        <div>
            <div class='section-title'>Sentimen Pelanggan</div>
            <div class='section-subtitle'>Kategori dengan rating terbaik dan terburuk dari pelanggan</div>
        </div>
    </div>""", unsafe_allow_html=True)

    tab_best, tab_worst = st.tabs(["🏆 Sentimen Terbaik", "⚠️ Sentimen Terburuk"])

    with tab_best:
        top_n_sent = st.slider("Top N kategori", 5, 15, 10, key='best_n')
        st.plotly_chart(plot_sentiment(review_df, top_n=top_n_sent, best=True), use_container_width=True, config={'displayModeBar': False})
        best_cat = review_df.dropna().sort_values('review_score', ascending=False).iloc[0]
        st.markdown(f"""
        <div class='insight-box'>
            🏆 <strong>{best_cat['product_category_name_english'].replace('_',' ').title()}</strong>
            mendapatkan rating rata-rata tertinggi ({best_cat['review_score']:.2f}/5.00 ★).
            Kategori ini menunjukkan kepuasan pelanggan yang sangat tinggi — kualitas produk, harga,
            dan pengalaman belanja yang luar biasa kemungkinan menjadi faktor utama.
        </div>""", unsafe_allow_html=True)

    with tab_worst:
        top_n_worst = st.slider("Top N kategori", 5, 15, 10, key='worst_n')
        st.plotly_chart(plot_sentiment(review_df, top_n=top_n_worst, best=False), use_container_width=True, config={'displayModeBar': False})
        worst_cat = review_df.dropna().sort_values('review_score', ascending=True).iloc[0]
        st.markdown(f"""
        <div class='insight-box'>
            ⚠️ <strong>{worst_cat['product_category_name_english'].replace('_',' ').title()}</strong>
            mendapatkan rating rata-rata terendah ({worst_cat['review_score']:.2f}/5.00 ★).
            Kategori ini perlu investigasi lebih lanjut — kemungkinan disebabkan oleh
            kualitas produk yang tidak sesuai ekspektasi, masalah pengiriman, atau layanan purna jual yang buruk.
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("<hr style='border-color:#1e293b; margin: 40px 0 20px;'>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#334155; font-size:0.78rem; padding-bottom:20px;'>
    Proyek Analisis Data · Revolusi Al-Ghifari · revo.bili0912@gmail.com · ID Dicoding: evolusi<br>
    <span style='color:#1e3a5f;'>Dataset: Brazilian E-Commerce Public Dataset by Olist</span>
</div>
""", unsafe_allow_html=True)
