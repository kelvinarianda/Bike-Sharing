import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# =====================
# LOAD DATA
# =====================
df = pd.read_csv("main_data.csv")
df["dteday"] = pd.to_datetime(df["dteday"])

# =====================
# TITLE
# =====================
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis penyewaan sepeda berdasarkan **cuaca dan waktu**")

# =====================
# SIDEBAR FILTER
# =====================
st.sidebar.header("🔎 Filter Data")

season = st.sidebar.selectbox(
    "Pilih Musim",
    sorted(df["season"].unique())
)

workingday = st.sidebar.selectbox(
    "Hari Kerja",
    ["Semua", "Ya", "Tidak"]
)

filtered_df = df[df["season"] == season]

if workingday == "Ya":
    filtered_df = filtered_df[filtered_df["workingday"] == 1]
elif workingday == "Tidak":
    filtered_df = filtered_df[filtered_df["workingday"] == 0]

# =====================
# METRICS
# =====================
col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", int(filtered_df["cnt"].sum()))
col2.metric("Rata-rata Harian", int(filtered_df["cnt"].mean()))
col3.metric("Data Tersedia", len(filtered_df))

st.markdown("---")

# =====================
# LAYOUT 2 KOLOM
# =====================
col_left, col_right = st.columns(2)

# =====================
# GRAFIK 1: CUACA
# =====================
with col_left:
    st.subheader("🌤️ Pengaruh Cuaca")

    fig1, ax1 = plt.subplots()
    sns.barplot(x="weathersit", y="cnt", data=filtered_df, ax=ax1)
    ax1.set_title("Cuaca vs Penyewaan")
    ax1.set_xlabel("Cuaca")
    ax1.set_ylabel("Jumlah")

    st.pyplot(fig1)

# =====================
# GRAFIK 2: TREND WAKTU
# =====================
with col_right:
    st.subheader("📈 Tren Penyewaan")

    fig2, ax2 = plt.subplots()
    sns.lineplot(x="dteday", y="cnt", data=filtered_df, ax=ax2)
    ax2.set_title("Tren Waktu")
    plt.xticks(rotation=45)

    st.pyplot(fig2)

# =====================
# INSIGHT
# =====================
st.markdown("---")
st.subheader("💡 Insight")

st.info("""
- Penyewaan sepeda tertinggi terjadi saat kondisi cuaca cerah.
- Jumlah penyewaan menurun saat cuaca buruk.
- Terdapat pola penggunaan yang stabil dengan peningkatan pada hari kerja.
- Data menunjukkan perilaku pengguna dipengaruhi oleh faktor lingkungan dan aktivitas harian.
""")

# =====================
# DATA TABLE
# =====================
st.markdown("---")
st.subheader("📊 Data Preview")

st.dataframe(filtered_df.head(20))