import streamlit as st
from pages.home import render_home
from pages.data_overview import render_data_overview
from pages.eda import render_eda
from pages.career_insights import render_career_insights
from pages.filter_page import render_filters
from pages.executive_summary import render_executive_summary
from pages.career_predictor import render_career_predictor
from utils import load_data, get_plotly_template

# Page configuration
st.set_page_config(
    page_title="AI Career Recommendation Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling
st.markdown("""
    <style>
    /* Global styling */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
    }
    
    /* Font and typography */
    html, body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Hide default header and footer */
    .stAppHeader {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main content styling */
    .main {
        padding: 2rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
        text-align: center;
    }
    
    .metric-card h4 {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0 0 0;
    }
    
    /* Section titles */
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #1f2937;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    .subsection-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        color: #374151;
    }
    
    /* Data display */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #f3f4f6;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        border-radius: 8px 8px 0 0;
    }
    
    /* Cards with border */
    .insight-card {
        background: #f9fafb;
        border-left: 4px solid #667eea;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #d1fae5;
        border: 1px solid #10b981;
        border-radius: 8px;
    }
    
    /* Warning messages */
    .stWarning {
        background-color: #fef3c7;
        border: 1px solid #f59e0b;
        border-radius: 8px;
    }
    
    /* Info messages */
    .stInfo {
        background-color: #dbeafe;
        border: 1px solid #3b82f6;
        border-radius: 8px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .hero-section h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 800;
    }
    
    .hero-section p {
        font-size: 1.1rem;
        opacity: 0.95;
        line-height: 1.6;
    }
    
    /* Loading animation */
    .spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-section h1 {
            font-size: 1.8rem;
        }
        
        .section-title {
            font-size: 1.4rem;
        }
        
        .metric-card .value {
            font-size: 1.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Load data
DATA_PATH = "New_Career_Recommendation_Cleaned.csv"

# Fungsi inisialisasi yang diperbaiki tanpa menggunakan @st.cache_resource secara salah
def init_session_state():
    """Initialize session state variables."""
    if "df" not in st.session_state:
        st.session_state.df = load_data(DATA_PATH)
    if "template" not in st.session_state:
        st.session_state.template = get_plotly_template()

# Jalankan inisialisasi state terlebih dahulu sebelum variabel ditarik
init_session_state()

df = st.session_state.df
plotly_template = st.session_state.template

# Sidebar configuration
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🎓</div>
        <h1 style='margin: 0; font-size: 1.5rem;'>Career Dashboard</h1>
        <p style='margin: 0.5rem 0; color: #6b7280; font-size: 0.9rem;'>
            AI-Powered Career Recommendation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    **📊 Dashboard Overview**
    
    Platform analitik komprehensif untuk rekomendasi karier berbasis AI, dirancang untuk mahasiswa dan profesional muda.
    
    **📈 Dataset Info**
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Records", f"{len(df):,}")
    with col2:
        st.metric("Features", len(df.columns))
    
    st.markdown("---")
    
    # Page navigation with improved styling
    st.markdown("**🗂️ Navigasi**")
    
    page_names = [
        "🏠 Home",
        "📋 Executive Summary",
        "📊 Data Overview",
        "📈 Exploratory Analysis",
        "💼 Career Insights",
        "🧩 Filter Data",
        "🤖 Career Predictor",
    ]
    
    page = st.radio("Pilih Halaman", page_names, index=0)
    
    st.markdown("---")
    st.markdown("""
    **ℹ️ Informasi**
    
    Dataset: New_Career_Recommendation_Cleaned  
    Ukuran: 49,500 Records × 20 Features  
    Pamaruan: 2026  
    
    **Developer:** Data Science Team
    """)

# Route to appropriate page
if page == "🏠 Home":
    render_home(df, plotly_template)
elif page == "📋 Executive Summary":
    render_executive_summary(df, plotly_template)
elif page == "📊 Data Overview":
    render_data_overview(df, plotly_template)
elif page == "📈 Exploratory Analysis":
    render_eda(df, plotly_template)
elif page == "💼 Career Insights":
    render_career_insights(df, plotly_template)
elif page == "🧩 Filter Data":
    render_filters(df, plotly_template)
elif page == "🤖 Career Predictor":
    render_career_predictor(df, plotly_template)