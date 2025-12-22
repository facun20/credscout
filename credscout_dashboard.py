import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from collections import Counter

# Page config
st.set_page_config(
    page_title="CredScout Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e293b 0%, #334155 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data(uploaded_file):
    """Load and cache the CSV data"""
    df = pd.read_csv(uploaded_file)
    # Ensure date_added is datetime
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    return df

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 CredScout Intelligence Platform</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">Market Intelligence for Continuing Education</p>
</div>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "Upload your programs CSV file",
    type=['csv'],
    help="Upload the credscout_test_data.csv file"
)

if uploaded_file is not None:
    # Load data
    df = load_data(uploaded_file)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Search
    search_term = st.sidebar.text_input(
        "Search",
        placeholder="Search by skill, topic, institution...",
        help="Search across title, institution, skills, and description"
    )
    
    # Credential Type filter
    credential_types = ['All'] + sorted(df['credential_type'].dropna().unique().tolist())
    selected_credential = st.sidebar.selectbox(
        "Credential Type",
        credential_types
    )
    
    # Province filter
    provinces = ['All'] + sorted(df['province'].dropna().unique().tolist())
    selected_province = st.sidebar.selectbox(
        "Province",
        provinces
    )
    
    # Delivery Mode filter
    delivery_modes = ['All'] + sorted(df['delivery_mode'].dropna().unique().tolist())
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
    
    # Clear filters button
    if st.sidebar.button("Clear All Filters"):
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
    if selected_credential != 'All':
        filtered_df = filtered_df[filtered_df['credential_type'] == selected_credential]
    
    # Province filter
    if selected_province != 'All':
        filtered_df = filtered_df[filtered_df['province'] == selected_province]
    
    # Delivery mode filter
    if selected_delivery != 'All':
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
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Programs",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df) - len(df)} from all" if len(filtered_df) < len(df) else None
        )
    
    with col2:
        unique_institutions = filtered_df['institution'].nunique()
        st.metric(
            label="🏛️ Institutions",
            value=unique_institutions
        )
    
    with col3:
        avg_price = filtered_df['price_cad'].mean()
        st.metric(
            label="💰 Average Price",
            value=f"${avg_price:,.0f}"
        )
    
    with col4:
        thirty_days_ago = datetime.now() - timedelta(days=30)
        new_programs = len(filtered_df[filtered_df['date_added'] >= thirty_days_ago])
        st.metric(
            label="🆕 New (30 days)",
            value=new_programs
        )
    
    st.markdown("---")
    
    # Skills Chart
    st.subheader("📈 Top Skills Across All Programs")
    
    # Extract and count skills
    all_skills = []
    for skills_str in filtered_df['skills'].dropna():
        skills_list = [s.strip() for s in str(skills_str).split(',')]
        all_skills.extend(skills_list)
    
    if all_skills:
        skill_counts = Counter(all_skills)
        top_skills = skill_counts.most_common(15)
        
        skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])
        
        fig = px.bar(
            skills_df,
            x='Count',
            y='Skill',
            orientation='h',
            title='',
            color='Count',
            color_continuous_scale='Blues',
            height=500
        )
        fig.update_layout(
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No skills data available for current filters")
    
    st.markdown("---")
    
    # Results counter and export
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**Showing {len(filtered_df)} of {len(df)} programs**")
    
    with col2:
        # Export button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export CSV",
            data=csv,
            file_name=f"credscout_programs_{datetime.now().strftime('%Y-%m-%d')}.csv",
            mime="text/csv"
        )
    
    # Programs table
    st.subheader("📋 Programs")
    
    # Format the dataframe for display
    display_df = filtered_df[[
        'title', 'institution', 'credential_type', 'province', 
        'delivery_mode', 'duration_weeks', 'price_cad', 'skills'
    ]].copy()
    
    display_df.columns = [
        'Title', 'Institution', 'Type', 'Province', 
        'Delivery', 'Duration (weeks)', 'Price (CAD)', 'Skills'
    ]
    
    # Format price with dollar sign
    display_df['Price (CAD)'] = display_df['Price (CAD)'].apply(lambda x: f"${x:,.0f}")
    
    # Show table with clickable titles
    st.dataframe(
        display_df,
        use_container_width=True,
        height=600,
        column_config={
            "Title": st.column_config.TextColumn(
                "Title",
                width="large"
            ),
            "Skills": st.column_config.TextColumn(
                "Skills",
                width="large"
            )
        }
    )
    
    # Expandable program details
    st.markdown("---")
    st.subheader("🔍 View Program Details")
    
    selected_program = st.selectbox(
        "Select a program to view details",
        options=filtered_df['title'].tolist(),
        index=0
    )
    
    if selected_program:
        program = filtered_df[filtered_df['title'] == selected_program].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Institution:** {program['institution']}")
            st.markdown(f"**Type:** {program['credential_type']}")
            st.markdown(f"**Province:** {program['province']}")
            st.markdown(f"**Delivery:** {program['delivery_mode']}")
        
        with col2:
            st.markdown(f"**Duration:** {program['duration_weeks']} weeks")
            st.markdown(f"**Price:** ${program['price_cad']:,.0f}")
            st.markdown(f"**Added:** {program['date_added'].strftime('%Y-%m-%d')}")
            st.markdown(f"**[View Program]({program['program_url']})**")
        
        st.markdown("**Description:**")
        st.write(program['description'])
        
        st.markdown("**Skills:**")
        skills_list = [s.strip() for s in str(program['skills']).split(',')]
        st.write(", ".join([f"`{skill}`" for skill in skills_list]))

else:
    # Instructions when no file is uploaded
    st.info("👆 Upload your CSV file to get started")
    
    st.markdown("""
    ### 📝 Expected CSV Format
    
    Your CSV should include these columns:
    - `program_id` - Unique identifier
    - `title` - Program name
    - `institution` - University/College name
    - `province` - Canadian province
    - `credential_type` - micro-credential, certificate, professional development
    - `delivery_mode` - online, hybrid, in-person
    - `duration_weeks` - Number of weeks
    - `price_cad` - Price in Canadian dollars
    - `skills` - Comma-separated skills (e.g., "Python, Machine Learning, SQL")
    - `description` - Program description
    - `program_url` - Link to program page
    - `date_added` - Date in YYYY-MM-DD format
    
    Use the test data file: `credscout_test_data.csv`
    """)
