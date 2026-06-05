# AI Career Recommendation Dashboard

Dashboard Streamlit profesional untuk eksplorasi dan analisis dataset `New_Career_Recommendation_Cleaned.csv`.

## Fitur

- Layout `wide` dengan desain modern
- Dukungan `light mode` dan `dark mode` otomatis dari Streamlit
- Sidebar navigasi dengan icon
- Modul halaman terpisah menggunakan folder `pages`
- KPI cards, visualisasi Plotly, dan tabel interaktif
- Filter interaktif dan download CSV hasil filter
- Optimasi load dataset dengan `st.cache_data`

## Struktur File

- `streamlit_app.py` - entry point utama
- `utils.py` - helper untuk load dataset dan tema
- `pages/home.py` - halaman HOME
- `pages/data_overview.py` - halaman DATA OVERVIEW
- `pages/eda.py` - halaman EDA
- `pages/career_insights.py` - halaman CAREER INSIGHTS
- `pages/filter_page.py` - halaman FILTER INTERAKTIF
- `requirements.txt` - dependencies

## Cara Jalankan

1. Salin atau letakkan `New_Career_Recommendation_Cleaned.csv` di folder proyek ini.
2. Install dependency:

```bash
pip install -r requirements.txt
```

3. Jalankan Streamlit:

```bash
streamlit run streamlit_app.py
```

4. Buka browser pada alamat yang ditampilkan oleh Streamlit.
