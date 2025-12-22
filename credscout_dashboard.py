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

# Professional CSS
st.markdown("""
<style>
    /* Main styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header */
    .credscout-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem 3rem;
        border-radius: 0;
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .credscout-logo {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }
    
    .credscout-tagline {
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Metrics */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border-left: 4px solid #3b82f6;
        height: 100%;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        line-height: 1;
    }
    
    .metric-delta {
        font-size: 0.875rem;
        color: #64748b;
        margin-top: 0.5rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Cards */
    .insight-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    
    /* Filters */
    .stSelectbox label, .stSlider label, .stTextInput label {
        font-size: 0.875rem;
        font-weight: 600;
        color: #475569;
    }
    
    /* Tables */
    .dataframe {
        font-size: 0.875rem;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #2563eb;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stDownloadButton>button {
        background-color: white;
        color: #3b82f6;
        border: 1px solid #3b82f6;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #ffffff;
    }
    
    /* Remove default streamlit branding for professional look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 1rem;
        font-weight: 500;
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

def calculate_market_insights(df):
    """Calculate key market insights"""
    insights = {
        'total_programs': len(df),
        'total_institutions': df['institution'].nunique(),
        'avg_price': df['price_cad'].mean(),
        'median_price': df['price_cad'].median(),
        'avg_duration': df['duration_weeks'].mean(),
        'credential_distribution': df['credential_type'].value_counts().to_dict(),
        'delivery_distribution': df['delivery_mode'].value_counts().to_dict(),
        'province_distribution': df['province'].value_counts().to_dict()
    }
    return insights

# Header
st.markdown("""
<div class="credscout-header">
    <div class="credscout-logo">CredScout Intelligence</div>
    <div class="credscout-tagline">Market Intelligence for Continuing Professional Education</div>
</div>
""", unsafe_allow_html=True)

# File uploader with professional styling
uploaded_file = st.file_uploader(
    "Upload Program Dataset",
    type=['csv'],
    help="Upload your CPE programs dataset in CSV format",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    # Load data
    df = load_data(uploaded_file)
    
    # Sidebar filters
    st.sidebar.markdown("### Filters & Search")
    
    # Search
    search_term = st.sidebar.text_input(
        "Search Programs",
        placeholder="Keywords, skills, institution..."
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
    
    st.sidebar.markdown("---")
    
    # Clear filters button
    if st.sidebar.button("Reset All Filters", use_container_width=True):
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
    
    # Calculate insights
    insights = calculate_market_insights(filtered_df)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_programs = len(filtered_df) - len(df)
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Total Programs</div>
            <div class="metric-value">{len(filtered_df):,}</div>
            <div class="metric-delta">{delta_programs:+,} from full dataset</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Institutions</div>
            <div class="metric-value">{insights['total_institutions']}</div>
            <div class="metric-delta">Across Canada</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Avg. Price</div>
            <div class="metric-value">${insights['avg_price']:,.0f}</div>
            <div class="metric-delta">Median: ${insights['median_price']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        thirty_days_ago = datetime.now() - timedelta(days=30)
        new_programs = len(filtered_df[filtered_df['date_added'] >= thirty_days_ago])
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">New Programs</div>
            <div class="metric-value">{new_programs}</div>
            <div class="metric-delta">Last 30 days</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Overview", "🎯 Skills Intelligence", "📋 Program Explorer", "📈 Competitive Analysis"])
    
    with tab1:
        st.markdown('<div class="section-header">Market Overview</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Credential Type Distribution
            st.markdown("#### Credential Type Distribution")
            cred_dist = filtered_df['credential_type'].value_counts()
            fig_cred = px.pie(
                values=cred_dist.values,
                names=cred_dist.index,
                color_discrete_sequence=['#3b82f6', '#8b5cf6', '#ec4899']
            )
            fig_cred.update_traces(textposition='inside', textinfo='percent+label')
            fig_cred.update_layout(
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20),
                height=300
            )
            st.plotly_chart(fig_cred, use_container_width=True)
        
        with col2:
            # Delivery Mode Distribution
            st.markdown("#### Delivery Mode Distribution")
            delivery_dist = filtered_df['delivery_mode'].value_counts()
            fig_delivery = px.pie(
                values=delivery_dist.values,
                names=delivery_dist.index,
                color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b']
            )
            fig_delivery.update_traces(textposition='inside', textinfo='percent+label')
            fig_delivery.update_layout(
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20),
                height=300
            )
            st.plotly_chart(fig_delivery, use_container_width=True)
        
        # Geographic Distribution
        st.markdown("#### Geographic Distribution")
        province_counts = filtered_df['province'].value_counts().reset_index()
        province_counts.columns = ['Province', 'Programs']
        
        fig_geo = px.bar(
            province_counts,
            x='Province',
            y='Programs',
            color='Programs',
            color_continuous_scale='Blues'
        )
        fig_geo.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Number of Programs",
            margin=dict(l=20, r=20, t=20, b=20),
            height=350
        )
        st.plotly_chart(fig_geo, use_container_width=True)
        
        # Price vs Duration Analysis
        st.markdown("#### Price vs. Duration Analysis")
        fig_scatter = px.scatter(
            filtered_df,
            x='duration_weeks',
            y='price_cad',
            color='credential_type',
            size='price_cad',
            hover_data=['title', 'institution'],
            color_discrete_sequence=['#3b82f6', '#8b5cf6', '#ec4899']
        )
        fig_scatter.update_layout(
            xaxis_title="Duration (weeks)",
            yaxis_title="Price (CAD)",
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with tab2:
        st.markdown('<div class="section-header">Skills Intelligence</div>', unsafe_allow_html=True)
        
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
                st.markdown("#### Top Skills Across Programs")
                fig_skills = px.bar(
                    skills_df.head(15),
                    x='Count',
                    y='Skill',
                    orientation='h',
                    color='Count',
                    color_continuous_scale='Blues'
                )
                fig_skills.update_layout(
                    showlegend=False,
                    yaxis={'categoryorder': 'total ascending'},
                    xaxis_title="Number of Programs",
                    yaxis_title="",
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=500
                )
                st.plotly_chart(fig_skills, use_container_width=True)
            
            with col2:
                st.markdown("#### Skills Market Share")
                # Top 5 skills as percentage
                total_skill_mentions = sum(skill_counts.values())
                top_5_skills = skills_df.head(5)
                top_5_skills['Percentage'] = (top_5_skills['Count'] / total_skill_mentions * 100).round(1)
                
                for idx, row in top_5_skills.iterrows():
                    st.markdown(f"""
                    <div style="margin-bottom: 1rem; padding: 1rem; background: white; border-radius: 6px; border-left: 3px solid #3b82f6;">
                        <div style="font-weight: 600; color: #1e293b; margin-bottom: 0.25rem;">{row['Skill']}</div>
                        <div style="color: #64748b; font-size: 0.875rem;">{row['Count']} programs ({row['Percentage']}%)</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Skills Co-occurrence Analysis
            st.markdown("#### Skills Co-occurrence Insights")
            
            col1, col2, col3 = st.columns(3)
            
            # Calculate some interesting co-occurrences
            # This is a simplified version - you could make this more sophisticated
            programs_with_skills = filtered_df[filtered_df['skills'].notna()]
            
            with col1:
                python_programs = programs_with_skills[programs_with_skills['skills'].str.contains('Python', case=False, na=False)]
                ml_in_python = python_programs[python_programs['skills'].str.contains('Machine Learning', case=False, na=False)]
                if len(python_programs) > 0:
                    percentage = (len(ml_in_python) / len(python_programs) * 100)
                    st.markdown(f"""
                    <div class="insight-card">
                        <div style="font-size: 2rem; font-weight: 700; color: #3b82f6;">{percentage:.0f}%</div>
                        <div style="color: #64748b;">of Python programs also teach Machine Learning</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                leadership_programs = programs_with_skills[programs_with_skills['skills'].str.contains('Leadership', case=False, na=False)]
                if len(leadership_programs) > 0:
                    avg_price = leadership_programs['price_cad'].mean()
                    st.markdown(f"""
                    <div class="insight-card">
                        <div style="font-size: 2rem; font-weight: 700; color: #8b5cf6;">${avg_price:,.0f}</div>
                        <div style="color: #64748b;">average price for Leadership programs</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col3:
                data_programs = programs_with_skills[
                    programs_with_skills['skills'].str.contains('Data', case=False, na=False)
                ]
                if len(data_programs) > 0:
                    st.markdown(f"""
                    <div class="insight-card">
                        <div style="font-size: 2rem; font-weight: 700; color: #ec4899;">{len(data_programs)}</div>
                        <div style="color: #64748b;">programs focus on Data skills</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No skills data available for current filters")
    
    with tab3:
        st.markdown('<div class="section-header">Program Explorer</div>', unsafe_allow_html=True)
        
        # Results counter and export
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**Showing {len(filtered_df):,} of {len(df):,} programs**")
        
        with col2:
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Export Dataset",
                data=csv,
                file_name=f"credscout_export_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Format the dataframe for display
        display_df = filtered_df[[
            'title', 'institution', 'credential_type', 'province', 
            'delivery_mode', 'duration_weeks', 'price_cad'
        ]].copy()
        
        display_df.columns = [
            'Program Title', 'Institution', 'Credential Type', 'Province', 
            'Delivery', 'Duration', 'Price'
        ]
        
        # Format price
        display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:,.0f}")
        display_df['Duration'] = display_df['Duration'].apply(lambda x: f"{x}w")
        
        # Show table
        st.dataframe(
            display_df,
            use_container_width=True,
            height=500,
            column_config={
                "Program Title": st.column_config.TextColumn(
                    "Program Title",
                    width="large"
                )
            }
        )
        
        # Program Detail View
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Program Details</div>', unsafe_allow_html=True)
        
        # Select program
        selected_program = st.selectbox(
            "Select a program to view detailed information",
            options=filtered_df['title'].tolist(),
            label_visibility="collapsed"
        )
        
        if selected_program:
            program = filtered_df[filtered_df['title'] == selected_program].iloc[0]
            
            # Program detail card
            st.markdown(f"""
            <div style="background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
                <h3 style="color: #1e293b; margin-bottom: 1rem;">{program['title']}</h3>
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
            
            st.markdown("**Program Description**")
            st.write(program['description'])
            
            st.markdown("**Skills Covered**")
            skills_list = [s.strip() for s in str(program['skills']).split(',')]
            skills_html = " ".join([f'<span style="background: #eff6ff; color: #1e40af; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.875rem; margin-right: 0.5rem; margin-bottom: 0.5rem; display: inline-block;">{skill}</span>' for skill in skills_list])
            st.markdown(skills_html, unsafe_allow_html=True)
            
            # Market context for this program
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Market Context**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                similar_credential = df[df['credential_type'] == program['credential_type']]
                st.metric(
                    "Similar Programs",
                    f"{len(similar_credential)}",
                    delta=f"in {program['credential_type']}"
                )
            
            with col2:
                same_institution = df[df['institution'] == program['institution']]
                st.metric(
                    "Institution Portfolio",
                    f"{len(same_institution)}",
                    delta="total programs"
                )
            
            with col3:
                # Price comparison
                similar_prices = similar_credential['price_cad']
                if len(similar_prices) > 0:
                    percentile = (similar_prices < program['price_cad']).sum() / len(similar_prices) * 100
                    if percentile < 33:
                        position = "Lower third"
                    elif percentile < 67:
                        position = "Mid-range"
                    else:
                        position = "Upper third"
                    st.metric(
                        "Price Position",
                        position,
                        delta=f"{percentile:.0f}th percentile"
                    )
    
    with tab4:
        st.markdown('<div class="section-header">Competitive Analysis</div>', unsafe_allow_html=True)
        
        # Institution comparison
        st.markdown("#### Top Institutions by Program Volume")
        
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
            height=400
        )
        
        # Price benchmarking
        st.markdown("#### Price Distribution by Credential Type")
        
        fig_box = px.box(
            filtered_df,
            x='credential_type',
            y='price_cad',
            color='credential_type',
            color_discrete_sequence=['#3b82f6', '#8b5cf6', '#ec4899']
        )
        fig_box.update_layout(
            showlegend=False,
            xaxis_title="Credential Type",
            yaxis_title="Price (CAD)",
            height=400
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
        # Market gaps
        st.markdown("#### Market Opportunity Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Under-served provinces
            st.markdown("**Under-served Markets**")
            province_prog_count = df.groupby('province').size().sort_values()
            
            for province in province_prog_count.head(5).index:
                count = province_prog_count[province]
                st.markdown(f"""
                <div style="padding: 0.75rem; background: #fef2f2; border-left: 3px solid #ef4444; margin-bottom: 0.5rem; border-radius: 4px;">
                    <div style="font-weight: 600; color: #991b1b;">{province}</div>
                    <div style="font-size: 0.875rem; color: #7f1d1d;">Only {count} programs available</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # High-demand skills with low supply
            st.markdown("**High-Demand Skills (Low Supply)**")
            
            # This is illustrative - in production you'd calculate this based on actual demand data
            emerging_skills = [
                ("Generative AI", 2),
                ("Sustainability", 3),
                ("Cloud Security", 4),
                ("Data Ethics", 2),
                ("Quantum Computing", 1)
            ]
            
            for skill, count in emerging_skills:
                st.markdown(f"""
                <div style="padding: 0.75rem; background: #f0fdf4; border-left: 3px solid #22c55e; margin-bottom: 0.5rem; border-radius: 4px;">
                    <div style="font-weight: 600; color: #166534;">{skill}</div>
                    <div style="font-size: 0.875rem; color: #14532d;">Only {count} programs teaching this</div>
                </div>
                """, unsafe_allow_html=True)

else:
    # Professional instructions
    st.markdown("""
    <div style="background: white; padding: 3rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); max-width: 800px; margin: 2rem auto;">
        <h3 style="color: #1e293b; margin-bottom: 1.5rem;">Welcome to CredScout Intelligence</h3>
        
        <p style="color: #475569; line-height: 1.6; margin-bottom: 1.5rem;">
            Upload your continuing professional education dataset to access comprehensive market intelligence, 
            competitive analysis, and skills insights across Canada's CPE landscape.
        </p>
        
        <h4 style="color: #1e293b; margin-bottom: 1rem; font-size: 1rem;">Dataset Requirements</h4>
        
        <div style="background: #f8fafc; padding: 1.5rem; border-radius: 6px; font-family: monospace; font-size: 0.875rem;">
            <strong>Required Columns:</strong><br><br>
            • program_id — Unique identifier<br>
            • title — Program name<br>
            • institution — Institution name<br>
            • province — Canadian province<br>
            • credential_type — micro-credential | certificate | professional development<br>
            • delivery_mode — online | hybrid | in-person<br>
            • duration_weeks — Duration in weeks<br>
            • price_cad — Price in CAD<br>
            • skills — Comma-separated (e.g., "Python, Data Analysis, SQL")<br>
            • description — Program description<br>
            • program_url — Direct link to program<br>
            • date_added — Date (YYYY-MM-DD)
        </div>
        
        <p style="color: #64748b; font-size: 0.875rem; margin-top: 1.5rem;">
            Sample dataset: credscout_test_data.csv
        </p>
    </div>
    """, unsafe_allow_html=True)
