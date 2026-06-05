from tempfile import template

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from utils import (
    create_bar_chart, create_histogram, create_pie_chart,
    create_box_plot, create_correlation_heatmap
)

def render_eda(df: pd.DataFrame, template: str) -> None:
    """Render comprehensive exploratory data analysis page."""
    
    st.markdown("# 📈 Exploratory Data Analysis")
    st.markdown(
        "🔍 Halaman ini menyediakan analisis visual mendalam untuk mengidentifikasi pola, "
        "tren, dan insight penting dari dataset karier."
    )
    
    # Tabs for different analysis types
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔢 Categorical Distribution",
        "📊 Numeric Analysis",
        "🔗 Correlation Analysis",
        "📈 Comparative Analysis",
        "💡 Insights"
    ])
    
    # ============== TAB 1: CATEGORICAL DISTRIBUTION ==============
    with tab1:
        st.markdown("## Categorical Features Distribution")
        st.write("Analisis distribusi fitur kategorikal untuk memahami komposisi dataset.")
        
        st.markdown("---")
        st.markdown("### 🎓 Distribusi Jurusan")
        if "Jurusan" in df.columns:
            majors = df["Jurusan"].value_counts().head(15).reset_index()
            majors.columns = ["Jurusan", "Count"]
            
            col1, col2 = st.columns([2, 1])
            with col1:
                fig = px.bar(
                    majors,
                    x="Jurusan",
                    y="Count",
                    title="Top 15 Majors by Frequency",
                    template=template,
                    color="Count",
                    color_continuous_scale="Viridis"
                )
                fig.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.metric("Total Unique Majors", df["Jurusan"].nunique())
                st.metric("Most Common", majors["Jurusan"].iloc[0])
        
        st.markdown("---")
        st.markdown("### 💡 Distribusi Bidang Minat")
        if "Bidang Minat" in df.columns:
            interests = df["Bidang Minat"].value_counts().reset_index()
            interests.columns = ["Bidang Minat", "Count"]
            
            fig = px.pie(
                interests,
                names="Bidang Minat",
                values="Count",
                title="Interest Fields Distribution",
                template=template
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 💼 Distribusi Tujuan Karier")
        if "Tujuan Karier" in df.columns:
            goals = df["Tujuan Karier"].value_counts().reset_index()
            goals.columns = ["Tujuan Karier", "Count"]
            
            fig = px.bar(
                goals,
                x="Count",
                y="Tujuan Karier",
                orientation="h",
                title="Career Goals Distribution",
                template=template,
                color="Count",
                color_continuous_scale="Blues"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 👔 Distribusi Gaya Kerja")
        if "Gaya Kerja" in df.columns:
            fig = px.pie(
                df["Gaya Kerja"].value_counts().reset_index(),
                names="Gaya Kerja",
                values="count",
                title="Work Style Composition",
                template=template
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🏢 Distribusi Preferensi Industri")
        if "Preferensi Industri" in df.columns:
            industries = df["Preferensi Industri"].value_counts().head(12).reset_index()
            industries.columns = ["Preferensi Industri", "Count"]
            
            fig = px.bar(
                industries,
                x="Preferensi Industri",
                y="Count",
                title="Top 12 Industry Preferences",
                template=template,
                text="Count"
            )
            fig.update_layout(height=400, xaxis_tickangle=-45)
            fig.update_traces(textposition='auto')
            st.plotly_chart(fig, use_container_width=True)
    
    # ============== TAB 2: NUMERIC ANALYSIS ==============
    with tab2:
        st.markdown("## Numeric Features Analysis")
        st.write("Analisis distribusi dan statistik untuk fitur numerik.")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        st.markdown("---")
        st.markdown("### 📚 IPK Distribution")
        if "IPK" in df.columns:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mean IPK", f"{df['IPK'].mean():.2f}")
            with col2:
                st.metric("Median IPK", f"{df['IPK'].median():.2f}")
            with col3:
                st.metric("Std Dev", f"{df['IPK'].std():.2f}")
            
            fig = px.histogram(
                df,
                x="IPK",
                nbins=30,
                title="IPK Distribution with Box Plot",
                template=template,
                marginal="box",
                color_discrete_sequence=["#667eea"]
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🏅 Sertifikasi Distribution")
        if "Jumlah Sertifikasi" in df.columns:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mean Certifications", f"{df['Jumlah Sertifikasi'].mean():.2f}")
            with col2:
                st.metric("Max Certifications", f"{int(df['Jumlah Sertifikasi'].max())}")
            with col3:
                st.metric("Unique Values", df["Jumlah Sertifikasi"].nunique())
            
            fig = px.histogram(
                df,
                x="Jumlah Sertifikasi",
                nbins=20,
                title="Certification Count Distribution",
                template=template,
                marginal="rug",
                color_discrete_sequence=["#764ba2"]
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🎯 Skill Metrics Distribution")
        
        skill_cols = [
            "Kepemimpinan", "Komunikasi", "Kerja Tim", "Kreativitas",
            "Berpikir Kritis", "Pemecahan Masalah"
        ]
        
        existing_skills = [col for col in skill_cols if col in df.columns]
        
        if existing_skills:
            selected_skill = st.selectbox("Select Skill to Analyze", existing_skills)
            
            if selected_skill:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Mean", f"{df[selected_skill].mean():.2f}")
                with col2:
                    st.metric("Median", f"{df[selected_skill].median():.2f}")
                with col3:
                    st.metric("Range", f"{df[selected_skill].min():.1f} - {df[selected_skill].max():.1f}")
                
                fig = px.histogram(
                    df,
                    x=selected_skill,
                    nbins=20,
                    title=f"{selected_skill} Distribution",
                    template=template,
                    marginal="box"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📊 Multiple Numeric Features Comparison")
        
        selected_features = st.multiselect(
            "Select features to compare",
            numeric_cols,
            default=numeric_cols[:3] if len(numeric_cols) > 0 else []
        )
        
        if selected_features:
            # Create subplots for comparison
            n_cols = min(len(selected_features), 3)
            cols = st.columns(n_cols)
            
            for idx, col in enumerate(selected_features):
                with cols[idx % n_cols]:
                    st.metric(col, f"{df[col].mean():.2f}")
            
            # Distribution comparison
            fig = go.Figure()
            for col in selected_features:
                fig.add_trace(go.Histogram(x=df[col], name=col, opacity=0.7))
            
            fig.update_layout(
                barmode='overlay',
                title="Numeric Features Distribution Comparison",
                xaxis_title="Value",
                yaxis_title="Frequency",
                height=400,
                template=template
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ============== TAB 3: CORRELATION ANALYSIS ==============
    with tab3:
        st.markdown("## Correlation Analysis")
        st.write("Analisis hubungan antar fitur numerik untuk mengidentifikasi multicollinearity.")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) > 1:
            # Full correlation heatmap
            st.markdown("### 🔗 Full Correlation Matrix")
            
            fig = create_correlation_heatmap(df, template)
            st.plotly_chart(fig, use_container_width=True)
            
            # Correlation insights
            st.markdown("---")
            st.markdown("### 📌 Key Correlations")
            
            corr_matrix = df[numeric_cols].corr()
            
            # Find strong correlations
            strong_corrs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.5:
                        strong_corrs.append({
                            'Feature 1': corr_matrix.columns[i],
                            'Feature 2': corr_matrix.columns[j],
                            'Correlation': corr_value
                        })
            
            if strong_corrs:
                strong_df = pd.DataFrame(strong_corrs).sort_values('Correlation', 
                                                                   key=abs, 
                                                                   ascending=False)
                st.info("Strong correlations (|r| > 0.5):")
                st.dataframe(strong_df, use_container_width=True)
            else:
                st.info("No strong correlations found (|r| > 0.5)")
        else:
            st.warning("Not enough numeric columns for correlation analysis")
    
    # ============== TAB 4: COMPARATIVE ANALYSIS ==============
    with tab4:
        st.markdown("## Comparative Analysis")
        st.write("Analisis hubungan antar variabel kategorikal dan numerik.")
        
        st.markdown("---")
        st.markdown("### 📈 IPK by Major")
        
        if "IPK" in df.columns and "Jurusan" in df.columns:
            top_majors = df["Jurusan"].value_counts().head(10).index
            df_filtered = df[df["Jurusan"].isin(top_majors)]
            
            fig = px.box(
                df_filtered,
                x="Jurusan",
                y="IPK",
                title="IPK Distribution by Top 10 Majors",
                template=template,
                color="Jurusan"
            )
            fig.update_layout(height=400, xaxis_tickangle=-45, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🏅 Certifications by Career Recommendation")
        
        if "Jumlah Sertifikasi" in df.columns and "Rekomendasi Karier" in df.columns:
            top_careers = df["Rekomendasi Karier"].value_counts().head(8).index
            df_filtered = df[df["Rekomendasi Karier"].isin(top_careers)]
            
            fig = px.box(
                df_filtered,
                x="Rekomendasi Karier",
                y="Jumlah Sertifikasi",
                title="Certification Count by Recommended Career (Top 8)",
                template=template,
                color="Rekomendasi Karier"
            )
            fig.update_layout(height=400, xaxis_tickangle=-45, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🎯 Interest Field vs Career Recommendation")
        
        if "Bidang Minat" in df.columns and "Rekomendasi Karier" in df.columns:

            # Ambil 8 bidang minat teratas
            top_interests = df["Bidang Minat"].value_counts().head(8).index

            # Filter dataframe
            df_filtered = df[
                df["Bidang Minat"].isin(top_interests)
            ]

            # Crosstab yang benar
            crosstab = pd.crosstab(
                df_filtered["Bidang Minat"],
                df_filtered["Rekomendasi Karier"]
            )

            st.write("Shape df_filtered:", df_filtered.shape)
            st.write("Shape crosstab:", crosstab.shape)

            fig = px.imshow(
                crosstab,
                labels={
                    "x": "Career Recommendation",
                    "y": "Interest Field",
                    "color": "Count"
                },
                title="Interest Field vs Career Recommendation Heatmap",
                template=template,
                color_continuous_scale="Viridis"
            )

            fig.update_layout(
                height=450,
                xaxis_tickangle=-45
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ============== TAB 5: INSIGHTS ==============
    with tab5:
        st.markdown("## 💡 Data Insights & Summary")
        
        st.markdown("### Key Findings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Distribution Insights")
            st.info(f"""
            **Major Distribution:**
            - Total Majors: {df['Jurusan'].nunique()}
            - Most Common: {df['Jurusan'].value_counts().index[0]}
            
            **Interest Fields:**
            - Total Fields: {df['Bidang Minat'].nunique()}
            - Most Popular: {df['Bidang Minat'].value_counts().index[0]}
            """)
        
        with col2:
            st.markdown("#### Performance Insights")
            st.info(f"""
            **Academic Metrics:**
            - Avg IPK: {df['IPK'].mean():.2f}
            - Avg Certifications: {df['Jumlah Sertifikasi'].mean():.2f}
            
            **Career Path:**
            - Total Career Types: {df['Rekomendasi Karier'].nunique()}
            - Most Recommended: {df['Rekomendasi Karier'].value_counts().index[0]}
            """)
        
        st.markdown("---")
        st.markdown("### Data Quality Summary")
        
        quality_metrics = pd.DataFrame({
            'Metric': ['Total Records', 'Total Features', 'Missing Values %', 'Duplicate Records'],
            'Value': [
                f"{len(df):,}",
                f"{len(df.columns)}",
                f"{(df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100):.2f}%",
                f"{df.duplicated().sum()}"
            ]
        })
        
        st.dataframe(quality_metrics, use_container_width=True)
