import streamlit as st
import pandas as pd
import numpy as np
from utils import get_data_statistics, get_categorical_stats, export_data_to_csv

def render_data_overview(df: pd.DataFrame, template: str) -> None:
    """Render comprehensive data overview page."""
    
    st.markdown("# 📊 Data Overview")
    st.markdown(
        "📖 Halaman ini menyediakan analisis lengkap struktur dataset, "
        "tipe data, missing values, dan eksplorasi statistik interaktif."
    )
    
    # Get statistics
    stats = get_data_statistics(df)
    
    st.markdown("---")
    st.markdown("## 📋 Dataset Statistics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Total Rows", f"{stats['total_rows']:,}")
    with col2:
        st.metric("📁 Total Columns", f"{stats['total_columns']}")
    with col3:
        st.metric("💾 Memory Usage", stats['memory_usage'])
    with col4:
        missing_percent = (stats['missing_values'] / (stats['total_rows'] * stats['total_columns']) * 100)
        st.metric("❌ Missing Values", f"{missing_percent:.2f}%")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔄 Duplicate Records", f"{stats['duplicates']:,}")
    with col2:
        completeness = ((stats['total_rows'] * stats['total_columns'] - stats['missing_values']) / 
                       (stats['total_rows'] * stats['total_columns']) * 100)
        st.metric("✅ Data Completeness", f"{completeness:.2f}%")
    
    st.markdown("---")
    
    # Data type breakdown
    st.markdown("## 🔤 Data Type Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Numeric Columns")
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            for col in numeric_cols:
                st.write(f"- `{col}`")
        else:
            st.info("No numeric columns found")
    
    with col2:
        st.markdown("### Categorical Columns")
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        if categorical_cols:
            for col in categorical_cols:
                st.write(f"- `{col}`")
        else:
            st.info("No categorical columns found")
    
    # Detailed type information
    st.markdown("---")
    st.markdown("## 📝 Column Information")
    
    # Create detailed column info table
    col_info = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.astype(str),
        'Non-Null Count': df.count().values,
        'Missing': df.isnull().sum().values,
        'Missing %': (df.isnull().sum().values / len(df) * 100).round(2),
        'Unique': [df[col].nunique() for col in df.columns]
    })
    
    st.dataframe(col_info, use_container_width=True, height=400)
    
    st.markdown("---")
    st.markdown("## 📊 Statistical Summary")
    
    # Numeric statistics
    st.markdown("### Numeric Features - Descriptive Statistics")
    numeric_stats = df.describe().T
    numeric_stats.columns = ['Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max']
    st.dataframe(numeric_stats, use_container_width=True)
    
    # Categorical statistics
    st.markdown("### Categorical Features - Value Counts")
    
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if categorical_cols:
        selected_col = st.selectbox(
            "🔍 Select Column to Analyze",
            categorical_cols,
            key="cat_analysis"
        )
        
        if selected_col:
            stats_df = get_categorical_stats(df, selected_col)
            st.dataframe(stats_df, use_container_width=True)
            
            # Display distribution
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**Top 10 Values in {selected_col}:**")
                top_10 = df[selected_col].value_counts().head(10)
                st.bar_chart(top_10)
            with col2:
                st.write(f"**Summary for {selected_col}:**")
                st.metric("Unique Values", df[selected_col].nunique())
                st.metric("Missing Values", df[selected_col].isnull().sum())
                st.metric("Most Common", df[selected_col].value_counts().index[0])
    
    st.markdown("---")
    st.markdown("## ❌ Missing Values Analysis")
    
    missing_summary = pd.DataFrame({
        'Column': df.columns,
        'Missing Count': df.isnull().sum().values,
        'Missing %': (df.isnull().sum().values / len(df) * 100).round(2)
    }).sort_values('Missing Count', ascending=False)
    
    missing_with_data = missing_summary[missing_summary['Missing Count'] > 0]
    
    if len(missing_with_data) > 0:
        st.warning(f"⚠️ {len(missing_with_data)} columns dengan missing values")
        st.dataframe(missing_with_data, use_container_width=True)
    else:
        st.success("✅ No missing values found in dataset!")
    
    st.markdown("---")
    st.markdown("## 🔍 Advanced Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Data Preview", "Column Search", "Data Export"])
    
    with tab1:
        st.markdown("### Interactive Data Preview")
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write("**Browse dataset:**")
        with col2:
            rows = st.number_input("Rows to show", 5, 100, 10)
        with col3:
            view_type = st.radio("View", ["Head", "Tail", "Sample"], horizontal=True)
        
        if view_type == "Head":
            st.dataframe(df.head(rows), use_container_width=True)
        elif view_type == "Tail":
            st.dataframe(df.tail(rows), use_container_width=True)
        else:
            st.dataframe(df.sample(min(rows, len(df))), use_container_width=True)
    
    with tab2:
        st.markdown("### Column Search & Filter")
        search_term = st.text_input("🔍 Search column name...")
        
        if search_term:
            matching_cols = [col for col in df.columns if search_term.lower() in col.lower()]
            
            if matching_cols:
                st.success(f"Found {len(matching_cols)} matching columns:")
                for col in matching_cols:
                    with st.expander(f"📊 {col}"):
                        st.write(f"**Type:** {df[col].dtype}")
                        st.write(f"**Non-null Count:** {df[col].count()}")
                        st.write(f"**Unique Values:** {df[col].nunique()}")
                        
                        if df[col].dtype == 'object':
                            st.write("**Value Counts:**")
                            st.bar_chart(df[col].value_counts().head(10))
                        else:
                            st.write("**Statistics:**")
                            st.write(df[col].describe())
            else:
                st.warning(f"No columns found matching '{search_term}'")
    
    with tab3:
        st.markdown("### Export Dataset")
        st.write("Download the dataset in different formats:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = export_data_to_csv(df)
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name="career_data_export.csv",
                mime="text/csv"
            )
        
        with col2:
            excel_data = df.to_excel(None, index=False)
            st.download_button(
                label="📊 Download as Excel",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name="career_data_export.xlsx",
                mime="application/vnd.ms-excel"
            )
        
        with col3:
            json_data = df.to_json(orient='records')
            st.download_button(
                label="📄 Download as JSON",
                data=json_data,
                file_name="career_data_export.json",
                mime="application/json"
            )
        
        st.info("💡 Select rows to export:")
        
        n_rows = st.slider("Number of rows to export", 1, len(df), min(1000, len(df)))
        subset_df = df.head(n_rows)
        
        st.write(f"Ready to export {len(subset_df)} rows")
        
        col1, col2 = st.columns(2)
        with col1:
            csv_subset = export_data_to_csv(subset_df)
            st.download_button(
                label="✅ Download Selected Rows (CSV)",
                data=csv_subset,
                file_name=f"career_data_{n_rows}_rows.csv",
                mime="text/csv"
            )
