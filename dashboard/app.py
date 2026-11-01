from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Bike Rental Analysis Dashboard", layout="wide")

# ---------------------------------------------------------------------------
# 1. LOAD DATA
# Path dibuat absolut berdasarkan lokasi file app.py, jadi tetap jalan
# walaupun Streamlit dijalankan dari folder root repo (seperti di Streamlit Cloud).
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
CANDIDATES = [
    BASE_DIR / "main_data.csv",
    BASE_DIR.parent / "dashboard" / "main_data.csv",
    BASE_DIR.parent / "data" / "day.csv",
]

SEASON_LABELS = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
WEATHER_LABELS = {
    1: "Clear",
    2: "Mist",
    3: "Light Snow/Rain",
    4: "Heavy Rain/Snow",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    csv_path = next((p for p in CANDIDATES if p.exists()), None)
    if csv_path is None:
        raise FileNotFoundError(
            "File data tidak ditemukan. Sudah dicari di: "
            + ", ".join(str(p) for p in CANDIDATES)
        )

    df = pd.read_csv(csv_path)
    df["dteday"] = pd.to_datetime(df["dteday"])

    # main_data.csv adalah hasil merge day.csv + hour.csv (kolom berakhiran _x = data harian,
    # _y = data per jam). Kita pakai data harian saja.
    rename_map = {
        "season_x": "season", "yr_x": "yr", "mnth_x": "mnth",
        "holiday_x": "holiday", "weekday_x": "weekday",
        "workingday_x": "workingday", "weathersit_x": "weathersit",
        "temp_x": "temp", "atemp_x": "atemp", "hum_x": "hum",
        "windspeed_x": "windspeed", "casual_x": "casual",
        "registered_x": "registered", "cnt_x": "cnt",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    daily_cols = [
        "dteday", "season", "yr", "mnth", "holiday", "weekday", "workingday",
        "weathersit", "temp", "atemp", "hum", "windspeed", "casual",
        "registered", "cnt",
    ]
    df = df[[c for c in daily_cols if c in df.columns]]

    # Baris harian terduplikasi 24x akibat merge dengan data per jam -> hapus
    df = df.drop_duplicates(subset="dteday").reset_index(drop=True)
    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

# ---------------------------------------------------------------------------
# 2. JUDUL
# ---------------------------------------------------------------------------
st.title("Bike Rental Analysis Dashboard")
st.caption(f"Data harian: {len(df)} hari ({df['dteday'].min().date()} s/d {df['dteday'].max().date()})")

# ---------------------------------------------------------------------------
# 3. CORRELATION MATRIX
# ---------------------------------------------------------------------------
st.subheader("Correlation Matrix")
corr_cols = [c for c in ["temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"] if c in df.columns]
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df[corr_cols].corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
ax.set_title("Correlation Matrix Main Data")
st.pyplot(fig)
plt.close(fig)

# ---------------------------------------------------------------------------
# 4. HISTOGRAM
# ---------------------------------------------------------------------------
st.subheader("Histogram of Bike Rentals per Day")
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df["cnt"], bins=20, color="skyblue", edgecolor="black")
ax.set_xlabel("Total Bike Rentals")
ax.set_ylabel("Frequency")
ax.set_title("Histogram of Bike Rentals per Day")
st.pyplot(fig)
plt.close(fig)

# ---------------------------------------------------------------------------
# 5. BOXPLOT PER MUSIM
# ---------------------------------------------------------------------------
st.subheader("Box Plot of Bike Rentals by Season")
df["season_label"] = df["season"].map(SEASON_LABELS)
season_order = [SEASON_LABELS[k] for k in sorted(SEASON_LABELS) if SEASON_LABELS[k] in set(df["season_label"])]
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x="season_label", y="cnt", hue="season_label", data=df,
            order=season_order, palette="Set3", legend=False, ax=ax)
ax.set_xlabel("Season")
ax.set_ylabel("Total Bike Rentals")
ax.set_title("Box Plot of Bike Rentals by Season")
st.pyplot(fig)
plt.close(fig)

# ---------------------------------------------------------------------------
# 6. DAMPAK LIBURAN
# ---------------------------------------------------------------------------
st.subheader("Impact of Holiday on Bike Rentals")
holiday_rental = df.groupby("holiday")["cnt"].mean()
holiday_names = ["No" if i == 0 else "Yes" for i in holiday_rental.index]
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(holiday_names, holiday_rental.values, color="lightblue")
ax.set_xlabel("Holiday")
ax.set_ylabel("Average Bike Rentals")
ax.set_title("Impact of Holiday on Bike Rentals")
st.pyplot(fig)
plt.close(fig)

# ---------------------------------------------------------------------------
# 7. DAMPAK CUACA
# ---------------------------------------------------------------------------
st.subheader("Impact of Weather Situation on Bike Rentals")
df["weather_label"] = df["weathersit"].map(WEATHER_LABELS)
weather_rental = df.groupby("weather_label")["cnt"].mean()
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(weather_rental.index, weather_rental.values, color="lightblue")
ax.set_xlabel("Weather Situation")
ax.set_ylabel("Average Bike Rentals")
ax.set_title("Impact of Weather on Bike Rentals")
plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
st.pyplot(fig)
plt.close(fig)

# ---------------------------------------------------------------------------
# 8. DISTRIBUSI PER CUACA
# ---------------------------------------------------------------------------
st.subheader("Distribution of Bike Rentals by Weather Situation")
weather_order = [v for v in WEATHER_LABELS.values() if v in set(df["weather_label"])]
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(x="weather_label", y="cnt", hue="weather_label", data=df,
            order=weather_order, palette="Set2", legend=False, ax=ax)
ax.set_xlabel("Weather Situation")
ax.set_ylabel("Total Bike Rentals")
ax.set_title("Distribution of Bike Rentals by Weather Situation")
st.pyplot(fig)
plt.close(fig)

# ---------------------------------------------------------------------------
# 9. RATA-RATA MUSIM x CUACA
# ---------------------------------------------------------------------------
st.subheader("Average Bike Rentals by Season and Weather")
df["season_weather"] = df["season_label"].astype(str) + " - " + df["weather_label"].astype(str)
season_weather_rental = df.groupby("season_weather")["cnt"].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(12, 6))
season_weather_rental.plot(kind="bar", color="steelblue", ax=ax)
ax.set_xlabel("Season and Weather")
ax.set_ylabel("Average Bike Rentals")
ax.set_title("Average Bike Rentals by Season and Weather")
plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ---------------------------------------------------------------------------
# 10. KELOMPOK PENYEWAAN (BINNING)
# ---------------------------------------------------------------------------
st.subheader("Rental Groups (Season - Weather)")
high_rental = season_weather_rental[season_weather_rental > 5000].index.tolist()
medium_rental = season_weather_rental[(season_weather_rental >= 2000) & (season_weather_rental <= 5000)].index.tolist()
low_rental = season_weather_rental[season_weather_rental < 2000].index.tolist()

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**High (> 5000)**")
    st.write(high_rental or "-")
with col2:
    st.markdown("**Medium (2000 - 5000)**")
    st.write(medium_rental or "-")
with col3:
    st.markdown("**Low (< 2000)**")
    st.write(low_rental or "-")
