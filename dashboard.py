import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_sum_payment_type_df(df):
    sum_payment_type_df = df.groupby("payment_type").size().sort_values(ascending=False).reset_index(name="Jumlah_Payment")
    return sum_payment_type_df

def create_monthly_orders_df(df):
    monthly_orders_df = df.resample(rule='ME', on='shipping_limit_date').agg({
        "order_id": "nunique"
    }).reset_index()
    monthly_orders_df.rename(columns={"order_id": "order_count"}, inplace=True)
    monthly_orders_df["year"] = monthly_orders_df["shipping_limit_date"].dt.year
    monthly_orders_df["month"] = monthly_orders_df["shipping_limit_date"].dt.strftime('%b')
    return monthly_orders_df

def create_sum_year_df(df):
    sum_year_df = df.groupby("year")["order_count"].sum().reset_index()
    return sum_year_df

# Membaca data
all_df = pd.read_csv("all_data.csv")

# Konversi kolom tanggal ke format datetime
all_df["shipping_limit_date"] = pd.to_datetime(all_df["shipping_limit_date"])
all_df = all_df.sort_values(by="shipping_limit_date", ascending=True, ignore_index=True)

# Daftar tahun yang tersedia
available_years = list(range(2016, 2021))

# Sidebar
with st.sidebar:
    start_year = st.selectbox("Pilih Tahun Awal", available_years, index=0)
    filtered_years = [year for year in available_years if year >= start_year]
    end_year = st.selectbox("Pilih Tahun Akhir", filtered_years, index=len(filtered_years) - 1)

# Filter data
main_df = all_df[(all_df["shipping_limit_date"].dt.year >= start_year) & 
                 (all_df["shipping_limit_date"].dt.year <= end_year)]

# DataFrame berdasarkan filter data
sum_payment_type_df = create_sum_payment_type_df(main_df)
monthly_orders_df = create_monthly_orders_df(main_df)
sum_year_df = create_sum_year_df(monthly_orders_df)

# Tampilan Dashboard
st.header('Dashboard E-Commerce Public 🛒')

#Grafik 1
st.subheader('Tipe Payment Terbanyak dan Sedikit')
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#72BCD4"]

fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(x="payment_type", y="Jumlah_Payment", data=sum_payment_type_df, palette=colors, ax=ax1)
ax1.set_title("Penggunaan Tipe Pembayaran", fontsize=14)
ax1.set_xlabel("Tipe Pembayaran", fontsize=12)
ax1.set_ylabel("Jumlah Penggunaan", fontsize=12)

st.pyplot(fig1)

# Grafik 2
st.subheader('Grafik Order yang Didapatkan Setiap Bulan')

filtered_df = monthly_orders_df[(monthly_orders_df["year"] >= start_year) & 
                                (monthly_orders_df["year"] <= end_year)]
pivot_df = filtered_df.pivot(index="month", columns="year", values="order_count")

month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
pivot_df = pivot_df.reindex(month_order)

fig2, ax2 = plt.subplots(figsize=(12, 6))
pivot_df.plot(kind="bar", ax=ax2)

ax2.set_title(f"Jumlah Order Per Bulan ({start_year}-{end_year})", fontsize=16)
ax2.set_xlabel("Bulan", fontsize=12)
ax2.set_ylabel("Jumlah Order", fontsize=12)
ax2.set_xticklabels(month_order, rotation=0, fontsize=12)
ax2.legend(title="Tahun")
ax2.grid(axis="y", linestyle="--", alpha=0.7)

st.pyplot(fig2)

# Grafik 3
st.subheader(f"Total Orders per Tahun")

filtered_sum_year_df = sum_year_df[(sum_year_df["year"] >= start_year) & 
                                   (sum_year_df["year"] <= end_year)]

fig3, ax3 = plt.subplots(figsize=(8, 5))
ax3.bar(filtered_sum_year_df["year"].astype(str), filtered_sum_year_df["order_count"], color="#72BCD4")

ax3.set_title("Total Orders per Tahun", fontsize=14)
ax3.set_xlabel("Tahun", fontsize=12)
ax3.set_ylabel("Total Order", fontsize=12)
ax3.grid(axis="y", linestyle="--", alpha=0.7)

st.pyplot(fig3)

st.caption('Copyright (c) Ichwan 2025')