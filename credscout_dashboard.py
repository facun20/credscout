import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from collections import Counter
import numpy as np
import re

# Page config
st.set_page_config(
    page_title="CredScout Intelligence Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        background-color: #f7f8fa;
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    .credscout-header {
        background: white;
        padding: 1.75rem 2.5rem;
        margin: -2rem -2rem 2.5rem -2rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .credscout-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827;
        letter-spacing: -0.02em;
    }
    
    .credscout-logo-accent {
        color: #3b82f6;
    }
    
    .credscout-tagline {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 400;
        margin-top: 0.25rem;
    }
    
    .search-box {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 2rem;
    }
    
    .search-result-badge {
        display: inline-block;
        background: #eff6ff;
        color: #1e40af;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.875rem;
        font-weight: 500;
        margin-right: 0.5rem;
        border: 1px solid #bfdbfe;
    }
    
    .metric-card {
        background: white;
        padding: 1.75rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        height: 100%;
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        border-color: #cbd5e1;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 500;
        margin-bottom: 0.75rem;
        letter-spacing: -0.01em;
    }
    
    .metric-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: #111827;
        line-height: 1;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .metric-delta {
        font-size: 0.8125rem;
        color: #6b7280;
        font-weight: 400;
    }
    
    .section-subheader {
        font-size: 0.9375rem;
        font-weight: 600;
        color: #374151;
        margin: 1.5rem 0 1rem 0;
        letter-spacing: -0.01em;
    }
    
    .insight-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .insight-card:hover {
        border-color: #cbd5e1;
    }
    
    .badge-note {
        display: inline-block;
        background: #f3f4f6;
        color: #6b7280;
        font-size: 0.75rem;
        font-weight: 500;
        padding: 0.25rem 0.625rem;
        border-radius: 6px;
        margin-left: 0.5rem;
        letter-spacing: -0.01em;
    }
    
    .stSelectbox label, .stSlider label, .stTextInput label, .stMultiSelect label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
        letter-spacing: -0.01em;
    }
    
    .stButton>button:hover {
        background-color: #2563eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stDownloadButton>button {
        background-color: white;
        color: #374151;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
    }
    
    .stDownloadButton>button:hover {
        border-color: #9ca3af;
        background-color: #f9fafb;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: white;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        padding: 0.25rem;
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem;
        color: #6b7280;
        border-radius: 8px;
        background: transparent;
        letter-spacing: -0.01em;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #111827;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    .dataframe {
        font-size: 0.875rem;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px;
    }
    
    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e5e7eb;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .info-box {
        background: #eff6ff;
        border-left: 3px solid #3b82f6;
        padding: 1rem;
        border-radius: 6px;
        font-size: 0.875rem;
        color: #1e40af;
        margin: 1rem 0;
    }
    
    .quick-search-tags {
        margin-top: 1rem;
    }
    
    .quick-tag {
        display: inline-block;
        background: white;
        border: 1px solid #d1d5db;
        color: #374151;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.8125rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .quick-tag:hover {
        background: #f3f4f6;
        border-color: #9ca3af;
    }
</style>
""", unsafe_allow_html=True)

# Load data function
def clean_price(price_str):
    """Extract numeric price from various formats"""
    if pd.isna(price_str) or price_str == 'Unknown':
        return None
    clean = str(price_str).replace('$', '').replace(',', '').replace(' ', '').replace('CAD', '').replace('cad', '')
    try:
        return float(clean)
    except:
        return None

def clean_duration(duration_str):
    """Convert duration to weeks"""
    if pd.isna(duration_str) or duration_str == 'Unknown':
        return None
    duration_str = str(duration_str).lower()
    numbers = re.findall(r'\d+\.?\d*', duration_str)
    if not numbers:
        return None
    num = float(numbers[0])
    if 'month' in duration_str:
        return num * 4
    elif 'week' in duration_str:
        return num
    elif 'day' in duration_str:
        return num / 7
    elif 'hour' in duration_str:
        return num / 40
    elif 'year' in duration_str:
        return num * 52
    return None

def categorize_offering_level(row):
    """Categorize offering into levels"""
    cred_type = str(row.get('credential_type', '')).lower()
    price = row.get('price_cad')
    duration = row.get('duration_weeks')
    if (price and price < 500) or (duration and duration < 2):
        return 'micro_learning'
    if (price and price > 5000) or (duration and duration > 24):
        return 'diploma'
    if 'course' in cred_type and price and price < 1000:
        return 'course'
    if 'certificate' in cred_type or 'credential' in cred_type:
        if price and price > 2000:
            return 'certificate_advanced'
        return 'certificate'
    if 'professional' in cred_type or 'statement' in cred_type:
        return 'professional_development'
    return 'certificate'

@st.cache_data
def load_data(uploaded_file):
    """Load and process CSV data - handles headerless raw data or preprocessed data"""
    
    # Try reading first - see if it has headers
    try:
        test_df = pd.read_csv(uploaded_file, nrows=1)
        uploaded_file.seek(0)  # Reset file pointer
        
        # Check if first row looks like data or headers
        if 'program_id' in test_df.columns or 'offering_level' in test_df.columns:
            # Preprocessed data with headers
            df = pd.read_csv(uploaded_file)
            df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
            return df
    except:
        pass
    
    uploaded_file.seek(0)  # Reset file pointer
    
    # Assume headerless raw format
    df = pd.read_csv(
        uploaded_file,
        header=None,
        names=[
            'institution', 'program_name', 'credential_type', 'delivery_mode',
            'duration', 'skills', 'price', 'description', 'url', 'scraped_date'
        ]
    )
    
    # Rename to expected format
    df['title'] = df['program_name']
    df['program_url'] = df['url']
    df['program_id'] = range(1, len(df) + 1)
    df['province'] = 'Unknown'
    
    # Clean prices
    df['price_cad'] = df['price'].apply(clean_price)
    df['price_display'] = df['price']
    
    # Clean durations
    df['duration_weeks'] = df['duration'].apply(clean_duration)
    df['duration_display'] = df['duration']
    
    # Categorize offering levels
    df['offering_level'] = df.apply(categorize_offering_level, axis=1)
    
    # Add data quality
    def assess_quality(row):
        unknown_count = sum([
            1 for col in ['credential_type', 'delivery_mode', 'duration', 'skills', 'price', 'description']
            if pd.isna(row.get(col)) or row.get(col) == 'Unknown' or row.get(col) == ''
        ])
        return 'poor' if unknown_count >= 4 else ('moderate' if unknown_count >= 2 else 'good')
    
    df['data_quality'] = df.apply(assess_quality, axis=1)
    df['date_added'] = pd.to_datetime(df['scraped_date'], errors='coerce')
    
    return df

def estimate_unique_programs(df):
    """Calculate Lightcast-style estimates"""
    total = len(df)
    course_count = len(df[df['offering_level'] == 'course'])
    
    # Assume 4 courses ≈ 1 certificate
    estimated_programs_from_courses = course_count / 4
    non_course_count = total - course_count
    estimated_unique = int(non_course_count + estimated_programs_from_courses)
    
    return {
        'total': total,
        'estimated_unique': estimated_unique,
        'course_count': course_count
    }

# Page config
st.set_page_config(
    page_title="CredScout Intelligence Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        background-color: #f7f8fa;
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    .credscout-header {
        background: white;
        padding: 1.75rem 2.5rem;
        margin: -2rem -2rem 2.5rem -2rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .credscout-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827;
        letter-spacing: -0.02em;
    }
    
    .credscout-logo-accent {
        color: #3b82f6;
    }
    
    .credscout-tagline {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 400;
        margin-top: 0.25rem;
    }
    
    .search-box {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 2rem;
    }
    
    .search-result-badge {
        display: inline-block;
        background: #eff6ff;
        color: #1e40af;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.875rem;
        font-weight: 500;
        margin-right: 0.5rem;
        border: 1px solid #bfdbfe;
    }
    
    .metric-card {
        background: white;
        padding: 1.75rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        height: 100%;
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        border-color: #cbd5e1;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 500;
        margin-bottom: 0.75rem;
        letter-spacing: -0.01em;
    }
    
    .metric-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: #111827;
        line-height: 1;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .metric-delta {
        font-size: 0.8125rem;
        color: #6b7280;
        font-weight: 400;
    }
    
    .section-subheader {
        font-size: 0.9375rem;
        font-weight: 600;
        color: #374151;
        margin: 1.5rem 0 1rem 0;
        letter-spacing: -0.01em;
    }
    
    .insight-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .insight-card:hover {
        border-color: #cbd5e1;
    }
    
    .badge-note {
        display: inline-block;
        background: #f3f4f6;
        color: #6b7280;
        font-size: 0.75rem;
        font-weight: 500;
        padding: 0.25rem 0.625rem;
        border-radius: 6px;
        margin-left: 0.5rem;
        letter-spacing: -0.01em;
    }
    
    .stSelectbox label, .stSlider label, .stTextInput label, .stMultiSelect label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
        letter-spacing: -0.01em;
    }
    
    .stButton>button:hover {
        background-color: #2563eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stDownloadButton>button {
        background-color: white;
        color: #374151;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
    }
    
    .stDownloadButton>button:hover {
        border-color: #9ca3af;
        background-color: #f9fafb;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: white;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        padding: 0.25rem;
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem;
        color: #6b7280;
        border-radius: 8px;
        background: transparent;
        letter-spacing: -0.01em;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #111827;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    .dataframe {
        font-size: 0.875rem;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px;
    }
    
    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e5e7eb;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .info-box {
        background: #eff6ff;
        border-left: 3px solid #3b82f6;
        padding: 1rem;
        border-radius: 6px;
        font-size: 0.875rem;
        color: #1e40af;
        margin: 1rem 0;
    }
    
    .quick-search-tags {
        margin-top: 1rem;
    }
    
    .quick-tag {
        display: inline-block;
        background: white;
        border: 1px solid #d1d5db;
        color: #374151;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.8125rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .quick-tag:hover {
        background: #f3f4f6;
        border-color: #9ca3af;
    }
</style>
""", unsafe_allow_html=True)

# Load data function
def clean_price(price_str):
    """Extract numeric price from various formats"""
    if pd.isna(price_str) or price_str == 'Unknown':
        return None
    clean = str(price_str).replace('$', '').replace(',', '').replace(' ', '').replace('CAD', '').replace('cad', '')
    try:
        return float(clean)
    except:
        return None

def clean_duration(duration_str):
    """Convert duration to weeks"""
    if pd.isna(duration_str) or duration_str == 'Unknown':
        return None
    duration_str = str(duration_str).lower()
    numbers = re.findall(r'\d+\.?\d*', duration_str)
    if not numbers:
        return None
    num = float(numbers[0])
    if 'month' in duration_str:
        return num * 4
    elif 'week' in duration_str:
        return num
    elif 'day' in duration_str:
        return num / 7
    elif 'hour' in duration_str:
        return num / 40
    elif 'year' in duration_str:
        return num * 52
    return None

def categorize_offering_level(row):
    """Categorize offering into levels"""
    cred_type = str(row.get('credential_type', '')).lower()
    price = row.get('price_cad')
    duration = row.get('duration_weeks')
    if (price and price < 500) or (duration and duration < 2):
        return 'micro_learning'
    if (price and price > 5000) or (duration and duration > 24):
        return 'diploma'
    if 'course' in cred_type and price and price < 1000:
        return 'course'
    if 'certificate' in cred_type or 'credential' in cred_type:
        if price and price > 2000:
            return 'certificate_advanced'
        return 'certificate'
    if 'professional' in cred_type or 'statement' in cred_type:
        return 'professional_development'
    return 'certificate'

@st.cache_data
def load_data(uploaded_file):
    """Load and process CSV data - handles headerless raw data or preprocessed data"""
    
    # Try reading first - see if it has headers
    try:
        test_df = pd.read_csv(uploaded_file, nrows=1)
        uploaded_file.seek(0)  # Reset file pointer
        
        # Check if first row looks like data or headers
        if 'program_id' in test_df.columns or 'offering_level' in test_df.columns:
            # Preprocessed data with headers
            df = pd.read_csv(uploaded_file)
            df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
            return df
    except:
        pass
    
    uploaded_file.seek(0)  # Reset file pointer
    
    # Assume headerless raw format
    df = pd.read_csv(
        uploaded_file,
        header=None,
        names=[
            'institution', 'program_name', 'credential_type', 'delivery_mode',
            'duration', 'skills', 'price', 'description', 'url', 'scraped_date'
        ]
    )
    
    # Rename to expected format
    df['title'] = df['program_name']
    df['program_url'] = df['url']
    df['program_id'] = range(1, len(df) + 1)
    df['province'] = 'Unknown'
    
    # Clean prices
    df['price_cad'] = df['price'].apply(clean_price)
    df['price_display'] = df['price']
    
    # Clean durations
    df['duration_weeks'] = df['duration'].apply(clean_duration)
    df['duration_display'] = df['duration']
    
    # Categorize offering levels
    df['offering_level'] = df.apply(categorize_offering_level, axis=1)
    
    # Add data quality
    def assess_quality(row):
        unknown_count = sum([
            1 for col in ['credential_type', 'delivery_mode', 'duration', 'skills', 'price', 'description']
            if pd.isna(row.get(col)) or row.get(col) == 'Unknown' or row.get(col) == ''
        ])
        return 'poor' if unknown_count >= 4 else ('moderate' if unknown_count >= 2 else 'good')
    
    df['data_quality'] = df.apply(assess_quality, axis=1)
    df['date_added'] = pd.to_datetime(df['scraped_date'], errors='coerce')
    
    return df

def extract_top_skills(df, top_n=50):
    """Extract top skills from the dataset"""
    all_skills = []
    for skills_str in df['skills'].dropna():
        if skills_str != 'Unknown':
            skills_list = [s.strip() for s in str(skills_str).split(',')]
            all_skills.extend(skills_list)
    
    if all_skills:
        skill_counts = Counter(all_skills)
        return [skill for skill, count in skill_counts.most_common(top_n)]
    return []

# Header
st.markdown("""
<div class="credscout-header">
    <div>
        <div class="credscout-logo"><span class="credscout-logo-accent">Cred</span>Scout Intelligence</div>
        <div class="credscout-tagline">The Intelligence Layer for Continuing Education</div>
    </div>
</div>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "Upload Processed Dataset",
    type=['csv'],
    help="Use the preprocessed CSV file from preprocess_cpe_data.py",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    # Load data
    df = load_data(uploaded_file)
    
    # Extract top skills for quick search
    top_skills = extract_top_skills(df, top_n=20)
    
    # PROMINENT SEARCH BOX (Main area, not sidebar)
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input(
            "🔍 Search the CPE Market",
            placeholder="Try: AI, Python, Leadership, Data Science, Project Management...",
            key="main_search",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("Clear Search", use_container_width=True):
            st.session_state.main_search = ""
            st.rerun()
    
    # Quick search tags
    if not search_term and len(top_skills) > 0:
        st.markdown('<div class="quick-search-tags" style="margin-top: 0.5rem;">', unsafe_allow_html=True)
        st.markdown('<div style="color: #6b7280; font-size: 0.8125rem; margin-bottom: 0.5rem;">Popular searches:</div>', unsafe_allow_html=True)
        
        # Create clickable tags (using columns for layout)
        tag_cols = st.columns(8)
        for idx, skill in enumerate(top_skills[:8]):
            with tag_cols[idx % 8]:
                if st.button(skill, key=f"tag_{idx}", use_container_width=True):
                    st.session_state.main_search = skill
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar filters (keep existing)
    st.sidebar.markdown("### Advanced Filters")
    st.sidebar.markdown("")
    
    # Offering Level filter
    offering_levels = ['All Levels'] + sorted(df['offering_level'].dropna().unique().tolist())
    selected_offering_level = st.sidebar.selectbox(
        "Offering Level",
        offering_levels,
        help="Categorized by duration and price signals"
    )
    
    # Credential Type filter
    credential_types = ['All Types'] + sorted(df['credential_type'].dropna().unique().tolist())
    selected_credential = st.sidebar.selectbox(
        "Credential Type",
        credential_types
    )
    
    # Institution filter
    institutions = ['All Institutions'] + sorted(df['institution'].dropna().unique().tolist())
    selected_institution = st.sidebar.selectbox(
        "Institution",
        institutions
    )
    
    # Delivery Mode filter
    delivery_modes = ['All Modes'] + sorted(df['delivery_mode'].dropna().unique().tolist())
    selected_delivery = st.sidebar.selectbox(
        "Delivery Mode",
        delivery_modes
    )
    
    # Data Quality filter
    quality_levels = ['All Quality Levels', 'Good', 'Moderate', 'Poor']
    selected_quality = st.sidebar.selectbox(
        "Data Quality",
        quality_levels,
        help="Filter by data completeness"
    )
    
    # Price range filter
    prices = df['price_cad'].dropna()
    if len(prices) > 0:
        min_price = int(prices.min())
        max_price = int(prices.max())
        price_range = st.sidebar.slider(
            "Price Range (CAD)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=100
        )
    else:
        price_range = (0, 10000)
    
    # Duration range filter
    durations = df['duration_weeks'].dropna()
    if len(durations) > 0:
        min_duration = int(durations.min())
        max_duration = int(durations.max())
        duration_range = st.sidebar.slider(
            "Duration (weeks)",
            min_value=min_duration,
            max_value=max_duration,
            value=(min_duration, max_duration)
        )
    else:
        duration_range = (0, 52)
    
    st.sidebar.markdown("")
    
    # Clear filters button
    if st.sidebar.button("Reset All Filters", use_container_width=True):
        st.rerun()
    
    # Apply filters
    filtered_df = df.copy()
    
    # Search filter (from main search box)
    if search_term:
        search_term_lower = search_term.lower()
        filtered_df = filtered_df[
            filtered_df['title'].str.lower().str.contains(search_term_lower, na=False) |
            filtered_df['institution'].str.lower().str.contains(search_term_lower, na=False) |
            filtered_df['skills'].str.lower().str.contains(search_term_lower, na=False) |
            filtered_df['description'].str.lower().str.contains(search_term_lower, na=False)
        ]
    
    # Offering level filter
    if selected_offering_level != 'All Levels':
        filtered_df = filtered_df[filtered_df['offering_level'] == selected_offering_level]
    
    # Credential type filter
    if selected_credential != 'All Types':
        filtered_df = filtered_df[filtered_df['credential_type'] == selected_credential]
    
    # Institution filter
    if selected_institution != 'All Institutions':
        filtered_df = filtered_df[filtered_df['institution'] == selected_institution]
    
    # Delivery mode filter
    if selected_delivery != 'All Modes':
        filtered_df = filtered_df[filtered_df['delivery_mode'] == selected_delivery]
    
    # Data quality filter
    if selected_quality != 'All Quality Levels':
        filtered_df = filtered_df[filtered_df['data_quality'] == selected_quality.lower()]
    
    # Price filter
    filtered_df = filtered_df[
        (filtered_df['price_cad'].isna()) |
        ((filtered_df['price_cad'] >= price_range[0]) & (filtered_df['price_cad'] <= price_range[1]))
    ]
    
    # Duration filter
    filtered_df = filtered_df[
        (filtered_df['duration_weeks'].isna()) |
        ((filtered_df['duration_weeks'] >= duration_range[0]) & (filtered_df['duration_weeks'] <= duration_range[1]))
    ]
    
    # Calculate estimates
    full_estimates = estimate_unique_programs(df)
    filtered_estimates = estimate_unique_programs(filtered_df)
    
    # Search Results Badge (if searching)
    if search_term:
        unique_institutions_in_search = filtered_df['institution'].nunique()
        st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <span class="search-result-badge">
                🔍 Found {len(filtered_df):,} offerings for "{search_term}" across {unique_institutions_in_search} institutions
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Metrics Row - Lightcast style
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Offerings</div>
            <div class="metric-value">{len(filtered_df):,}</div>
            <div class="metric-delta">~{filtered_estimates['estimated_unique']:,} unique programs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        unique_institutions = filtered_df['institution'].nunique()
        total_institutions = df['institution'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Institutions</div>
            <div class="metric-value">{unique_institutions}</div>
            <div class="metric-delta">of {total_institutions} total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_price = filtered_df['price_cad'].mean()
        median_price = filtered_df['price_cad'].median()
        if pd.notna(avg_price):
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Average Price</div>
                <div class="metric-value">${avg_price:,.0f}</div>
                <div class="metric-delta">Median: ${median_price:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Average Price</div>
                <div class="metric-value">N/A</div>
                <div class="metric-delta">Insufficient data</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        thirty_days_ago = datetime.now() - timedelta(days=30)
        new_programs = len(filtered_df[filtered_df['date_added'] >= thirty_days_ago])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Recently Added</div>
            <div class="metric-value">{new_programs}</div>
            <div class="metric-delta">Last 30 days</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Lightcast-style note
    st.markdown(f"""
    <div class="info-box">
        📊 <strong>About these numbers:</strong> Total offerings includes all items in our database ({full_estimates['total']:,}). 
        Estimated unique programs (~{full_estimates['estimated_unique']:,}) accounts for component courses that may be part of larger credentials. 
        <strong>Institution count ({total_institutions})</strong> reflects universities with data in this dataset.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Market Overview", "Skills Intelligence", "Program Explorer", "Competitive Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-subheader">By Offering Level</div>', unsafe_allow_html=True)
            level_dist = filtered_df['offering_level'].value_counts()
            fig_level = px.pie(
                values=level_dist.values,
                names=level_dist.index,
                hole=0.4,
                color_discrete_sequence=['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']
            )
            fig_level.update_traces(
                textposition='outside',
                textinfo='label+percent',
                textfont_size=13
            )
            fig_level.update_layout(
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20),
                height=320,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='#374151')
            )
            st.plotly_chart(fig_level, use_container_width=True)
        
        with col2:
            st.markdown('<div class="section-subheader">By Credential Type</div>', unsafe_allow_html=True)
            cred_dist = filtered_df['credential_type'].value_counts().head(6)
            fig_cred = px.pie(
                values=cred_dist.values,
                names=cred_dist.index,
                hole=0.4,
                color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#6366f1']
            )
            fig_cred.update_traces(
                textposition='outside',
                textinfo='label+percent',
                textfont_size=13
            )
            fig_cred.update_layout(
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20),
                height=320,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='#374151')
            )
            st.plotly_chart(fig_cred, use_container_width=True)
        
        st.markdown('<div class="section-subheader">Top Institutions by Volume</div>', unsafe_allow_html=True)
        inst_counts = filtered_df['institution'].value_counts().head(15).reset_index()
        inst_counts.columns = ['Institution', 'Offerings']
        
        fig_inst = px.bar(
            inst_counts,
            x='Offerings',
            y='Institution',
            orientation='h',
            color='Offerings',
            color_continuous_scale=[[0, '#dbeafe'], [1, '#3b82f6']]
        )
        fig_inst.update_layout(
            showlegend=False,
            xaxis_title="Number of Offerings",
            yaxis_title="",
            margin=dict(l=20, r=20, t=20, b=20),
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='#374151'),
            xaxis=dict(gridcolor='#f3f4f6'),
            yaxis=dict(categoryorder='total ascending', gridcolor='#f3f4f6')
        )
        st.plotly_chart(fig_inst, use_container_width=True)
        
        st.markdown('<div class="section-subheader">Price vs. Duration Analysis</div>', unsafe_allow_html=True)
        scatter_df = filtered_df.dropna(subset=['price_cad', 'duration_weeks'])
        if len(scatter_df) > 0:
            fig_scatter = px.scatter(
                scatter_df,
                x='duration_weeks',
                y='price_cad',
                color='offering_level',
                size='price_cad',
                hover_data=['title', 'institution'],
                color_discrete_sequence=['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']
            )
            fig_scatter.update_layout(
                xaxis_title="Duration (weeks)",
                yaxis_title="Price (CAD)",
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='#374151'),
                xaxis=dict(gridcolor='#f3f4f6'),
                yaxis=dict(gridcolor='#f3f4f6'),
                legend=dict(
                    title="",
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("Not enough data with both price and duration for scatter plot")
    
    with tab2:
        # Extract and count skills
        all_skills = []
        for skills_str in filtered_df['skills'].dropna():
            if skills_str != 'Unknown':
                skills_list = [s.strip() for s in str(skills_str).split(',')]
                all_skills.extend(skills_list)
        
        if all_skills:
            skill_counts = Counter(all_skills)
            top_skills_data = skill_counts.most_common(20)
            
            skills_df = pd.DataFrame(top_skills_data, columns=['Skill', 'Count'])
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown('<div class="section-subheader">Top Skills in Market</div>', unsafe_allow_html=True)
                fig_skills = px.bar(
                    skills_df.head(15),
                    x='Count',
                    y='Skill',
                    orientation='h',
                    color='Count',
                    color_continuous_scale=[[0, '#dbeafe'], [1, '#3b82f6']]
                )
                fig_skills.update_layout(
                    showlegend=False,
                    xaxis_title="Number of Programs",
                    yaxis_title="",
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=520,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', color='#374151'),
                    xaxis=dict(gridcolor='#f3f4f6'),
                    yaxis=dict(categoryorder='total ascending', gridcolor='#f3f4f6')
                )
                st.plotly_chart(fig_skills, use_container_width=True)
            
            with col2:
                st.markdown('<div class="section-subheader">Market Leaders</div>', unsafe_allow_html=True)
                
                total_skill_mentions = sum(skill_counts.values())
                top_5_skills = skills_df.head(5)
                top_5_skills['Percentage'] = (top_5_skills['Count'] / total_skill_mentions * 100).round(1)
                
                for idx, row in top_5_skills.iterrows():
                    st.markdown(f"""
                    <div class="insight-card">
                        <div style="font-weight: 600; color: #111827; margin-bottom: 0.375rem; font-size: 0.9375rem;">{row['Skill']}</div>
                        <div style="color: #6b7280; font-size: 0.8125rem;">{row['Count']} mentions • {row['Percentage']}% of market</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No skills data available for current filters")
    
    with tab3:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f'<div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 1rem;">Showing {len(filtered_df):,} offerings (est. ~{filtered_estimates["estimated_unique"]:,} unique programs)</div>', unsafe_allow_html=True)
        
        with col2:
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Export Dataset",
                data=csv,
                file_name=f"credscout_export_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Format table
        display_df = filtered_df[[
            'title', 'institution', 'credential_type', 'offering_level',
            'delivery_mode', 'duration_weeks', 'price_cad', 'data_quality'
        ]].copy()
        
        display_df.columns = [
            'Program', 'Institution', 'Type', 'Level',
            'Delivery', 'Duration', 'Price', 'Quality'
        ]
        
        display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "Unknown")
        display_df['Duration'] = display_df['Duration'].apply(lambda x: f"{x:.0f}w" if pd.notna(x) else "Unknown")
        display_df['Quality'] = display_df['Quality'].apply(lambda x: x.title() if pd.notna(x) else "Unknown")
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=450,
            hide_index=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-subheader">Program Details</div>', unsafe_allow_html=True)
        
        if len(filtered_df) > 0:
            selected_program = st.selectbox(
                "Select program",
                options=filtered_df['title'].tolist(),
                label_visibility="collapsed"
            )
            
            if selected_program:
                program = filtered_df[filtered_df['title'] == selected_program].iloc[0]
                
                st.markdown(f"""
                <div class="insight-card" style="padding: 2rem;">
                    <h3 style="color: #111827; margin-bottom: 0.5rem; font-size: 1.25rem; font-weight: 600;">{program['title']}</h3>
                    <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 1.5rem;">
                        {program['institution']} • {program['credential_type'].title()}
                        <span class="badge-note">{program['offering_level'].replace('_', ' ').title()}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Delivery Mode**")
                    st.write(program['delivery_mode'] if pd.notna(program['delivery_mode']) else "Unknown")
                    st.markdown("**Duration**")
                    st.write(f"{program['duration_weeks']:.0f} weeks" if pd.notna(program['duration_weeks']) else program['duration_display'])
                
                with col2:
                    st.markdown("**Price**")
                    if pd.notna(program['price_cad']):
                        st.write(f"${program['price_cad']:,.0f} CAD")
                    else:
                        st.write(program['price_display'] if pd.notna(program['price_display']) else "Unknown")
                    st.markdown("**Data Quality**")
                    st.write(program['data_quality'].title())
                
                with col3:
                    st.markdown("**Date Added**")
                    st.write(program['date_added'].strftime('%B %d, %Y') if pd.notna(program['date_added']) else "Unknown")
                    st.markdown("**Program Link**")
                    st.markdown(f"[Visit Program Page →]({program['program_url']})")
                
                st.markdown("---")
                
                if pd.notna(program['description']) and program['description'] != 'Unknown':
                    st.markdown("**Description**")
                    st.write(program['description'])
                
                if pd.notna(program['skills']) and program['skills'] != 'Unknown':
                    st.markdown("**Skills**")
                    skills_list = [s.strip() for s in str(program['skills']).split(',')]
                    skills_html = " ".join([f'<span style="background: #eff6ff; color: #1e40af; padding: 0.375rem 0.75rem; border-radius: 6px; font-size: 0.8125rem; margin-right: 0.5rem; margin-bottom: 0.5rem; display: inline-block; border: 1px solid #bfdbfe;">{skill}</span>' for skill in skills_list])
                    st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.info("No programs match your current filters")
    
    with tab4:
        st.markdown('<div class="section-subheader">Top Institutions by Volume</div>', unsafe_allow_html=True)
        
        institution_stats = filtered_df.groupby('institution').agg({
            'program_id': 'count',
            'price_cad': 'mean',
            'duration_weeks': 'mean'
        }).round(0).reset_index()
        
        institution_stats.columns = ['Institution', 'Offerings', 'Avg Price', 'Avg Duration']
        institution_stats = institution_stats.sort_values('Offerings', ascending=False).head(10)
        institution_stats['Avg Price'] = institution_stats['Avg Price'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "N/A")
        institution_stats['Avg Duration'] = institution_stats['Avg Duration'].apply(lambda x: f"{x:.0f}w" if pd.notna(x) else "N/A")
        
        st.dataframe(
            institution_stats,
            use_container_width=True,
            hide_index=True,
            height=380
        )
        
        st.markdown('<div class="section-subheader">Price Distribution by Offering Level</div>', unsafe_allow_html=True)
        
        price_df = filtered_df.dropna(subset=['price_cad', 'offering_level'])
        if len(price_df) > 0:
            fig_box = px.box(
                price_df,
                x='offering_level',
                y='price_cad',
                color='offering_level',
                color_discrete_sequence=['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']
            )
            fig_box.update_layout(
                showlegend=False,
                xaxis_title="",
                yaxis_title="Price (CAD)",
                height=380,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='#374151'),
                xaxis=dict(gridcolor='#f3f4f6'),
                yaxis=dict(gridcolor='#f3f4f6')
            )
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.info("Insufficient price data for distribution analysis")

else:
    st.markdown("""
    <div style="background: white; padding: 3.5rem; border-radius: 16px; border: 1px solid #e5e7eb; max-width: 900px; margin: 3rem auto;">
        <h2 style="color: #111827; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em;">Welcome to CredScout Intelligence</h2>
        
        <p style="color: #6b7280; line-height: 1.7; margin-bottom: 2rem; font-size: 1rem;">
            Upload your preprocessed continuing professional education dataset to access comprehensive market intelligence.
        </p>
        
        <h3 style="color: #111827; margin-bottom: 1rem; font-size: 1.125rem; font-weight: 600;">Quick Start</h3>
        
        <div style="background: #f9fafb; padding: 2rem; border-radius: 12px; border: 1px solid #e5e7eb; margin-bottom: 1.5rem;">
            <ol style="color: #374151; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li>Run <code style="background: #e5e7eb; padding: 0.25rem 0.5rem; border-radius: 4px; font-family: monospace;">preprocess_cpe_data.py</code> on your scraped data</li>
                <li>Upload the generated <code style="background: #e5e7eb; padding: 0.25rem 0.5rem; border-radius: 4px; font-family: monospace;">credscout_processed_data.csv</code></li>
                <li>Explore market intelligence across 4 tabs</li>
            </ol>
        </div>
        
        <p style="color: #9ca3af; font-size: 0.875rem;">
            📊 Transparent metrics • Lightcast-style estimates • Professional analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
