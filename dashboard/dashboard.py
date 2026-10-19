import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set page configuration
st.set_page_config(
    page_title="Brazilian E-Commerce Analytics Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling for polished UI
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-left: 5px solid #1f77b4;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading for optimal performance
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "main_data.csv")
    if not os.path.exists(data_path):
        data_path = os.path.join("dashboard", "main_data.csv")
    
    df = pd.read_csv(data_path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"])
    return df

df_raw = load_data()

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=75)
    st.title("E-Commerce Dashboard")
    st.caption("Dicoding Final Project: Belajar Fundamental Analisis Data")
    
    st.markdown("---")
    st.subheader("Filter Data")
    
    # Date Range Picker
    min_date = df_raw["order_purchase_timestamp"].min().date()
    max_date = df_raw["order_purchase_timestamp"].max().date()
    
    date_range = st.date_input(
        label="Rentang Tanggal Pesanan",
        min_value=min_date,
        max_value=max_date,
        value=[pd.to_datetime("2017-01-01").date(), pd.to_datetime("2018-08-31").date()]
    )
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
        start_date = end_date = date_range[0]
    else:
        start_date, end_date = min_date, max_date
    
    # State Filter
    all_states = sorted(df_raw["customer_state"].dropna().unique().tolist())
    state_options = ["Semua State"] + all_states
    selected_state_option = st.multiselect(
        label="Pilih Wilayah (State)",
        options=state_options,
        default=["Semua State"]
    )
    # Jika memilih "Semua State" atau tidak ada pilihan → tampilkan semua
    if not selected_state_option or "Semua State" in selected_state_option:
        selected_states = all_states
    else:
        selected_states = selected_state_option
        
    st.markdown("---")
    st.markdown("**Profil Analis:**")
    st.markdown("- **Nama:** Gilbert Finsen Zakaria Lian")
    st.markdown("- **ID Dicoding:** gilbert_lian")
    st.markdown("- **Dataset:** Brazilian E-Commerce (Olist)")

# Apply filters
filtered_df = df_raw[
    (df_raw["order_purchase_timestamp"].dt.date >= start_date) &
    (df_raw["order_purchase_timestamp"].dt.date <= end_date) &
    (df_raw["customer_state"].isin(selected_states))
]

# ----------------- HEADER & KPIS -----------------
st.markdown('<div class="main-header">🛍️ Brazilian E-Commerce Performance Dashboard</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Menganalisis Tren Penjualan, Efisiensi Pengiriman, Skor Kepuasan Pelanggan, dan Segmentasi Pelanggan (Data: {start_date} s/d {end_date})</div>', unsafe_allow_html=True)

# KPI Metrics
total_orders = filtered_df["order_id"].nunique()
total_revenue = filtered_df["price"].sum()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
avg_review = filtered_df["review_score"].dropna().mean()
on_time_count = (filtered_df["delivery_status"] == "On-Time / Early").sum()
total_delivered = filtered_df["delivery_status"].dropna().count()
on_time_pct = (on_time_count / total_delivered * 100) if total_delivered > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(label="Total Pesanan", value=f"{total_orders:,}")
with col2:
    st.metric(label="Total Revenue (BRL)", value=f"R$ {total_revenue:,.2f}")
with col3:
    st.metric(label="Rata-rata Order Value", value=f"R$ {avg_order_value:,.2f}")
with col4:
    st.metric(label="Rata-rata Kepuasan ⭐", value=f"{avg_review:.2f} / 5.0" if not np.isnan(avg_review) else "N/A")
with col5:
    st.metric(label="Tingkat On-Time Delivery", value=f"{on_time_pct:.1f}%")

st.markdown("---")

# ----------------- TABS -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Tren Penjualan", 
    "🏆 Kategori Produk (Pertanyaan 1)", 
    "🚚 Logistik & Kepuasan (Pertanyaan 2)", 
    "👥 RFM Analysis", 
    "🗺️ Analisis Geografis"
])

# ----- TAB 1: Tren Penjualan Bulanan -----
with tab1:
    st.subheader("Tren Penjualan Bulanan & Volume Pesanan")
    df_trend = filtered_df.copy()
    df_trend["year_month"] = df_trend["order_purchase_timestamp"].dt.to_period("M").astype(str)
    
    monthly_summary = df_trend.groupby("year_month").agg(
        revenue=("price", "sum"),
        orders=("order_id", "nunique")
    ).reset_index()
    
    fig, ax1 = plt.subplots(figsize=(12, 5))
    color = '#1f77b4'
    ax1.set_xlabel('Bulan Pemesanan', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Total Revenue (BRL)', color=color, fontsize=11, fontweight='bold')
    line1 = ax1.plot(monthly_summary['year_month'], monthly_summary['revenue'], color=color, marker='o', linewidth=2.5, label='Revenue (BRL)')
    ax1.tick_params(axis='y', labelcolor=color)
    plt.xticks(rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    ax2 = ax1.twinx()
    color = '#ff7f0e'
    ax2.set_ylabel('Total Pesanan', color=color, fontsize=11, fontweight='bold')
    line2 = ax2.plot(monthly_summary['year_month'], monthly_summary['orders'], color=color, marker='s', linestyle='--', linewidth=2, label='Orders')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Dinamika Pertumbuhan Revenue dan Volume Pesanan Bulanan', fontsize=14, fontweight='bold', pad=15)
    fig.tight_layout()
    st.pyplot(fig)
    
    st.info("💡 **Insight:** Penjualan platform mengalami pertumbuhan eksponensial sepanjang 2017 hingga pertengahan 2018. Puncak tertinggi tercatat pada November 2017 (momentum Black Friday) dengan lonjakan volume transaksi lebih dari 200%.")

# ----- TAB 2: Kategori Produk (Pertanyaan 1) -----
with tab2:
    st.subheader("Pertanyaan Bisnis 1: Kategori Produk dengan Revenue Tertinggi & Terendah")
    
    cat_summary = filtered_df.groupby("product_category_name_english").agg(
        total_revenue=("price", "sum"),
        total_orders=("order_id", "count")
    ).reset_index()
    
    top_5_cats = cat_summary.sort_values("total_revenue", ascending=False).head(5)
    bottom_5_cats = cat_summary.sort_values("total_revenue", ascending=True).head(5)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("#### 🥇 Top 5 Kategori Teratas (Revenue)")
        fig, ax = plt.subplots(figsize=(8, 5))
        # Warna seragam biru, highlight hijau hanya pada nilai tertinggi (index 0)
        base_color_top = '#93C5FD'
        highlight_color_top = '#10B981'
        colors = [highlight_color_top if i == 0 else base_color_top for i in range(len(top_5_cats))]
        bars = ax.barh(top_5_cats['product_category_name_english'], top_5_cats['total_revenue'], color=colors)
        ax.invert_yaxis()
        ax.set_xlabel('Total Revenue (BRL)', fontsize=10, fontweight='bold')
        ax.set_title('Top 5 Kategori Produk Berdasarkan Revenue', fontsize=12, fontweight='bold')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        for bar in bars:
            width = bar.get_width()
            ax.text(width * 1.01, bar.get_y() + bar.get_height()/2, f"R$ {width:,.0f}", ha='left', va='center', fontsize=9, fontweight='bold')
        fig.tight_layout()
        st.pyplot(fig)
        
    with col_right:
        st.markdown("#### 🔻 Bottom 5 Kategori Terendah (Revenue)")
        fig, ax = plt.subplots(figsize=(8, 5))
        # Warna seragam merah muda, highlight merah tua hanya pada nilai terendah (index 0)
        base_color_bot = '#FCA5A5'
        highlight_color_bot = '#EF4444'
        colors = [highlight_color_bot if i == 0 else base_color_bot for i in range(len(bottom_5_cats))]
        bars = ax.barh(bottom_5_cats['product_category_name_english'], bottom_5_cats['total_revenue'], color=colors)
        ax.invert_yaxis()
        ax.set_xlabel('Total Revenue (BRL)', fontsize=10, fontweight='bold')
        ax.set_title('Bottom 5 Kategori Produk Berdasarkan Revenue', fontsize=12, fontweight='bold')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        for bar in bars:
            width = bar.get_width()
            ax.text(width * 1.05, bar.get_y() + bar.get_height()/2, f"R$ {width:,.0f}", ha='left', va='center', fontsize=9, fontweight='bold')
        fig.tight_layout()
        st.pyplot(fig)

    st.success("""
    📌 **Temuan Kunci Pertanyaan 1:**
    - Kategori **health_beauty**, **watches_gifts**, dan **bed_bath_table** adalah tiga pilar kontributor pendapatan utama dengan revenue masing-masing melebihi R$ 1.000.000.
    - Sebaliknya, kategori **security_and_services**, **fashion_childrens_clothes**, dan **cds_dvds_musicals** mencatat pendapatan paling minim (< R$ 1.000) dan volume pesanan yang sangat sedikit.
    """)

# ----- TAB 3: Logistik & Kepuasan (Pertanyaan 2) -----
with tab3:
    st.subheader("Pertanyaan Bisnis 2: Pengaruh Keterlambatan Pengiriman terhadap Kepuasan Pelanggan")
    
    deliv_df = filtered_df.dropna(subset=["delivery_status", "review_score"]).copy()
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        avg_score_ontime = deliv_df[deliv_df["delivery_status"] == "On-Time / Early"]["review_score"].mean()
        st.metric(
            label="⭐ Rata-rata Skor: Tepat Waktu / Lebih Cepat",
            value=f"{avg_score_ontime:.2f} / 5.0",
            delta="Puas (+1.73 poin)",
            delta_color="normal"
        )
    with col_m2:
        avg_score_late = deliv_df[deliv_df["delivery_status"] == "Late"]["review_score"].mean()
        st.metric(
            label="⚠️ Rata-rata Skor: Terlambat (Late)",
            value=f"{avg_score_late:.2f} / 5.0",
            delta="-1.73 penurunan drastis",
            delta_color="inverse"
        )
        
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("#### Proporsi Rating (1 s/d 5) Berdasarkan Status Pengiriman")
        crosstab_pct = pd.crosstab(deliv_df["delivery_status"], deliv_df["review_score"], normalize="index") * 100
        
        fig, ax = plt.subplots(figsize=(8, 5))
        crosstab_pct.plot(kind="bar", stacked=True, colormap="RdYlGn", ax=ax, edgecolor="black", alpha=0.85)
        ax.set_title("Distribusi Rating Ulasan: On-Time vs Late", fontsize=12, fontweight='bold')
        ax.set_ylabel("Persentase (%)", fontsize=10, fontweight='bold')
        ax.set_xlabel("Status Pengiriman", fontsize=10, fontweight='bold')
        ax.legend(title="Rating Bintang", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=0)
        fig.tight_layout()
        st.pyplot(fig)
        
    with col_v2:
        st.markdown("#### Hubungan Jumlah Hari Keterlambatan vs Skor Review")
        late_sample = deliv_df[deliv_df["delay_days"] > 0].copy()
        late_sample["delay_bracket"] = pd.cut(
            late_sample["delay_days"], 
            bins=[0, 3, 7, 14, 30, np.inf], 
            labels=["1-3 Hari", "4-7 Hari", "8-14 Hari", "15-30 Hari", "> 30 Hari"]
        )
        bracket_scores = late_sample.groupby("delay_bracket", observed=False)["review_score"].mean().reset_index()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(bracket_scores["delay_bracket"].astype(str), bracket_scores["review_score"], color="#F97316")
        ax.set_ylim(1, 5)
        ax.set_ylabel("Rata-rata Skor Review", fontsize=10, fontweight='bold')
        ax.set_xlabel("Rentang Hari Keterlambatan", fontsize=10, fontweight='bold')
        ax.set_title("Penurunan Skor Review Seiring Makin Lamanya Keterlambatan", fontsize=12, fontweight='bold')
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, f"{height:.2f}", ha='center', fontsize=9, fontweight='bold')
        fig.tight_layout()
        st.pyplot(fig)

    st.warning("""
    📌 **Temuan Kunci Pertanyaan 2:**
    - Pada pengiriman **On-Time / Early**, **62.5%** pelanggan memberikan rating sempurna (bintang 5) dan skor rata-rata mencapai **4.29**.
    - Ketika pengiriman **Terlambat (Late)**, skor rata-rata anjlok menjadi **2.57**, dengan **46.2%** pelanggan langsung melayangkan rating bintang 1.
    - Keterlambatan lebih dari 7 hari menurunkan kepuasan rata-rata ke level kritis di bawah 2.0 bintang.
    """)

# ----- TAB 4: RFM Analysis -----
with tab4:
    st.subheader("Analisis Lanjutan: RFM Analysis (Recency, Frequency, Monetary)")
    st.caption("Segmentasi perilaku transaksi pelanggan tanpa algoritma machine learning sesuai kriteria bintang 5 Dicoding.")
    
    # Calculate RFM based on current filtered slice
    ref_date = filtered_df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    rfm_df = filtered_df.groupby("customer_unique_id").agg(
        recency=("order_purchase_timestamp", lambda d: (ref_date - d.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("price", "sum")
    ).reset_index()
    
    col_rfm1, col_rfm2, col_rfm3 = st.columns(3)
    
    with col_rfm1:
        st.markdown("##### ⏱️ Top 5 by Recency (Transaksi Terkini)")
        top_recency = rfm_df.sort_values("recency", ascending=True).head(5)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(top_recency["customer_unique_id"].str[:8] + "...", top_recency["recency"], color="#60A5FA")
        ax.invert_yaxis()
        ax.set_xlabel("Recency (Hari)", fontsize=9, fontweight='bold')
        ax.set_title("Customer Paling Aktif Belanja Terkini", fontsize=10, fontweight='bold')
        fig.tight_layout()
        st.pyplot(fig)
        
    with col_rfm2:
        st.markdown("##### 🔁 Top 5 by Frequency (Frekuensi Terbanyak)")
        top_freq = rfm_df.sort_values("frequency", ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(top_freq["customer_unique_id"].str[:8] + "...", top_freq["frequency"], color="#34D399")
        ax.invert_yaxis()
        ax.set_xlabel("Frekuensi Pesanan", fontsize=9, fontweight='bold')
        ax.set_title("Customer Paling Sering Bertransaksi", fontsize=10, fontweight='bold')
        fig.tight_layout()
        st.pyplot(fig)
        
    with col_rfm3:
        st.markdown("##### 💰 Top 5 by Monetary (Nilai Belanja Tertinggi)")
        top_mon = rfm_df.sort_values("monetary", ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(top_mon["customer_unique_id"].str[:8] + "...", top_mon["monetary"], color="#FBBF24")
        ax.invert_yaxis()
        ax.set_xlabel("Monetary (BRL)", fontsize=9, fontweight='bold')
        ax.set_title("Customer Pengeluaran Tertinggi", fontsize=10, fontweight='bold')
        fig.tight_layout()
        st.pyplot(fig)
        
    st.info("💡 **Insight RFM:** Mayoritas customer e-commerce di platform melakukan pembelian 1 kali (single transaction buyers). Namun segmen pelanggan berulang (repeat buyers) memiliki loyalitas tinggi dengan frekuensi hingga belasan transaksi dan kontribusi pengeluaran hingga ribuan BRL.")

# ----- TAB 5: Geospatial Distribution -----
with tab5:
    st.subheader("Analisis Lanjutan: Sebaran Geografis Pelanggan (Geospatial Analysis)")
    
    state_orders = filtered_df.groupby("customer_state").agg(
        total_orders=("order_id", "nunique"),
        total_revenue=("price", "sum"),
        avg_delivery_time=("delivery_time_days", "mean")
    ).reset_index().sort_values("total_orders", ascending=False)
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("#### 10 Negara Bagian (State) Terbesar Berdasarkan Pesanan")
        fig, ax = plt.subplots(figsize=(8, 5))
        top10_orders = state_orders.head(10)
        # Seragamkan warna: biru dominan, highlight state tertinggi (index 0)
        geo_colors = ['#1D4ED8' if i == 0 else '#93C5FD' for i in range(len(top10_orders))]
        ax.bar(top10_orders["customer_state"], top10_orders["total_orders"], color=geo_colors)
        ax.set_xlabel("Negara Bagian (State)", fontsize=10, fontweight='bold')
        ax.set_ylabel("Jumlah Pesanan Unik", fontsize=10, fontweight='bold')
        ax.set_title("Konsentrasi Pelanggan per Negara Bagian Brazil", fontsize=12, fontweight='bold')
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        fig.tight_layout()
        st.pyplot(fig)
        
    with col_g2:
        st.markdown("#### Rata-rata Durasi Pengiriman (Hari) per State (Top 10)")
        fig, ax = plt.subplots(figsize=(8, 5))
        top10_delivery = state_orders.head(10).sort_values("avg_delivery_time", ascending=False)
        # Seragamkan warna: merah dominan, highlight state terlama (index 0)
        del_colors = ['#B91C1C' if i == 0 else '#FCA5A5' for i in range(len(top10_delivery))]
        ax.bar(top10_delivery["customer_state"], top10_delivery["avg_delivery_time"], color=del_colors)
        ax.set_xlabel("Negara Bagian (State)", fontsize=10, fontweight='bold')
        ax.set_ylabel("Rata-rata Waktu Pengiriman (Hari)", fontsize=10, fontweight='bold')
        ax.set_title("Perbandingan Efisiensi Logistik Antar State", fontsize=12, fontweight='bold')
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        fig.tight_layout()
        st.pyplot(fig)
        
    st.info("💡 **Insight Geografis:** Konsentrasi transaksi sangat terpusat di wilayah tenggara Brazil, khususnya São Paulo (SP), Rio de Janeiro (RJ), dan Minas Gerais (MG). Waktu pengiriman di wilayah SP jauh lebih cepat (~8 hari) dibanding wilayah utara/timur laut seperti BA (~15 hari) akibat kedekatan lokasi hub logistik seller.")

# ----------------- FOOTER -----------------
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8;'>Proyek Akhir Belajar Fundamental Analisis Data | Dicoding Indonesia © 2026</p>", unsafe_allow_html=True)
