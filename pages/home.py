import streamlit as st
import pandas as pd
from utils import (
    format_int, format_float, get_data_insights, 
    get_data_statistics, get_categorical_stats
)

def render_home(df: pd.DataFrame, template: str) -> None:
    """Render enhanced home page with hero section and KPIs."""
    
    # Hero section
    st.markdown("""
    <div class='hero-section'>
        <h1>🎓 AI Career Recommendation Dashboard</h1>
        <p>Platform analitik terdepan untuk rekomendasi karier berbasis Artificial Intelligence.<br/>
        Jelajahi dataset 49,500+ mahasiswa dengan 20 fitur komprehensif.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main KPI metrics
    st.markdown("### 📊 Dataset Overview")
    
    stats = get_data_statistics(df)
    
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        st.metric(
            "📋 Total Data",
            format_int(stats['total_rows']),
            "Records"
        )
    
    with col2:
        st.metric(
            "🏢 Total Jurusan",
            format_int(df['Jurusan'].nunique()),
            "Programs"
        )
    
    with col3:
        st.metric(
            "💡 Total Bidang Minat",
            format_int(df['Bidang Minat'].nunique()),
            "Fields"
        )
    
    with col4:
        st.metric(
            "👔 Total Karier",
            format_int(df['Rekomendasi Karier'].nunique()),
            "Careers"
        )
    
    # Academic metrics
    st.markdown("### 🎯 Academic Performance Metrics")
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        avg_ipk = df['IPK'].mean()
        st.metric(
            "📚 Rata-rata IPK",
            format_float(avg_ipk, 2),
            f"Range: {df['IPK'].min():.2f} - {df['IPK'].max():.2f}"
        )
    
    with col2:
        avg_cert = df['Jumlah Sertifikasi'].mean()
        st.metric(
            "🏅 Rata-rata Sertifikasi",
            format_float(avg_cert, 1),
            f"Max: {int(df['Jumlah Sertifikasi'].max())}"
        )
    
    with col3:
        st.metric(
            "📁 Total Fitur",
            format_int(len(df.columns)),
            "Columns"
        )
    
    # Key insights
    st.markdown("---")
    st.markdown("### 💡 Key Insights")
    
    insights = get_data_insights(df)
    
    insight_cols = st.columns(2)
    
    with insight_cols[0]:
        if 'major' in insights:
            st.info(f"🎓 {insights['major']}")
        if 'career' in insights:
            st.success(f"💼 {insights['career']}")
    
    with insight_cols[1]:
        if 'interest' in insights:
            st.info(f"🌟 {insights['interest']}")
        if 'gpa' in insights:
            st.success(f"📊 {insights['gpa']}")
    
    st.markdown("---")
    
    # Data quality information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "✅ Data Completeness",
            f"{((len(df) - stats['missing_values']) / (len(df) * len(df.columns)) * 100):.1f}%"
        )
    
    with col2:
        st.metric(
            "🔄 Duplicate Records",
            format_int(stats['duplicates'])
        )
    
    with col3:
        st.metric(
            "💾 Memory Usage",
            stats['memory_usage']
        )
    
    # Feature overview
    st.markdown("---")
    st.markdown("### 📋 Feature Overview")
    
    with st.expander("📖 View Complete Feature List"):
        st.write("""
        **Numeric Features:**
        - IPK (Indeks Prestasi Kumulatif)
        - Jumlah Sertifikasi
        - Kepemimpinan (Leadership)
        - Komunikasi (Communication)
        - Kerja Tim (Teamwork)
        - Kreativitas (Creativity)
        - Berpikir Kritis (Critical Thinking)
        - Pemecahan Masalah (Problem Solving)
        
        **Categorical Features:**
        - Jurusan (Major)
        - Bidang Minat (Interest Field)
        - Keahlian 1, 2, 3 (Skills)
        - Pengalaman Magang (Internship Experience)
        - Pengalaman Organisasi (Organization Experience)
        - Pengalaman Kompetisi (Competition Experience)
        - Gaya Kerja (Work Style)
        - Preferensi Industri (Industry Preference)
        - Tujuan Karier (Career Goal)
        - Rekomendasi Karier (Career Recommendation)
        """)
    
    # Top categories preview
    st.markdown("---")
    st.markdown("### 🔍 Top Categories Preview")
    
    preview_cols = st.columns(3)
    
    with preview_cols[0]:
        with st.expander("🎓 Top 5 Jurusan"):
            top_majors = df['Jurusan'].value_counts().head(5)
            for i, (major, count) in enumerate(top_majors.items(), 1):
                st.write(f"{i}. **{major}** - {count:,} ({count/len(df)*100:.1f}%)")
    
    with preview_cols[1]:
        with st.expander("💡 Top 5 Bidang Minat"):
            top_interests = df['Bidang Minat'].value_counts().head(5)
            for i, (interest, count) in enumerate(top_interests.items(), 1):
                st.write(f"{i}. **{interest}** - {count:,} ({count/len(df)*100:.1f}%)")
    
    with preview_cols[2]:
        with st.expander("💼 Top 5 Karier"):
            top_careers = df['Rekomendasi Karier'].value_counts().head(5)
            for i, (career, count) in enumerate(top_careers.items(), 1):
                st.write(f"{i}. **{career}** - {count:,} ({count/len(df)*100:.1f}%)")
    
    # Sample data
    st.markdown("---")
    st.markdown("### 👁️ Data Preview")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**Sample dari dataset (10 baris pertama):**")
    with col2:
        sample_size = st.selectbox("Show", [5, 10, 20], index=1, key="sample_size")
    
    st.dataframe(
        df.head(sample_size),
        use_container_width=True,
        height=300
    )
    
    # Footer info
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; font-size: 0.9rem; margin-top: 2rem;'>
        <p>🔒 <strong>Data Privacy:</strong> Semua data telah dianonimkan untuk keperluan penelitian.</p>
        <p>📅 <strong>Last Updated:</strong> 2026 | <strong>Version:</strong> 2.0 Professional Edition</p>
    </div>
    """, unsafe_allow_html=True)
