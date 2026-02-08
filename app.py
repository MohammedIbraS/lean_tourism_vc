# # app.py
# import streamlit as st
# from importlib import import_module

# # Page configuration
# st.set_page_config(
#     page_title="Tourism VC Simulator",
#     page_icon="🏝️",
#     layout="wide",
#     initial_sidebar_state="expanded",
#     menu_items={
#         'Get Help': None,
#         'Report a bug': None,
#         'About': "Tourism Virtual Clinic Simulator - Compare business models for VC services"
#     }
# )

# # Custom CSS for better UI/UX
# st.markdown("""
#     <style>
#     /* Main container improvements */
#     .main .block-container {
#         padding-top: 2rem;
#         padding-bottom: 2rem;
#     }
    
#     /* Better header styling */
#     h1 {
#         color: #1f77b4;
#         border-bottom: 3px solid #1f77b4;
#         padding-bottom: 0.5rem;
#         margin-bottom: 1rem;
#     }
    
#     /* Sidebar improvements */
#     .css-1d391kg {
#         padding-top: 2rem;
#     }
    
#     /* Better button styling */
#     .stButton > button {
#         width: 100%;
#         border-radius: 8px;
#         font-weight: 600;
#         transition: all 0.3s ease;
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 4px 8px rgba(0,0,0,0.2);
#     }
    
#     /* Better metric cards */
#     [data-testid="stMetricValue"] {
#         font-size: 1.5rem;
#     }
    
#     /* Better tabs */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 8px;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         border-radius: 8px 8px 0 0;
#         padding: 10px 20px;
#         font-weight: 600;
#     }
    
#     /* Info boxes */
#     .info-box {
#         background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
#         padding: 1.5rem;
#         border-radius: 10px;
#         border-left: 5px solid #2196F3;
#         margin: 1rem 0;
#     }
    
#     /* Welcome banner */
#     .welcome-banner {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 2rem;
#         border-radius: 15px;
#         margin-bottom: 2rem;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#     }
    
#     /* Tooltip improvements */
#     .tooltip-icon {
#         display: inline-block;
#         width: 18px;
#         height: 18px;
#         border-radius: 50%;
#         background: #2196F3;
#         color: white;
#         text-align: center;
#         line-height: 18px;
#         font-size: 12px;
#         margin-left: 5px;
#         cursor: help;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Sidebar navigation and info
# with st.sidebar:
#     st.markdown("""
#         <div style="text-align: center; padding: 1rem 0;">
#             <h2 style="color: #1f77b4; margin-bottom: 0.5rem;">🏝️ VC Simulator</h2>
#             <p style="color: #666; font-size: 0.9rem;">Tourism Insurance + Virtual Clinic</p>
#         </div>
#     """, unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     st.markdown("### 📚 Navigation")
#     page = st.radio(
#         "Choose a page:",
#         ["📊 Sensitivity Analysis", "🎯 What-If Simulator"],
#         label_visibility="collapsed"
#     )
    
#     st.markdown("---")
    
#     with st.expander("ℹ️ About This App", expanded=False):
#         st.markdown("""
#         **Tourism Virtual Clinic Simulator**
        
#         Compare two business models for Virtual Clinic services:
        
#         - **Scenario A**: Paid VC (tourists pay per consultation)
#         - **Scenario B**: Free VC (included in insurance premium)
        
#         Use the **Sensitivity Analysis** page to explore parameter ranges and break-even points.
        
#         Use the **What-If Simulator** to test specific scenarios and get detailed KPIs.
#         """)
    
#     st.markdown("---")
    
#     st.markdown("### 💡 Quick Tips")
#     st.info("""
#     - Start with **Sensitivity Analysis** to understand parameter impacts
#     - Use **What-If Simulator** for specific scenario testing
#     - Adjust global parameters first, then scenario-specific ones
#     - Look for break-even points to optimize pricing
#     """)

# # Welcome banner
# st.markdown("""
#     <div class="welcome-banner">
#         <h1 style="color: white; border: none; padding: 0; margin: 0 0 0.5rem 0;">🏝️ Tourism Insurance + Virtual Clinic Simulator</h1>
#         <p style="font-size: 1.1rem; margin: 0; opacity: 0.95;">
#             Strategic decision support tool for comparing Virtual Clinic business models. 
#             Analyze profitability, identify break-even points, and optimize your strategy.
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# # Page routing
# if page == "📊 Sensitivity Analysis" or page == "":
#     with st.spinner("Loading Sensitivity Analysis..."):
#         module = import_module("1_comparison")
#         module.app()
# else:
#     with st.spinner("Loading What-If Simulator..."):
#         module = import_module("2_whatif")
#         module.app()



# # # Simple navigation
# # pages = {
# #     "Comparison (Landing)": "pages.1_comparison",
# #     "What-If Simulator": "pages.2_whatif"
# # }

# # choice = st.sidebar.selectbox("Choose page", list(pages.keys()))

# # module = import_module(pages[choice])


# app.py
import streamlit as st
from importlib import import_module

# Page configuration
st.set_page_config(
    page_title="Tourism VC Simulator",
    page_icon="🏖️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Tourism Virtual Clinic Simulator - Compare business models for VC services"
    }
)

# Custom CSS for better UI/UX
st.markdown("""
    <style>
    /* Main container improvements */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Better header styling */
    h1 {
        color: #1f77b4;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Sidebar improvements */
    .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* Better button styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Better metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }
    
    /* Better tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
    }
    
    /* Welcome banner */
    .welcome-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Tooltip improvements */
    .tooltip-icon {
        display: inline-block;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: #2196F3;
        color: white;
        text-align: center;
        line-height: 18px;
        font-size: 12px;
        margin-left: 5px;
        cursor: help;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation and info
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="color: #1f77b4; margin-bottom: 0.5rem;">🏖️ VC Simulator</h2>
            <p style="color: #666; font-size: 0.9rem;">Tourism Insurance + Virtual Clinic</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📚 Navigation")
    page = st.radio(
        "Choose a page:",
        ["🏥 Healthcare Revenue", "🎯 VC Cost - What-If Simulator", "📊 VC Cost - Sensitivity Analysis" ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    with st.expander("ℹ️ About This App", expanded=False):
        st.markdown("""
        **Tourism Virtual Clinic Simulator**
        
        Compare two business models for Virtual Clinic services:
        
        - **Scenario A**: Paid VC (tourists pay per consultation)
        - **Scenario B**: Free VC (included in insurance premium)
        
        **Pages:**
        - **Sensitivity Analysis**: Explore parameter ranges and break-even points
        - **What-If Simulator**: Test specific scenarios and get detailed KPIs
        - **Healthcare Revenue**: Analyze total revenue including downstream services
        """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Quick Tips")
    st.info("""
    - Start with **Sensitivity Analysis** to understand parameter impacts
    - Use **What-If Simulator** for specific scenario testing
    - Check **Healthcare Revenue** for complete revenue modeling
    - Adjust global parameters first, then scenario-specific ones
    """)

# Welcome banner
st.markdown("""
    <div class="welcome-banner">
        <h1 style="color: white; border: none; padding: 0; margin: 0 0 0.5rem 0;">🏖️ Tourism Insurance + Virtual Clinic Simulator</h1>
        <p style="font-size: 1.1rem; margin: 0; opacity: 0.95;">
            Strategic decision support tool for comparing Virtual Clinic business models. 
            Analyze profitability, identify break-even points, and optimize your strategy.
        </p>
    </div>
""", unsafe_allow_html=True)

# Page routing
if page == "📊 VC Cost - Sensitivity Analysis" or page == "":
    with st.spinner("Loading Sensitivity Analysis..."):
        module = import_module("1_comparison")
        module.app()
elif page == "🎯 VC Cost - What-If Simulator":
    with st.spinner("Loading What-If Simulator..."):
        module = import_module("2_whatif")
        module.app()
else:  # Healthcare Revenue
    with st.spinner("Loading Healthcare Revenue Analysis..."):
        module = import_module("3_healthcare_revenue")
        module.app()