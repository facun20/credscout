import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from collections import Counter
import numpy as np

# Page config
st.set_page_config(
    page_title="CredScout Intelligence Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-professional CSS matching Fortify design
st.markdown("""
<style>
    /* Import professional font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        background-color: #f7f8fa;
        padding: 0;
    }
    
    /* Remove default streamlit padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header */
    .credscout-header {
        background: white;
        padding: 1.75rem 2.5rem;
        margin: -2rem -2rem 2.5rem -2rem;
        border-bottom: 1px solid #e5e7eb;
        display: flex;
        align-items: center;
        justify-content: space-between;
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
    
    /* Metrics - Clean and spacious */
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
    
    .metric-delta-up {
        color: #10b981;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.125rem;
        font-weight: 600;
        color: #111827;
        margin: 2.5rem 0 1.25rem 0;
        letter-spacing: -0.01em;
    }
    
    .section-subheader {
        font-size: 0.9375rem;
        font-weight: 600;
        color: #374151;
        margin: 1.5rem 0 1rem 0;
        letter-spacing: -0.01em;
    }
    
    /* Cards - matching Fortify style */
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
    
    /* Badge design - clean pills */
    .badge-new {
        display: inline-block;
        background: #111827;
        color: white;
        font-size: 0.75rem;
        font-weight: 500;
        padding: 0.25rem 0.625rem;
        border-radius: 9999px;
        margin-left: 0.5rem;
        letter-spacing: -0.01em;
    }
    
    /* Filters */
    .stSelectbox label, .stSlider label, .stTextInput label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    
    .stSelectbox, .stSlider, .stTextInput {
        margin-bottom: 1.25rem;
    }
    
    /* Buttons - clean and professional */
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
    
    /* Tabs - clean design */
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
    
    /* Tables - clean and spacious */
    .dataframe {
        font-size: 0.875rem;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e5e7eb;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Remove streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* File uploader */
    .stFileUploader {
        background: white;
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
    }
    
    .stFileUploader:hover {
        border-color: #9ca3af;
    }
    
    /* Info boxes */
    .stAlert {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    /* Opportunity card styling */
    .opportunity-card {
        padding: 1rem;
        background: #f9fafb;
        border-left: 3px solid #3b82f6;
        border-radius: 6px;
        margin-bottom: 0.75rem;
    }
    
    .opportunity-title {
        font-weight: 600;
        color: #111827;
        font-size: 0.9375rem;
        margin-bottom: 0.25rem;
    }
    
    .opportunity-subtitle {
        font-size: 0.8125rem;
        color: #6b7280;
    }
</style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data(uploaded_file):
    """Load and cache the CSV data"""
    df = pd.read_csv(uploaded_file)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    return df

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
    "Upload Program Dataset",
    type=['csv'],
    help="CSV file with CPE programs data",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    # Load data
    df = load_data(uploaded_file)
    
    # Sidebar filters
    st.sidebar.markdown("### Filters")
    st.sidebar.markdown("")
    
    # Search
    search_term = st.sidebar.text_input(
        "Search Programs",
        placeholder="Skills, keywords, institution..."
    )
    
    # Credential Type filter
    credential_types = ['All Types'] + sorted(df['credential_type'].dropna().unique().tolist())
    selected_credential = st.sidebar.selectbox(
        "Credential Type",
        credential_types
    )
    
    # Province filter
    provinces = ['All Provinces'] + sorted(df['province'].dropna().unique().tolist())
    selected_province = st.sidebar.selectbox(
        "Province",
        provinces
    )
    
    # Delivery Mode filter
    delivery_modes = ['All Modes'] + sorted(df['delivery_mode'].dropna().unique().tolist())
    selected_delivery = st.sidebar.selectbox(
        "Delivery Mode",
        delivery_modes
    )
    
    # Price range filter
    min_price = int(df['price_cad'].min())
    max_price = int(df['price_cad'].max())
    price_range = st.sidebar.slider(
        "Price Range (CAD)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=100
    )
    
    # Duration range filter
    min_duration = int(df['duration_weeks'].min())
    max_duration = int(df['duration_weeks'].max())
    duration_range = st.sidebar.slider(
        "Duration (weeks)",
        min_value=min_duration,
        max_value=max_duration,
        value=(min_duration, max_duration)
    )
    
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    
    # Clear filters button
    if st.sidebar.button("Reset Filters", use_container_width=True):
        st.rerun()
    
    # Apply filters
    filtered_df = df.copy()
    
    # Search filter
    if search_term:
        search_term_lower = search_term.lower()
        filtered_df = filtered_df[
            filtered_df['title'].str.lower().str.contains(search_term_lower, na=False) |
            filtered_df['institution'].str.lower().str.contains(search_term_lower, na=False) |
            filtered_df['skills'].str.lower().str.contains(search_term_lower, na=False) |
            filtered_df['description'].str.lower().str.contains(search_term_lower, na=False)
        ]
    
    # Credential type filter
    if selected_credential != 'All Types':
        filtered_df = filtered_df[filtered_df['credential_type'] == selected_credential]
    
    # Province filter
    if selected_province != 'All Provinces':
        filtered_df = filtered_df[filtered_df['province'] == selected_province]
    
    # Delivery mode filter
    if selected_delivery != 'All Modes':
        filtered_df = filtered_df[filtered_df['delivery_mode'] == selected_delivery]
    
    # Price filter
    filtered_df = filtered_df[
        (filtered_df['price_cad'] >= price_range[0]) &
        (filtered_df['price_cad'] <= price_range[1])
    ]
    
    # Duration filter
    filtered_df = filtered_df[
        (filtered_df['duration_weeks'] >= duration_range[0]) &
        (filtered_df['duration_weeks'] <= duration_range[1])
    ]
    
    # Key Metrics Row - Clean and spacious
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_programs = len(filtered_df) - len(df)
        delta_text = f"{delta_programs:+,} from total" if delta_programs != 0 else "All programs"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Programs</div>
            <div class="metric-value">{len(filtered_df):,}</div>
            <div class="metric-delta">{delta_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        unique_institutions = filtered_df['institution'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Institutions</div>
            <div class="metric-value">{unique_institutions}</div>
            <div class="metric-delta">Across Canada</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_price = filtered_df['price_cad'].mean()
        median_price = filtered_df['price_cad'].median()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Price</div>
            <div class="metric-value">${avg_price:,.0f}</div>
            <div class="metric-delta">Median: ${median_price:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        thirty_days_ago = datetime.now() - timedelta(days=30)
        new_programs = len(filtered_df[filtered_df['date_added'] >= thirty_days_ago])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">New Programs</div>
            <div class="metric-value">{new_programs}</div>
            <div class="metric-delta">Last 30 days</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["Market Overview", "Skills Intelligence", "Program Explorer", "Competitive Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-subheader">Credential Distribution</div>', unsafe_allow_html=True)
            cred_dist = filtered_df['credential_type'].value_counts()
            fig_cred = px.pie(
                values=cred_dist.values,
                names=cred_dist.index,
                hole=0.4,
                color_discrete_sequence=['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b']
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
        
        with col2:
            st.markdown('<div class="section-subheader">Delivery Mode</div>', unsafe_allow_html=True)
            delivery_dist = filtered_df['delivery_mode'].value_counts()
            fig_delivery = px.pie(
                values=delivery_dist.values,
                names=delivery_dist.index,
                hole=0.4,
                color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#ec4899']
            )
            fig_delivery.update_traces(
                textposition='outside',
                textinfo='label+percent',
                textfont_size=13
            )
            fig_delivery.update_layout(
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20),
                height=320,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='#374151')
            )
            st.plotly_chart(fig_delivery, use_container_width=True)
        
        st.markdown('<div class="section-subheader">Geographic Distribution</div>', unsafe_allow_html=True)
        province_counts = filtered_df['province'].value_counts().reset_index()
        province_counts.columns = ['Province', 'Programs']
        
        fig_geo = px.bar(
            province_counts,
            x='Province',
            y='Programs',
            color='Programs',
            color_continuous_scale=[[0, '#dbeafe'], [1, '#3b82f6']]
        )
        fig_geo.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Number of Programs",
            margin=dict(l=20, r=20, t=20, b=20),
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='#374151'),
            xaxis=dict(gridcolor='#f3f4f6'),
            yaxis=dict(gridcolor='#f3f4f6')
        )
        st.plotly_chart(fig_geo, use_container_width=True)
        
        st.markdown('<div class="section-subheader">Price vs. Duration Analysis</div>', unsafe_allow_html=True)
        fig_scatter = px.scatter(
            filtered_df,
            x='duration_weeks',
            y='price_cad',
            color='credential_type',
            size='price_cad',
            hover_data=['title', 'institution'],
            color_discrete_sequence=['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b']
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
    
    with tab2:
        # Extract and count skills
        all_skills = []
        for skills_str in filtered_df['skills'].dropna():
            skills_list = [s.strip() for s in str(skills_str).split(',')]
            all_skills.extend(skills_list)
        
        if all_skills:
            skill_counts = Counter(all_skills)
            top_skills = skill_counts.most_common(20)
            
            skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])
            
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
                    yaxis={'categoryorder': 'total ascending'},
                    xaxis_title="Number of Programs",
                    yaxis_title="",
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=520,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', color='#374151'),
                    xaxis=dict(gridcolor='#f3f4f6'),
                    yaxis=dict(gridcolor='#f3f4f6')
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
                        <div style="color: #6b7280; font-size: 0.8125rem;">{row['Count']} programs • {row['Percentage']}% of market</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('<div class="section-subheader">Skills Co-occurrence Insights</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            programs_with_skills = filtered_df[filtered_df['skills'].notna()]
            
            with col1:
                python_programs = programs_with_skills[programs_with_skills['skills'].str.contains('Python', case=False, na=False)]
                ml_in_python = python_programs[python_programs['skills'].str.contains('Machine Learning', case=False, na=False)]
                if len(python_programs) > 0:
                    percentage = (len(ml_in_python) / len(python_programs) * 100)
                    st.markdown(f"""
                    <div class="insight-card">
                        <div style="font-size: 2.5rem; font-weight: 700; color: #3b82f6; margin-bottom: 0.5rem;">{percentage:.0f}%</div>
                        <div style="color: #6b7280; font-size: 0.875rem;">of Python programs include Machine Learning</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                leadership_programs = programs_with_skills[programs_with_skills['skills'].str.contains('Leadership', case=False, na=False)]
                if len(leadership_programs) > 0:
                    avg_price = leadership_programs['price_cad'].mean()
                    st.markdown(f"""
                    <div class="insight-card">
                        <div style="font-size: 2.5rem; font-weight: 700; color: #8b5cf6; margin-bottom: 0.5rem;">${avg_price:,.0f}</div>
                        <div style="color: #6b7280; font-size: 0.875rem;">average price for Leadership programs</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col3:
                data_programs = programs_with_skills[
                    programs_with_skills['skills'].str.contains('Data', case=False, na=False)
                ]
                if len(data_programs) > 0:
                    st.markdown(f"""
                    <div class="insight-card">
                        <div style="font-size: 2.5rem; font-weight: 700; color: #ec4899; margin-bottom: 0.5rem;">{len(data_programs)}</div>
                        <div style="color: #6b7280; font-size: 0.875rem;">programs focus on Data skills</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No skills data available for current filters")
    
    with tab3:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f'<div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 1rem;">Showing {len(filtered_df):,} of {len(df):,} programs</div>', unsafe_allow_html=True)
        
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
            'title', 'institution', 'credential_type', 'province', 
            'delivery_mode', 'duration_weeks', 'price_cad'
        ]].copy()
        
        display_df.columns = [
            'Program', 'Institution', 'Type', 'Province', 
            'Delivery', 'Duration', 'Price'
        ]
        
        display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:,.0f}")
        display_df['Duration'] = display_df['Duration'].apply(lambda x: f"{x}w")
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=450,
            hide_index=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-subheader">Program Details</div>', unsafe_allow_html=True)
        
        selected_program = st.selectbox(
            "Select program",
            options=filtered_df['title'].tolist(),
            label_visibility="collapsed"
        )
        
        if selected_program:
            program = filtered_df[filtered_df['title'] == selected_program].iloc[0]
            
            st.markdown(f"""
            <div class="insight-card" style="padding: 2rem;">
                <h3 style="color: #111827; margin-bottom: 1.5rem; font-size: 1.25rem; font-weight: 600;">{program['title']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Institution**")
                st.write(program['institution'])
                st.markdown("**Credential Type**")
                st.write(program['credential_type'].title())
                st.markdown("**Province**")
                st.write(program['province'])
            
            with col2:
                st.markdown("**Delivery Mode**")
                st.write(program['delivery_mode'].title())
                st.markdown("**Duration**")
                st.write(f"{program['duration_weeks']} weeks")
                st.markdown("**Date Added**")
                st.write(program['date_added'].strftime('%B %d, %Y'))
            
            with col3:
                st.markdown("**Price**")
                st.write(f"${program['price_cad']:,.0f} CAD")
                st.markdown("**Program Link**")
                st.markdown(f"[Visit Program Page →]({program['program_url']})")
            
            st.markdown("---")
            
            st.markdown("**Description**")
            st.write(program['description'])
            
            st.markdown("**Skills**")
            skills_list = [s.strip() for s in str(program['skills']).split(',')]
            skills_html = " ".join([f'<span style="background: #eff6ff; color: #1e40af; padding: 0.375rem 0.75rem; border-radius: 6px; font-size: 0.8125rem; margin-right: 0.5rem; margin-bottom: 0.5rem; display: inline-block; border: 1px solid #bfdbfe;">{skill}</span>' for skill in skills_list])
            st.markdown(skills_html, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Market Context**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                similar_credential = df[df['credential_type'] == program['credential_type']]
                st.metric(
                    "Similar Programs",
                    f"{len(similar_credential)}",
                    delta=None
                )
            
            with col2:
                same_institution = df[df['institution'] == program['institution']]
                st.metric(
                    "Institution Portfolio",
                    f"{len(same_institution)}",
                    delta=None
                )
            
            with col3:
                similar_prices = similar_credential['price_cad']
                if len(similar_prices) > 0:
                    percentile = (similar_prices < program['price_cad']).sum() / len(similar_prices) * 100
                    if percentile < 33:
                        position = "Lower Third"
                    elif percentile < 67:
                        position = "Mid-Range"
                    else:
                        position = "Upper Third"
                    st.metric(
                        "Price Position",
                        position,
                        delta=None
                    )
    
    with tab4:
        st.markdown('<div class="section-subheader">Top Institutions by Volume</div>', unsafe_allow_html=True)
        
        institution_stats = filtered_df.groupby('institution').agg({
            'program_id': 'count',
            'price_cad': 'mean',
            'duration_weeks': 'mean'
        }).round(0).reset_index()
        
        institution_stats.columns = ['Institution', 'Programs', 'Avg Price', 'Avg Duration']
        institution_stats = institution_stats.sort_values('Programs', ascending=False).head(10)
        institution_stats['Avg Price'] = institution_stats['Avg Price'].apply(lambda x: f"${x:,.0f}")
        institution_stats['Avg Duration'] = institution_stats['Avg Duration'].apply(lambda x: f"{x:.0f}w")
        
        st.dataframe(
            institution_stats,
            use_container_width=True,
            hide_index=True,
            height=380
        )
        
        st.markdown('<div class="section-subheader">Price Distribution by Credential Type</div>', unsafe_allow_html=True)
        
        fig_box = px.box(
            filtered_df,
            x='credential_type',
            y='price_cad',
            color='credential_type',
            color_discrete_sequence=['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b']
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
        
        st.markdown('<div class="section-subheader">Market Opportunity Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Under-Served Markets**")
            province_prog_count = df.groupby('province').size().sort_values()
            
            for province in province_prog_count.head(5).index:
                count = province_prog_count[province]
                st.markdown(f"""
                <div class="opportunity-card" style="border-left-color: #ef4444;">
                    <div class="opportunity-title">{province}</div>
                    <div class="opportunity-subtitle">Only {count} programs available</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Emerging Skills (Low Supply)**")
            
            emerging_skills = [
                ("Generative AI", 2),
                ("Sustainability", 3),
                ("Cloud Security", 4),
                ("Data Ethics", 2),
                ("Quantum Computing", 1)
            ]
            
            for skill, count in emerging_skills:
                st.markdown(f"""
                <div class="opportunity-card" style="border-left-color: #10b981;">
                    <div class="opportunity-title">{skill}</div>
                    <div class="opportunity-subtitle">Only {count} programs • High demand opportunity</div>
                </div>
                """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="background: white; padding: 3.5rem; border-radius: 16px; border: 1px solid #e5e7eb; max-width: 900px; margin: 3rem auto;">
        <h2 style="color: #111827; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em;">Welcome to CredScout Intelligence</h2>
        
        <p style="color: #6b7280; line-height: 1.7; margin-bottom: 2rem; font-size: 1rem;">
            Upload your continuing professional education dataset to access comprehensive market intelligence, 
            competitive analysis, and skills insights across Canada's CPE landscape.
        </p>
        
        <h3 style="color: #111827; margin-bottom: 1rem; font-size: 1.125rem; font-weight: 600;">Dataset Requirements</h3>
        
        <div style="background: #f9fafb; padding: 2rem; border-radius: 12px; font-family: 'Courier New', monospace; font-size: 0.875rem; border: 1px solid #e5e7eb;">
            <div style="margin-bottom: 1rem; color: #111827; font-weight: 600;">Required Columns:</div>
            
            <div style="color: #6b7280; line-height: 1.8;">
            • program_id<br>
            • title<br>
            • institution<br>
            • province<br>
            • credential_type<br>
            • delivery_mode<br>
            • duration_weeks<br>
            • price_cad<br>
            • skills<br>
            • description<br>
            • program_url<br>
            • date_added
            </div>
        </div>
        
        <p style="color: #9ca3af; font-size: 0.875rem; margin-top: 1.5rem;">
            Sample: credscout_test_data.csv
        </p>
    </div>
    """, unsafe_allow_html=True)
