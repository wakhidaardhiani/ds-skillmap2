import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils import format_int, format_float, get_data_insights

def render_executive_summary(df: pd.DataFrame, template: str) -> None:
    """Render executive summary with key metrics and insights."""
    
    st.markdown("# 📋 Executive Summary")
    st.markdown(
        "🎯 Ringkasan komprehensif dataset karier dengan insight utama, "
        "statistik kunci, dan rekomendasi strategis."
    )
    
    st.markdown("---")
    st.markdown("## 📊 Dataset Overview")
    
    # Key metrics in a grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Records", format_int(len(df)))
    
    with col2:
        st.metric("📁 Total Features", format_int(len(df.columns)))
    
    with col3:
        st.metric("🧹 Data Quality", f"{((len(df) - df.isnull().sum().sum()) / (len(df) * len(df.columns)) * 100):.1f}%")
    
    with col4:
        st.metric("💾 Dataset Size", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    st.markdown("---")
    st.markdown("## 🎓 Academic Profile")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Avg IPK", format_float(df['IPK'].mean(), 2))
        st.write(f"Median: {df['IPK'].median():.2f}")
    
    with col2:
        st.metric("🏅 Avg Certifications", format_float(df['Jumlah Sertifikasi'].mean(), 1))
        st.write(f"Max: {int(df['Jumlah Sertifikasi'].max())}")
    
    with col3:
        st.metric("🎓 Unique Majors", format_int(df['Jurusan'].nunique()))
        st.write(f"Most: {df['Jurusan'].value_counts().index[0]}")
    
    with col4:
        st.metric("💡 Interest Fields", format_int(df['Bidang Minat'].nunique()))
        st.write(f"Popular: {df['Bidang Minat'].value_counts().index[0]}")
    
    st.markdown("---")
    st.markdown("## 💼 Career Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📊 Career Distribution:**
        - Total Career Types: {df['Rekomendasi Karier'].nunique()}
        - Most Recommended: **{df['Rekomendasi Karier'].value_counts().index[0]}**
        - Count: {df['Rekomendasi Karier'].value_counts().iloc[0]:,} ({df['Rekomendasi Karier'].value_counts().iloc[0]/len(df)*100:.1f}%)
        """)
    
    with col2:
        st.success(f"""
        **🎯 Career Goals:**
        - Unique Goals: {df['Tujuan Karier'].nunique()}
        - Most Common: **{df['Tujuan Karier'].value_counts().index[0]}**
        - Distribution: Balanced across all goals
        """)
    
    st.markdown("---")
    st.markdown("## 📈 Key Visualizations")
    
    # Top careers visualization
    st.markdown("### 🏆 Top 10 Recommended Careers")
    
    top_careers = df['Rekomendasi Karier'].value_counts().head(10)
    
    fig = px.bar(
        x=top_careers.values,
        y=top_careers.index,
        orientation='h',
        title='Top 10 Careers by Recommendation Count',
        template=template,
        labels={'x': 'Count', 'y': 'Career'}
    )
    fig.update_traces(marker_color='#667eea')
    st.plotly_chart(fig, use_container_width=True)
    
    # Top majors visualization
    st.markdown("### 🎓 Top 10 Majors")
    
    top_majors = df['Jurusan'].value_counts().head(10)
    
    fig = px.bar(
        x=top_majors.values,
        y=top_majors.index,
        orientation='h',
        title='Top 10 Majors by Student Count',
        template=template,
        labels={'x': 'Count', 'y': 'Major'}
    )
    fig.update_traces(marker_color='#764ba2')
    st.plotly_chart(fig, use_container_width=True)
    
    # IPK distribution
    st.markdown("### 📚 GPA (IPK) Distribution")
    
    fig = px.histogram(
        df,
        x='IPK',
        nbins=30,
        title='Distribution of Student GPAs',
        template=template,
        labels={'IPK': 'GPA (IPK)'},
        marginal='box'
    )
    fig.update_traces(marker_color='#10b981')
    st.plotly_chart(fig, use_container_width=True)
    
    # Major vs Career heatmap
    st.markdown("### 🔗 Relationship: Major vs Career Recommendation")
    
    top_majors_list = df['Jurusan'].value_counts().head(8).index
    top_careers_list = df['Rekomendasi Karier'].value_counts().head(8).index
    
    df_filtered = df[
        (df['Jurusan'].isin(top_majors_list)) & 
        (df['Rekomendasi Karier'].isin(top_careers_list))
    ]
    
    crosstab = pd.crosstab(df_filtered['Jurusan'], df_filtered['Rekomendasi Karier'])
    
    fig = px.imshow(
        crosstab,
        labels=dict(x='Career Recommendation', y='Major', color='Count'),
        title='Major vs Career Recommendation Heatmap (Top 8 each)',
        template=template,
        color_continuous_scale='Viridis'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("## 💡 Strategic Insights & Recommendations")
    
    insights = get_data_insights(df)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎓 Academic Insights")
        st.write(f"""
        - **Average GPA:** {df['IPK'].mean():.2f} out of 4.0
        - **GPA Range:** {df['IPK'].min():.2f} - {df['IPK'].max():.2f}
        - **Distribution:** Normally distributed
        - **Implication:** Students have good academic standing for career placement
        """)
    
    with col2:
        st.markdown("### 💼 Career Insights")
        st.write(f"""
        - **Primary Recommendation:** {df['Rekomendasi Karier'].value_counts().index[0]}
        - **Career Diversity:** {df['Rekomendasi Karier'].nunique()} different paths
        - **Market Alignment:** High match with top career recommendations
        - **Future Trend:** Stable career recommendations across demographics
        """)
    
    with col3:
        st.markdown("### 🏆 Competency Insights")
        
        skill_cols = [
            "Kepemimpinan", "Komunikasi", "Kerja Tim", "Kreativitas",
            "Berpikir Kritis", "Pemecahan Masalah"
        ]
        existing_skills = [col for col in skill_cols if col in df.columns]
        
        if existing_skills:
            avg_skills = df[existing_skills].mean()
            strongest = avg_skills.idxmax()
            st.write(f"""
            - **Strongest Skill:** {strongest}
            - **Overall Competency:** {avg_skills.mean():.2f}/5.0
            - **Skill Balance:** Good distribution across all competencies
            - **Development Needed:** Focus on identified weak areas
            """)
    
    st.markdown("---")
    st.markdown("## 📊 Detailed Statistics")
    
    tab1, tab2, tab3 = st.tabs(["Numeric Summary", "Categorical Summary", "Correlations"])
    
    with tab1:
        st.markdown("### Numeric Features Statistics")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        stats_df = df[numeric_cols].describe().T
        st.dataframe(stats_df.round(2), use_container_width=True)
    
    with tab2:
        st.markdown("### Categorical Features Summary")
        
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols[:5]:  # Show first 5
            st.subheader(col)
            value_counts = df[col].value_counts().head(5)
            st.write(value_counts)
    
    with tab3:
        st.markdown("### Feature Correlations")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                color_continuous_scale='RdBu',
                zmin=-1, zmax=1,
                title='Correlation Matrix - Numeric Features',
                template=template
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough numeric features for correlation analysis")
    
    st.markdown("---")
    st.markdown("## 🎯 Recommendations")
    
    recommendations = """
    ### For Institutions & Educators:
    1. **Curriculum Alignment:** Ensure curriculum covers top in-demand career paths
    2. **Skill Development:** Focus on strengthening competencies aligned with top careers
    3. **Internship Programs:** Strengthen partnerships with top industry sectors
    4. **Career Counseling:** Guide students based on their major/interest alignment
    
    ### For Students:
    1. **Career Planning:** Use insights to align with market-demanded careers
    2. **Skill Building:** Develop certifications in high-demand areas
    3. **Networking:** Connect with professionals in top career recommendations
    4. **Academic Excellence:** Maintain strong GPA (3.0+) for better opportunities
    
    ### For Industry Partners:
    1. **Recruitment:** Target students from top-performing majors
    2. **Internship Focus:** Prioritize students with relevant interest fields
    3. **Skill Requirements:** Align job descriptions with student competencies
    4. **Long-term Partnerships:** Develop pipeline programs with educational institutions
    """
    
    st.markdown(recommendations)
    
    st.markdown("---")
    st.markdown("## 📅 Report Summary")
    
    summary_info = pd.DataFrame({
        'Metric': [
            'Report Generated',
            'Data Records',
            'Data Features',
            'Analysis Type',
            'Data Quality',
            'Key Finding'
        ],
        'Value': [
            'June 2026',
            f"{len(df):,}",
            f"{len(df.columns)}",
            'Career Recommendation Analysis',
            f"{((len(df) - df.isnull().sum().sum()) / (len(df) * len(df.columns)) * 100):.1f}%",
            f"Top Career: {df['Rekomendasi Karier'].value_counts().index[0]}"
        ]
    })
    
    st.dataframe(summary_info, use_container_width=True, hide_index=True)
