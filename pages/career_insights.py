import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from utils import get_top_categories, format_int

def render_career_insights(df: pd.DataFrame, template: str) -> None:
    """Render comprehensive career insights with multiple analysis tabs."""
    
    st.markdown("# 💼 Career Insights")
    st.markdown(
        "🔍 Analisis mendalam tentang rekomendasi karier, hubungan dengan berbagai faktor, "
        "dan insight untuk pengambilan keputusan karier."
    )
    
    # Create tabs for different analysis types
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "📈 Career Analysis",
        "🎓 Academic Analysis",
        "🏆 Skills Analysis"
    ])
    
    # ============== TAB 1: OVERVIEW ==============
    with tab1:
        st.markdown("## Career Overview")
        
        # Top careers
        st.markdown("### 🏆 Top 10 Recommended Careers")
        
        if "Rekomendasi Karier" in df.columns:
            top_careers = df["Rekomendasi Karier"].value_counts().head(10).reset_index()
            top_careers.columns = ["Rekomendasi Karier", "Count"]
            top_careers['Percentage'] = (top_careers['Count'] / top_careers['Count'].sum() * 100).round(2)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.bar(
                    top_careers,
                    x="Count",
                    y="Rekomendasi Karier",
                    orientation="h",
                    title="Top 10 Careers by Recommendation Count",
                    template=template,
                    color="Count",
                    color_continuous_scale="Viridis",
                    text="Count"
                )
                fig.update_layout(height=400)
                fig.update_traces(textposition='auto')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.metric("Total Career Types", df["Rekomendasi Karier"].nunique())
                st.metric("Most Recommended", top_careers["Rekomendasi Karier"].iloc[0])
                st.metric("Top Career Count", format_int(int(top_careers["Count"].iloc[0])))
            
            # Detailed table
            st.markdown("#### Detailed Career Rankings")
            st.dataframe(
                top_careers,
                use_container_width=True,
                hide_index=True
            )
        
        st.markdown("---")
        
        # Top majors
        st.markdown("### 🎓 Top 10 Majors")
        
        if "Jurusan" in df.columns:
            top_majors = df["Jurusan"].value_counts().head(10).reset_index()
            top_majors.columns = ["Jurusan", "Count"]
            top_majors['Percentage'] = (top_majors['Count'] / top_majors['Count'].sum() * 100).round(2)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.bar(
                    top_majors,
                    x="Count",
                    y="Jurusan",
                    orientation="h",
                    title="Top 10 Majors by Count",
                    template=template,
                    color="Count",
                    color_continuous_scale="Blues",
                    text="Count"
                )
                fig.update_layout(height=400)
                fig.update_traces(textposition='auto')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.metric("Total Majors", df["Jurusan"].nunique())
                st.metric("Most Common Major", top_majors["Jurusan"].iloc[0])
                st.metric("Top Major Count", format_int(int(top_majors["Count"].iloc[0])))
        
        st.markdown("---")
        
        # Top interest fields
        st.markdown("### 💡 Top 10 Interest Fields")
        
        if "Bidang Minat" in df.columns:
            top_interests = df["Bidang Minat"].value_counts().head(10).reset_index()
            top_interests.columns = ["Bidang Minat", "Count"]
            top_interests['Percentage'] = (top_interests['Count'] / top_interests['Count'].sum() * 100).round(2)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.bar(
                    top_interests,
                    x="Count",
                    y="Bidang Minat",
                    orientation="h",
                    title="Top 10 Interest Fields by Count",
                    template=template,
                    color="Count",
                    color_continuous_scale="Reds",
                    text="Count"
                )
                fig.update_layout(height=400)
                fig.update_traces(textposition='auto')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.metric("Total Interest Fields", df["Bidang Minat"].nunique())
                st.metric("Most Popular Interest", top_interests["Bidang Minat"].iloc[0])
                st.metric("Top Interest Count", format_int(int(top_interests["Count"].iloc[0])))
    
    # ============== TAB 2: CAREER ANALYSIS ==============
    with tab2:
        st.markdown("## Career-Based Analysis")
        
        st.markdown("### 🔗 Career Relationships")
        
        if all(col in df.columns for col in ["Rekomendasi Karier", "Jurusan"]):
            st.markdown("#### Top Majors for Each Career")
            
            # Select career to analyze
            careers = df["Rekomendasi Karier"].unique()
            selected_career = st.selectbox("Select Career to Analyze", careers)
            
            if selected_career:
                career_df = df[df["Rekomendasi Karier"] == selected_career]
                top_majors_for_career = career_df["Jurusan"].value_counts().head(10)
                
                st.metric(f"Students in {selected_career}", len(career_df))
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig = px.bar(
                        x=top_majors_for_career.values,
                        y=top_majors_for_career.index,
                        orientation="h",
                        title=f"Top Majors for: {selected_career}",
                        template=template,
                        labels={"x": "Count", "y": "Major"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.write(f"**Majors in {selected_career}:**")
                    for major, count in top_majors_for_career.items():
                        st.write(f"- {major}: {count}")
        
        st.markdown("---")
        
        if all(col in df.columns for col in ["Rekomendasi Karier", "Bidang Minat"]):
            st.markdown("#### Interest Fields by Career")
            
           # Ambil 8 karier teratas
            top_careers = df["Rekomendasi Karier"].value_counts().head(8).index

            # Filter dataframe
            df_filtered = df[
                df["Rekomendasi Karier"].isin(top_careers)
            ]

            # Crosstab yang benar
            crosstab = pd.crosstab(
                df_filtered["Rekomendasi Karier"],
                df_filtered["Bidang Minat"]
            )

            fig = px.imshow(
                crosstab,
                labels={
                    "x": "Interest Field",
                    "y": "Career",
                    "color": "Count"
                },
                title="Career vs Interest Field Heatmap (Top 8 Careers)",
                template=template,
                color_continuous_scale="YlOrRd"
            )

            fig.update_layout(
                height=450,
                xaxis_tickangle=-45
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
                
    # ============== TAB 3: ACADEMIC ANALYSIS ==============
    with tab3:
        st.markdown("## Academic Metrics Analysis")
        
        st.markdown("### 📚 IPK Distribution by Career")
        
        if all(col in df.columns for col in ["IPK", "Rekomendasi Karier"]):
            # Get top careers for cleaner visualization
            top_careers_list = df["Rekomendasi Karier"].value_counts().head(10).index
            df_filtered = df[df["Rekomendasi Karier"].isin(top_careers_list)]
            
            fig = px.box(
                df_filtered,
                x="Rekomendasi Karier",
                y="IPK",
                title="IPK Distribution by Top 10 Careers",
                template=template,
                color="Rekomendasi Karier",
                points="outliers"
            )
            fig.update_layout(height=400, xaxis_tickangle=-45, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics table
            st.markdown("#### IPK Statistics by Career")
            ipk_stats = df.groupby("Rekomendasi Karier")["IPK"].agg([
                "count", "mean", "median", "std", "min", "max"
            ]).round(2).sort_values("mean", ascending=False)
            
            st.dataframe(ipk_stats.head(10), use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🏅 Certifications by Career")
        
        if all(col in df.columns for col in ["Jumlah Sertifikasi", "Rekomendasi Karier"]):
            top_careers_list = df["Rekomendasi Karier"].value_counts().head(10).index
            df_filtered = df[df["Rekomendasi Karier"].isin(top_careers_list)]
            
            fig = px.box(
                df_filtered,
                x="Rekomendasi Karier",
                y="Jumlah Sertifikasi",
                title="Certification Distribution by Top 10 Careers",
                template=template,
                color="Rekomendasi Karier",
                points="outliers"
            )
            fig.update_layout(height=400, xaxis_tickangle=-45, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics table
            st.markdown("#### Certification Statistics by Career")
            cert_stats = df.groupby("Rekomendasi Karier")["Jumlah Sertifikasi"].agg([
                "count", "mean", "median", "max"
            ]).round(2).sort_values("mean", ascending=False)
            
            st.dataframe(cert_stats.head(10), use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🎯 Combined Academic Performance")
        
        # Scatter plot: IPK vs Certifications colored by career
        if all(col in df.columns for col in ["IPK", "Jumlah Sertifikasi", "Rekomendasi Karier"]):
            top_careers_list = df["Rekomendasi Karier"].value_counts().head(5).index
            df_filtered = df[df["Rekomendasi Karier"].isin(top_careers_list)]
            
            fig = px.scatter(
                df_filtered,
                x="IPK",
                y="Jumlah Sertifikasi",
                color="Rekomendasi Karier",
                title="IPK vs Certifications by Career (Top 5)",
                template=template,
                labels={"IPK": "IPK Score", "Jumlah Sertifikasi": "Number of Certifications"},
                opacity=0.6
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    # ============== TAB 4: SKILLS ANALYSIS ==============
    with tab4:
        st.markdown("## Skills & Competencies Analysis")
        
        skill_cols = [
            "Kepemimpinan", "Komunikasi", "Kerja Tim", "Kreativitas",
            "Berpikir Kritis", "Pemecahan Masalah"
        ]
        
        existing_skills = [col for col in skill_cols if col in df.columns]
        
        if existing_skills:
            st.markdown("### 📊 Skills Profile by Career")
            
            # Select career
            selected_career = st.selectbox(
                "Select Career",
                df["Rekomendasi Karier"].unique(),
                key="skills_career"
            )
            
            if selected_career:
                career_df = df[df["Rekomendasi Karier"] == selected_career]
                
                # Calculate average skills
                avg_skills = career_df[existing_skills].mean()
                
                # Radar chart
                fig = go.Figure(data=go.Scatterpolar(
                    r=avg_skills.values,
                    theta=avg_skills.index,
                    fill='toself',
                    name=selected_career
                ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                    title=f"Skills Profile: {selected_career}",
                    height=500,
                    template=template
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Skills comparison table
                st.markdown("#### Skills Comparison (Top 5 Careers)")
                
                top_careers = df["Rekomendasi Karier"].value_counts().head(5).index
                skills_comparison = []
                
                for career in top_careers:
                    career_data = df[df["Rekomendasi Karier"] == career][existing_skills].mean()
                    skills_comparison.append(career_data)
                
                skills_df = pd.DataFrame(skills_comparison, index=top_careers).round(2)
                st.dataframe(skills_df, use_container_width=True)
                
                # Heatmap
                st.markdown("#### Skills Heatmap (Top 8 Careers)")
                
                top_careers_8 = df["Rekomendasi Karier"].value_counts().head(8).index
                skills_data = []
                
                for career in top_careers_8:
                    career_data = df[df["Rekomendasi Karier"] == career][existing_skills].mean()
                    skills_data.append(career_data.values)
                
                fig = px.imshow(
                    skills_data,
                    labels=dict(x="Skill", y="Career", color="Average Score"),
                    x=existing_skills,
                    y=top_careers_8,
                    title="Skills Heatmap by Career",
                    template=template,
                    color_continuous_scale="RdYlGn"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🎖️ Overall Skills Distribution")
        
        if existing_skills:
            # Compare skills distributions
            selected_skills = st.multiselect(
                "Select Skills to Compare",
                existing_skills,
                default=existing_skills[:3]
            )
            
            if selected_skills:
                # Violin plot
                fig = go.Figure()
                
                for skill in selected_skills:
                    fig.add_trace(go.Violin(
                        y=df[skill],
                        name=skill,
                        box_visible=True,
                        meanline_visible=True
                    ))
                
                fig.update_layout(
                    title="Skills Distribution Comparison",
                    yaxis_title="Score",
                    template=template,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("## 📌 Key Takeaways")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"""
        **Most Recommended Career:**
        {df['Rekomendasi Karier'].value_counts().index[0]}
        
        **Count:** {df['Rekomendasi Karier'].value_counts().iloc[0]:,}
        """)
    
    with col2:
        st.success(f"""
        **Most Common Major:**
        {df['Jurusan'].value_counts().index[0]}
        
        **Count:** {df['Jurusan'].value_counts().iloc[0]:,}
        """)
    
    with col3:
        st.warning(f"""
        **Average IPK:**
        {df['IPK'].mean():.2f}
        
        **Average Certifications:**
        {df['Jumlah Sertifikasi'].mean():.1f}
        """)

    st.markdown("---")
    st.subheader("Hubungan Jumlah Sertifikasi terhadap Rekomendasi Karier")
    if all(col in df.columns for col in ["Jumlah Sertifikasi", "Rekomendasi Karier"]):
        fig = px.box(
            df,
            x="Rekomendasi Karier",
            y="Jumlah Sertifikasi",
            template=template,
        )
        fig.update_layout(xaxis_title="Rekomendasi Karier", yaxis_title="Jumlah Sertifikasi", title="Distribusi Sertifikasi per Rekomendasi Karier")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Kolom Jumlah Sertifikasi atau Rekomendasi Karier tidak ditemukan untuk analisis ini.")

    st.markdown("---")
    st.subheader("Hubungan Pengalaman Magang terhadap Rekomendasi Karier")
    if all(col in df.columns for col in ["Pengalaman Magang", "Rekomendasi Karier"]):
        fig = px.box(
            df,
            x="Rekomendasi Karier",
            y="Pengalaman Magang",
            template=template,
        )
        fig.update_layout(xaxis_title="Rekomendasi Karier", yaxis_title="Pengalaman Magang (bulan)", title="Distribusi Pengalaman Magang per Rekomendasi Karier")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Kolom Pengalaman Magang atau Rekomendasi Karier tidak ditemukan untuk analisis ini.")
