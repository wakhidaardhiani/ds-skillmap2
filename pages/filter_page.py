import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from utils import format_int, export_data_to_csv, filter_dataframe

def render_filters(df: pd.DataFrame, template: str) -> None:
    """Render interactive filter page with advanced features."""
    
    st.markdown("# 🧩 Interactive Filter & Data Explorer")
    st.markdown(
        "🔍 Gunakan filter canggih untuk eksplorasi subset data dan analisis interaktif "
        "sesuai dengan kebutuhan Anda."
    )
    
    # Store original df for reset
    original_df = df.copy()
    
    # Initialize session state for filters
    if "filters" not in st.session_state:
        st.session_state.filters = {}
    
    st.markdown("---")
    st.markdown("## 🎯 Filter Controls")
    
    # Create expandable filter section
    with st.expander("📋 Filter Options", expanded=True):
        col1, col2 = st.columns(2)
        
        # Categorical filters
        with col1:
            st.markdown("### Categorical Filters")
            
            # Jurusan filter
            if "Jurusan" in df.columns:
                jurusan_list = sorted(df["Jurusan"].dropna().unique())
                selected_jurusan = st.multiselect(
                    "🎓 Jurusan (Major)",
                    options=jurusan_list,
                    default=st.session_state.filters.get("Jurusan", []),
                    key="filter_jurusan"
                )
                st.session_state.filters["Jurusan"] = selected_jurusan
            else:
                selected_jurusan = []
            
            # Bidang Minat filter
            if "Bidang Minat" in df.columns:
                bidang_list = sorted(df["Bidang Minat"].dropna().unique())
                selected_bidang = st.multiselect(
                    "💡 Bidang Minat (Interest Field)",
                    options=bidang_list,
                    default=st.session_state.filters.get("Bidang Minat", []),
                    key="filter_bidang"
                )
                st.session_state.filters["Bidang Minat"] = selected_bidang
            else:
                selected_bidang = []
            
            # Gaya Kerja filter
            if "Gaya Kerja" in df.columns:
                gaya_list = sorted(df["Gaya Kerja"].dropna().unique())
                selected_gaya = st.multiselect(
                    "🎪 Gaya Kerja (Work Style)",
                    options=gaya_list,
                    default=st.session_state.filters.get("Gaya Kerja", []),
                    key="filter_gaya"
                )
                st.session_state.filters["Gaya Kerja"] = selected_gaya
            else:
                selected_gaya = []
        
        with col2:
            st.markdown("### More Filters")
            
            # Tujuan Karier filter
            if "Tujuan Karier" in df.columns:
                tujuan_list = sorted(df["Tujuan Karier"].dropna().unique())
                selected_tujuan = st.multiselect(
                    "🎯 Tujuan Karier (Career Goal)",
                    options=tujuan_list,
                    default=st.session_state.filters.get("Tujuan Karier", []),
                    key="filter_tujuan"
                )
                st.session_state.filters["Tujuan Karier"] = selected_tujuan
            else:
                selected_tujuan = []
            
            # Rekomendasi Karier filter
            if "Rekomendasi Karier" in df.columns:
                rekomendasi_list = sorted(df["Rekomendasi Karier"].dropna().unique())
                selected_rekomendasi = st.multiselect(
                    "💼 Rekomendasi Karier (Career Recommendation)",
                    options=rekomendasi_list,
                    default=st.session_state.filters.get("Rekomendasi Karier", []),
                    key="filter_rekomendasi"
                )
                st.session_state.filters["Rekomendasi Karier"] = selected_rekomendasi
            else:
                selected_rekomendasi = []
            
            # Preferensi Industri filter
            if "Preferensi Industri" in df.columns:
                industri_list = sorted(df["Preferensi Industri"].dropna().unique())
                selected_industri = st.multiselect(
                    "🏢 Preferensi Industri (Industry Preference)",
                    options=industri_list,
                    default=st.session_state.filters.get("Preferensi Industri", []),
                    key="filter_industri"
                )
                st.session_state.filters["Preferensi Industri"] = selected_industri
            else:
                selected_industri = []
    
    # Numeric range filters
    with st.expander("📊 Numeric Range Filters", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        # IPK range
        with col1:
            if "IPK" in df.columns:
                ipk_min, ipk_max = st.slider(
                    "📚 IPK Range",
                    min_value=float(df["IPK"].min()),
                    max_value=float(df["IPK"].max()),
                    value=(float(df["IPK"].min()), float(df["IPK"].max())),
                    step=0.01,
                    key="filter_ipk"
                )
                st.session_state.filters["IPK"] = (ipk_min, ipk_max)
            else:
                ipk_min = ipk_max = None
        
        # Sertifikasi range
        with col2:
            if "Jumlah Sertifikasi" in df.columns:
                cert_min, cert_max = st.slider(
                    "🏅 Certifications Range",
                    min_value=float(df["Jumlah Sertifikasi"].min()),
                    max_value=float(df["Jumlah Sertifikasi"].max()),
                    value=(float(df["Jumlah Sertifikasi"].min()), float(df["Jumlah Sertifikasi"].max())),
                    step=1.0,
                    key="filter_cert"
                )
                st.session_state.filters["Jumlah Sertifikasi"] = (cert_min, cert_max)
        
        # Pengalaman Magang filter (if numeric)
        with col3:
            if "Pengalaman Magang" in df.columns:
                st.write("Filter Pengalaman Magang tersedia di Filter Categorical")
    
 # Global search
    search_text = ""

    with st.expander("🔍 Global Search", expanded=False):
        search_text = st.text_input(
            "🔍 Search across all columns",
            placeholder="Enter keyword to search...",
            key="filter_search"
        )
    
    st.markdown("---")
    st.markdown("## 📈 Filter Results")

    # Apply filters
    filtered_df = original_df.copy()
    
    # Apply categorical filters
    if selected_jurusan:
        filtered_df = filtered_df[filtered_df["Jurusan"].isin(selected_jurusan)]
    if selected_bidang:
        filtered_df = filtered_df[filtered_df["Bidang Minat"].isin(selected_bidang)]
    if selected_gaya:
        filtered_df = filtered_df[filtered_df["Gaya Kerja"].isin(selected_gaya)]
    if selected_tujuan:
        filtered_df = filtered_df[filtered_df["Tujuan Karier"].isin(selected_tujuan)]
    if selected_rekomendasi:
        filtered_df = filtered_df[filtered_df["Rekomendasi Karier"].isin(selected_rekomendasi)]
    if selected_industri:
        filtered_df = filtered_df[filtered_df["Preferensi Industri"].isin(selected_industri)]
    
    # Apply numeric filters
    if ipk_min is not None and ipk_max is not None:
        filtered_df = filtered_df[
            (filtered_df["IPK"] >= ipk_min)
            & (filtered_df["IPK"] <= ipk_max)
        ]
    
    if "cert_min" in locals() and "cert_max" in locals():
        filtered_df = filtered_df[
            (filtered_df["Jumlah Sertifikasi"] >= cert_min) & 
            (filtered_df["Jumlah Sertifikasi"] <= cert_max)
        ]
    
    # Apply global search
    if search_text:
        mask = filtered_df.apply(
            lambda row: row.astype(str).str.contains(search_text, case=False, na=False).any(),
            axis=1,
        )
        filtered_df = filtered_df[mask]
    
    # Display statistics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📊 Original Rows", format_int(len(original_df)))
    
    with col2:
        st.metric("🔍 Filtered Rows", format_int(len(filtered_df)))
    
    with col3:
        percentage = (len(filtered_df) / len(original_df) * 100) if len(original_df) > 0 else 0
        st.metric("📈 % of Data", f"{percentage:.1f}%")
    
    with col4:
        st.metric("📁 Columns", format_int(len(filtered_df.columns)))
    
    with col5:
        if "Rekomendasi Karier" in filtered_df.columns:
            unique_careers = filtered_df["Rekomendasi Karier"].nunique()
            st.metric("💼 Unique Careers", format_int(unique_careers))
    
    st.markdown("---")
    st.markdown("## 📋 Data Display")
    
  # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Data Table",
        "📈 Quick Stats",
        "📉 Visualizations",
        "💾 Export Data"
    ])
    
    with tab1:
        st.markdown("### Filtered Dataset")
        
        # Pagination controls
        col1, col2, col3 = st.columns([2, 1, 1])
        
        if len(filtered_df) > 0:
            with col1:
                view_rows = st.slider(
                    "Rows to display",
                    min_value=5,
                    max_value=max(5, min(100, len(filtered_df))),
                    value=min(20, max(5, len(filtered_df)))
                )
            
            with col2:
                view_type = st.radio("View", ["First", "Last", "Sample"], horizontal=True)
                
        else:
            view_rows = 5
            st.warning("Tidak ada data yang sesuai filter.")
            
        # Display data
        if view_type == "First":
            st.dataframe(filtered_df.head(view_rows), use_container_width=True, height=400)
        elif view_type == "Last":
            st.dataframe(filtered_df.tail(view_rows), use_container_width=True, height=400)
        else:
            st.dataframe(
                filtered_df.sample(
                    n=min(view_rows, len(filtered_df)),
                    random_state=42
                ),
                use_container_width=True,
                height=400
            
)
    
    with tab2:
        st.markdown("### Filter Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Numeric Summary")
            numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                st.dataframe(filtered_df[numeric_cols].describe().round(2), use_container_width=True)
            else:
                st.info("No numeric columns to display")
        
        with col2:
            st.markdown("#### Categorical Summary")
            categorical_cols = filtered_df.select_dtypes(include=['object']).columns.tolist()
            if categorical_cols:
                selected_cat_col = st.selectbox("Select Categorical Column", categorical_cols)
                value_counts = filtered_df[selected_cat_col].value_counts()
                st.dataframe(
                    value_counts.reset_index().rename(columns={
                        selected_cat_col: "Value", "count": "Count"
                    }),
                    use_container_width=True
                )
    
    with tab3:
        st.markdown("### Filtered Data Visualizations")
        
        # IPK distribution
        if "IPK" in filtered_df.columns and len(filtered_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.histogram(
                    filtered_df,
                    x="IPK",
                    nbins=20,
                    title="IPK Distribution (Filtered)",
                    template=template,
                    marginal="box"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if "Rekomendasi Karier" in filtered_df.columns:
                    fig = px.box(
                        filtered_df,
                        x="Rekomendasi Karier",
                        y="IPK",
                        title="IPK by Career (Filtered)",
                        template=template,
                        color="Rekomendasi Karier"
                    )
                    fig.update_layout(xaxis_tickangle=-45, height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
        
        # Career recommendation distribution
        if "Rekomendasi Karier" in filtered_df.columns and len(filtered_df) > 0:
            career_counts = filtered_df["Rekomendasi Karier"].value_counts().head(10)
            
            fig = px.bar(
                x=career_counts.values,
                y=career_counts.index,
                orientation="h",
                title="Top 10 Career Recommendations (Filtered)",
                template=template,
                labels={"x": "Count", "y": "Career"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 💾 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = export_data_to_csv(filtered_df)
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name="filtered_career_data.csv",
                mime="text/csv"
            )
        
        with col2:
            json_data = filtered_df.to_json(orient='records')
            st.download_button(
                label="📄 Download as JSON",
                data=json_data,
                file_name="filtered_career_data.json",
                mime="application/json"
            )
        
        with col3:
            st.write("**Export Summary:**")
            st.metric("Records to Export", format_int(len(filtered_df)))
        
        st.markdown("---")
        st.markdown("### Custom Export")
        
        # Select columns to export
        export_cols = st.multiselect(
            "🔍 Select columns to export",
            filtered_df.columns.tolist(),
            default=filtered_df.columns.tolist()
        )
        
        if export_cols:
            export_df = filtered_df[export_cols]
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = export_data_to_csv(export_df)
                st.download_button(
                    label="✅ Download Selected Columns (CSV)",
                    data=csv_data,
                    file_name="filtered_custom_export.csv",
                    mime="text/csv",
                    key="custom_export"
                )
            
            with col2:
                st.write(f"**Columns:** {len(export_cols)}")
                st.write(f"**Rows:** {len(export_df)}")
    
    st.markdown("---")
    st.markdown("## 🔄 Filter Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Reset All Filters"):
            st.session_state.filters = {}
            st.rerun()
    
    with col2:
        if st.button("💾 Save Current Filter"):
            st.success("Filter configuration saved to session!")
    
    with col3:
        active_filters = sum([
            bool(selected_jurusan), bool(selected_bidang), bool(selected_gaya),
            bool(selected_tujuan), bool(selected_rekomendasi), bool(selected_industri),
            search_text != ""
        ])
        st.metric("Active Filters", active_filters)
