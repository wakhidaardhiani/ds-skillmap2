import pandas as pd
import streamlit as st
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple, Any
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

CACHE_KEY = "career_recommendation_data"


@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """Load CSV data with validation and column cleaning."""
    try:
        dataset_path = Path(file_path)
        if not dataset_path.exists():
            dataset_path = Path(__file__).parent / file_path
        
        if not dataset_path.exists():
            st.error(f"❌ File tidak ditemukan: {file_path}")
            return pd.DataFrame()
        
        df = pd.read_csv(dataset_path)
        
        # Clean column names: strip whitespace and convert underscore to space
        df.columns = df.columns.str.strip().str.replace('_', ' ')
        
        return df
    except Exception as e:
        st.error(f"❌ Error memuat data: {str(e)}")
        return pd.DataFrame()


def get_theme_mode() -> str:
    """Get current Streamlit theme mode."""
    try:
        theme_base = st.get_option("theme.base")
        return theme_base if theme_base else "light"
    except Exception:
        return "light"


def get_plotly_template() -> str:
    """Get appropriate Plotly template based on theme."""
    theme = get_theme_mode()
    return "plotly_dark" if theme == "dark" else "plotly"


def format_int(value: int) -> str:
    """Format integer with thousand separators."""
    return f"{value:,}" if value is not None else "0"


def format_float(value: float, decimals: int = 2) -> str:
    """Format float with specific decimals."""
    return f"{value:.{decimals}f}" if value is not None else "0.00"


def create_metric_card(title: str, value: str, icon: str = "📊") -> str:
    """Create HTML metric card."""
    return f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px; border-radius: 10px; text-align: center;
                color: white; margin: 10px 0;">
        <div style="font-size: 24px; margin-bottom: 10px;">{icon}</div>
        <div style="font-size: 14px; opacity: 0.9;">{title}</div>
        <div style="font-size: 28px; font-weight: bold; margin-top: 5px;">{value}</div>
    </div>
    """


def get_data_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """Get comprehensive data statistics."""
    stats = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
        "missing_values": df.isnull().sum().sum(),
        "duplicates": df.duplicated().sum(),
        "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
        "categorical_columns": df.select_dtypes(include=['object']).columns.tolist(),
    }
    return stats


def get_categorical_stats(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Get statistics for categorical column."""
    stats = df[col].value_counts().reset_index()
    stats.columns = [col, 'Count']
    stats['Percentage'] = (stats['Count'] / stats['Count'].sum() * 100).round(2)
    return stats


def create_bar_chart(df: pd.DataFrame, x: str, y: str, title: str, 
                     template: str, color: str = None, show_value: bool = True) -> go.Figure:
    """Create optimized bar chart."""
    fig = px.bar(
        df, 
        x=x, 
        y=y, 
        title=title,
        template=template,
        color=color if color else y,
        text=y if show_value else None,
        labels={x: x.replace('_', ' '), y: y.replace('_', ' ')}
    )
    fig.update_layout(
        height=400,
        showlegend=False,
        hovermode='x unified',
        margin=dict(l=50, r=50, t=60, b=50)
    )
    if show_value:
        fig.update_traces(textposition='auto', texttemplate='%{text:.0f}')
    return fig


def create_histogram(df: pd.DataFrame, column: str, title: str, 
                     template: str, nbins: int = 30) -> go.Figure:
    """Create optimized histogram."""
    fig = px.histogram(
        df,
        x=column,
        title=title,
        template=template,
        nbins=nbins,
        marginal="box",
        labels={column: column.replace('_', ' ')}
    )
    fig.update_layout(
        height=400,
        showlegend=False,
        hovermode='x unified',
        margin=dict(l=50, r=50, t=60, b=50)
    )
    return fig


def create_pie_chart(df: pd.DataFrame, column: str, title: str, template: str) -> go.Figure:
    """Create optimized pie chart."""
    value_counts = df[column].value_counts().reset_index()
    value_counts.columns = [column, 'count']
    
    fig = px.pie(
        value_counts,
        names=column,
        values='count',
        title=title,
        template=template,
        labels={column: column.replace('_', ' ')}
    )
    fig.update_layout(height=400, margin=dict(l=50, r=50, t=60, b=50))
    return fig


def create_box_plot(df: pd.DataFrame, y: str, x: str = None, title: str = None,
                   template: str = None) -> go.Figure:
    """Create optimized box plot."""
    title = title or f"Box Plot: {y.replace('_', ' ')}"
    fig = px.box(
        df,
        y=y,
        x=x,
        title=title,
        template=template,
        labels={y: y.replace('_', ' '), x: x.replace('_', ' ') if x else ''}
    )
    fig.update_layout(height=400, margin=dict(l=50, r=50, t=60, b=50))
    return fig


def create_scatter_plot(df: pd.DataFrame, x: str, y: str, color: str = None,
                       title: str = None, template: str = None) -> go.Figure:
    """Create optimized scatter plot."""
    title = title or f"{x.replace('_', ' ')} vs {y.replace('_', ' ')}"
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        template=template,
        labels={x: x.replace('_', ' '), y: y.replace('_', ' '), color: color.replace('_', ' ') if color else ''}
    )
    fig.update_layout(height=400, margin=dict(l=50, r=50, t=60, b=50), hovermode='closest')
    return fig


def get_top_categories(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
    """Get top N categories."""
    return df[column].value_counts().head(n).reset_index()


def calculate_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate correlation matrix for numeric columns."""
    numeric_df = df.select_dtypes(include=[np.number])
    return numeric_df.corr()


def create_correlation_heatmap(df: pd.DataFrame, template: str) -> go.Figure:
    """Create correlation heatmap."""
    corr_matrix = calculate_correlation(df)
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        hovertemplate='%{x} vs %{y}: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Correlation Matrix - Numeric Features",
        height=600,
        template=template,
        margin=dict(l=100, r=100, t=60, b=100)
    )
    return fig


def get_data_insights(df: pd.DataFrame) -> Dict[str, str]:
    """Generate automatic insights from data."""
    insights = {}
    
    # Most common major
    if 'Jurusan' in df.columns:
        top_major = df['Jurusan'].value_counts().index[0]
        insights['major'] = f"Jurusan paling banyak: **{top_major}**"
    
    # Most recommended career
    if 'Rekomendasi Karier' in df.columns:
        top_career = df['Rekomendasi Karier'].value_counts().index[0]
        count = df['Rekomendasi Karier'].value_counts().iloc[0]
        insights['career'] = f"Karier paling direkomendasikan: **{top_career}** ({count} kali)"
    
    # Most popular interest
    if 'Bidang Minat' in df.columns:
        top_interest = df['Bidang Minat'].value_counts().index[0]
        insights['interest'] = f"Bidang minat paling populer: **{top_interest}**"
    
    # Average GPA
    if 'IPK' in df.columns:
        avg_gpa = df['IPK'].mean()
        insights['gpa'] = f"Rata-rata IPK: **{avg_gpa:.2f}**"
    
    # Average certifications
    if 'Jumlah Sertifikasi' in df.columns:
        avg_cert = df['Jumlah Sertifikasi'].mean()
        insights['cert'] = f"Rata-rata Sertifikasi: **{avg_cert:.2f}**"
    
    return insights


def export_data_to_csv(df: pd.DataFrame, filename: str = "data_export.csv") -> bytes:
    """Export dataframe to CSV bytes."""
    return df.to_csv(index=False).encode('utf-8')


def filter_dataframe(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """Apply filters to dataframe."""
    result_df = df.copy()
    
    for col, value in filters.items():
        if col not in df.columns or value is None:
            continue
        
        if isinstance(value, list) and len(value) > 0:
            result_df = result_df[result_df[col].isin(value)]
        elif isinstance(value, tuple):  # Range filter
            result_df = result_df[(result_df[col] >= value[0]) & (result_df[col] <= value[1])]
    
    return result_df


def encode_categorical(df: pd.DataFrame, columns: List[str]) -> Tuple[pd.DataFrame, Dict[str, LabelEncoder]]:
    """Encode categorical columns for ML."""
    df_encoded = df.copy()
    encoders = {}
    
    for col in columns:
        if col in df_encoded.columns:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            encoders[col] = le
    
    return df_encoded, encoders


def get_feature_importance(model: RandomForestClassifier, feature_names: List[str], 
                          top_n: int = 10) -> pd.DataFrame:
    """Get feature importance from model."""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    
    importance_df = pd.DataFrame({
        'Feature': [feature_names[i] for i in indices],
        'Importance': importances[indices]
    })
    
    return importance_df.reset_index(drop=True)


def create_download_button_html(data: bytes, filename: str, label: str) -> str:
    """Create download button as HTML."""
    # Streamlit's download_button is better, so this is for reference only
    pass
