# # pages/2_whatif.py
# import streamlit as st
# from utils.calculations import calc_scenario_A, calc_scenario_B, compute_kpis_A, compute_kpis_B

# def app():
#     st.header("What-If Simulator — Detailed KPIs")
#     st.markdown("Enter specific parameters for Scenario A and Scenario B to compare full breakdowns.")

#     n = st.number_input("Total tourists (N)", min_value=1, value=28130000, step=1000, key='nB')
#     premium = st.number_input("Premium (SAR)", min_value=0, value=95)
#     vc_cost = st.number_input("VC Cost (SAR)", min_value=0, value=70)


#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Scenario A — Paid VC inputs")
#         A_sick = st.number_input("A: % Sick population", min_value=0, max_value=100, value=6) / 100.0
#         A_pct_vc = st.number_input("A: % VC uptake (paid)", min_value=0, max_value=100, value=30) / 100.0
#         A_vc_fee = st.number_input("A: VC Fee (SAR)", min_value=0, value=70, step=5)
#         resA = calc_scenario_A(n, A_sick, A_pct_vc, A_vc_fee, vc_cost)
#         kpisA = compute_kpis_A(resA, n)

#         st.write("### Scenario A Results")
#         for k, v in kpisA.items():
#             # format percentages and floats
#             if isinstance(v, float):
#                 try:
#                     st.metric(k, f"{v:,.2f}")
#                 except:
#                     st.metric(k, f"{v}")
#             else:
#                 st.metric(k, f"{v:,}" if isinstance(v, (int)) else str(v))

#     with col2:
#         st.subheader("Scenario B — Free VC inputs")

#         B_sick = st.number_input("B: % Sick population", min_value=0, max_value=100, value=16) / 100.0
#         B_pct_vc = st.number_input("B: % VC uptake (free)", min_value=0, max_value=100, value=80) / 100.0
#         B_emerg = st.number_input("B: Emergency premium (SAR)", min_value=0, step=5, max_value=premium-5 if premium>5 else 0, value=50)
#         resB = calc_scenario_B(n, premium, B_emerg, B_sick, B_pct_vc, vc_cost)
#         kpisB = compute_kpis_B(resB, n, premium)

#         st.write("### Scenario B Results")
#         for k, v in kpisB.items():
#             if isinstance(v, float):
#                 try:
#                     st.metric(k, f"{v:,.2f}")
#                 except:
#                     st.metric(k, f"{v}")
#             else:
#                 st.metric(k, f"{v:,}" if isinstance(v, (int)) else str(v))

#     st.markdown('---')
#     st.write('Recommendation:')
#     if kpisA['Net Profit (SAR)'] > kpisB['Net Profit (SAR)']:
#         st.success('Scenario A (Paid VC) yields higher net profit for these inputs.')
#     elif kpisB['Net Profit (SAR)'] > kpisA['Net Profit (SAR)']:
#         st.success('Scenario B (Free VC) yields higher net profit for these inputs.')
#     else:
#         st.info('Both scenarios yield similar net profit for these inputs.')

# pages/2_whatif.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.calculations import calc_scenario_A, calc_scenario_B, compute_kpis_A, compute_kpis_B
from utils import scenario_manager
import pandas as pd

def format_number(value, is_currency=False, is_percentage=False):
    """Format numbers for C-suite readability: K, M, B notation"""
    if value is None or (isinstance(value, str) and value == 'n/a'):
        return 'n/a'
    
    if is_percentage:
        return f"{value:.1f}%"
    
    prefix = "SAR " if is_currency else ""
    
    if abs(value) >= 1_000_000_000:
        return f"{prefix}{value/1_000_000_000:.2f}B"
    elif abs(value) >= 1_000_000:
        return f"{prefix}{value/1_000_000:.2f}M"
    elif abs(value) >= 10_000:
        return f"{prefix}{value/1_000:.1f}K"
    else:
        return f"{prefix}{value:,.0f}"

def create_comparison_chart(kpisA, kpisB, metric_name, title):
    """Create a bar chart comparing scenarios"""
    fig = go.Figure(data=[
        go.Bar(name='Scenario A (Paid VC)', 
               x=[metric_name], 
               y=[kpisA[metric_name]], 
               marker_color='#1f77b4',
               text=[format_number(kpisA[metric_name], is_currency=True)],
               textposition='outside',
               width=0.4),
        go.Bar(name='Scenario B (Free VC)', 
               x=[metric_name], 
               y=[kpisB[metric_name]], 
               marker_color='#ff7f0e',
               text=[format_number(kpisB[metric_name], is_currency=True)],
               textposition='outside',
               width=0.4)
    ])
    fig.update_layout(
        title=title,
        showlegend=True,
        height=450,
        margin=dict(t=60, b=60, l=80, r=80),
        autosize=True,
        yaxis=dict(
            automargin=True,
            fixedrange=False
        ),
        xaxis=dict(
            automargin=True,
            range=[-0.6, 0.6]
        ),
        bargap=0.3
    )
    return fig

def create_waterfall_chart(scenario_name, revenue, costs_breakdown, net_profit):
    """Create waterfall chart showing revenue to profit breakdown"""
    labels = ['Revenue'] + list(costs_breakdown.keys()) + ['Net Profit']
    values = [revenue] + [-v for v in costs_breakdown.values()] + [net_profit]
    
    fig = go.Figure(go.Waterfall(
        name=scenario_name,
        orientation="v",
        measure=["relative"] * len(values),
        x=labels,
        y=values,
        text=[format_number(v, is_currency=True) for v in values],
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    
    fig.update_layout(
        title=f"{scenario_name} - Revenue to Profit",
        showlegend=False,
        height=500,
        margin=dict(t=60, b=80, l=100, r=60),
        autosize=True,
        yaxis=dict(
            automargin=True,
            fixedrange=False
        ),
        xaxis=dict(
            automargin=True,
            tickangle=-45
        )
    )
    return fig

def app():
    # Page config and CSS styling
    st.markdown("""
        <style>
        .big-metric { font-size: 2rem; font-weight: bold; }
        .executive-summary { 
            background-color: #f0f2f6; 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 20px;
        }
        .recommendation-box {
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .scenario-card-a {
            background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 2px solid #2196F3;
            margin: 10px;
        }
        .scenario-card-b {
            background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 2px solid #FF9800;
            margin: 10px;
        }
        .scenario-header {
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(0,0,0,0.1);
        }
        .input-section {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 1px solid #e0e0e0;
        }
        .result-highlight {
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #4caf50;
            margin: 0.5rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Page header with better description
    st.markdown("""
        <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
            <h1 style="color: #1f77b4; margin-bottom: 0.5rem;">📊 What-If Scenario Simulator</h1>
            <p style="color: #555; font-size: 1rem; margin: 0;">
                Test specific parameter combinations and get detailed KPIs for both scenarios. 
                Perfect for comparing concrete business cases and making strategic decisions.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Input Section with collapsible
    with st.expander("⚙️ **Global Parameters** (Click to adjust)", expanded=True):
        st.markdown("""
            <div class="help-text" style="margin-bottom: 1rem;">
                💡 These parameters apply to both scenarios. Adjust them to match your business context.
            </div>
        """, unsafe_allow_html=True)
        
        col_input1, col_input2, col_input3 = st.columns(3)
        with col_input1:
            n = st.number_input(
                "Total Tourists (N)", 
                min_value=1, 
                value=28130000, 
                step=1000000, 
                key='nB',
                help="Total number of tourists expected in the analysis period"
            )
            st.caption(f"📊 {n/1_000_000:.1f}M tourists")
        with col_input2:
            premium = st.number_input(
                "Insurance Premium (SAR)", 
                min_value=0, 
                value=95,
                help="Base insurance premium charged per tourist"
            )
            st.caption(f"💰 SAR {premium} per tourist")
        with col_input3:
            vc_cost = st.number_input(
                "VC Delivery Cost (SAR)", 
                min_value=0, 
                value=50,
                help="Cost to deliver one virtual consultation"
            )
            st.caption(f"💊 SAR {vc_cost} per VC call")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Scenario Inputs with enhanced styling and better organization
    st.markdown("""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <h3 style="color: #1f77b4; margin-bottom: 0.5rem;">📝 Scenario Parameters</h3>
            <p style="color: #666; margin: 0; font-size: 0.95rem;">
                Enter specific parameter values for each scenario. Results will update automatically.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col_spacer, col2 = st.columns([10, 1, 10])

    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                        padding: 1.5rem; border-radius: 12px; border: 2px solid #2196F3; margin: 1rem 0;">
                <h3 style="color: #1976D2; margin-bottom: 0.5rem;">🔵 Scenario A — Paid VC</h3>
                <p style="color: #666; font-style: italic; margin-top: -5px; margin-bottom: 1rem;">
                    Tourists pay separately for VC services. Revenue scales with adoption.
                </p>
        """, unsafe_allow_html=True)
        
        A_sick = st.slider(
            "Population Seeking Care (%)", 
            min_value=0, 
            max_value=100, 
            value=6, 
            key='A_sick',
            help="What percentage of tourists need medical care?"
        ) / 100.0
        st.caption(f"📊 {A_sick*100:.1f}% of tourists ({int(n*A_sick):,} people)")
        
        A_pct_vc = st.slider(
            "VC Adoption Rate (%)", 
            min_value=0, 
            max_value=100, 
            value=30, 
            key='A_vc',
            help="What percentage of sick tourists choose VC over in-person visits?"
        ) / 100.0
        st.caption(f"💊 {A_pct_vc*100:.1f}% adoption ({int(n*A_sick*A_pct_vc):,} VC calls)")
        
        A_vc_fee = st.number_input(
            "VC Service Fee (SAR)", 
            min_value=0, 
            value=70, 
            step=5, 
            key='A_fee',
            help="Price charged per virtual consultation"
        )
        st.caption(f"💰 SAR {A_vc_fee} per consultation")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); 
                        padding: 1.5rem; border-radius: 12px; border: 2px solid #FF9800; margin: 1rem 0;">
                <h3 style="color: #F57C00; margin-bottom: 0.5rem;">🟠 Scenario B — Free VC</h3>
                <p style="color: #666; font-style: italic; margin-top: -5px; margin-bottom: 1rem;">
                    VC included in insurance premium. Fixed revenue model.
                </p>
        """, unsafe_allow_html=True)
        
        B_sick = st.slider(
            "Population Seeking Care (%)", 
            min_value=0, 
            max_value=100, 
            value=16, 
            key='B_sick',
            help="What percentage of tourists need medical care?"
        ) / 100.0
        st.caption(f"📊 {B_sick*100:.1f}% of tourists ({int(n*B_sick):,} people)")
        
        B_pct_vc = st.slider(
            "VC Adoption Rate (%)", 
            min_value=0, 
            max_value=100, 
            value=80, 
            key='B_vc',
            help="What percentage of sick tourists choose VC over in-person visits?"
        ) / 100.0
        st.caption(f"💊 {B_pct_vc*100:.1f}% adoption ({int(n*B_sick*B_pct_vc):,} VC calls)")
        
        B_emerg = st.number_input(
            "Emergency Insurance Cost (SAR)", 
            min_value=0, 
            max_value=premium-5 if premium>5 else 0, 
            value=50, 
            step=5, 
            key='B_emerg',
            help="Cost per tourist for emergency insurance coverage"
        )
        st.caption(f"🚨 SAR {B_emerg} per tourist (max: SAR {premium-5 if premium>5 else 0})")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Calculate scenarios
    resA = calc_scenario_A(n, A_sick, A_pct_vc, A_vc_fee, vc_cost)
    kpisA = compute_kpis_A(resA, n)
    
    resB = calc_scenario_B(n, premium, B_emerg, B_sick, B_pct_vc, vc_cost)
    kpisB = compute_kpis_B(resB, n, premium)

    # Executive Summary with better visual design
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
            <h2 style="color: white; margin-bottom: 0.5rem;">📈 Executive Summary</h2>
            <p style="color: white; opacity: 0.95; margin: 0; font-size: 0.95rem;">
                Quick overview of key financial metrics comparing both scenarios
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    profit_diff = kpisA['Net Profit (SAR)'] - kpisB['Net Profit (SAR)']
    profit_diff_pct = (profit_diff / kpisB['Net Profit (SAR)'] * 100) if kpisB['Net Profit (SAR)'] != 0 else 0
    
    summary_cols = st.columns(4)
    
    with summary_cols[0]:
        st.markdown("""
            <div style="background: #E3F2FD; padding: 1rem; border-radius: 8px; border-left: 4px solid #2196F3;">
                <p style="color: #666; font-size: 0.85rem; margin: 0 0 0.5rem 0;">Scenario A Profit</p>
        """, unsafe_allow_html=True)
        st.metric(
            "",
            format_number(kpisA['Net Profit (SAR)'], is_currency=True),
            delta=f"{format_number(profit_diff, is_currency=True)} vs B" if profit_diff != 0 else None,
            delta_color="normal" if profit_diff >= 0 else "inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with summary_cols[1]:
        st.markdown("""
            <div style="background: #FFF3E0; padding: 1rem; border-radius: 8px; border-left: 4px solid #FF9800;">
                <p style="color: #666; font-size: 0.85rem; margin: 0 0 0.5rem 0;">Scenario B Profit</p>
        """, unsafe_allow_html=True)
        st.metric(
            "",
            format_number(kpisB['Net Profit (SAR)'], is_currency=True),
            delta=f"{format_number(-profit_diff, is_currency=True)} vs A" if profit_diff != 0 else None,
            delta_color="normal" if profit_diff <= 0 else "inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with summary_cols[2]:
        margin_a = kpisA['Profit Margin'] if isinstance(kpisA['Profit Margin'], (int, float)) else 0
        margin_b = kpisB['Profit Margin'] if isinstance(kpisB['Profit Margin'], (int, float)) else 0
        st.markdown("""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea;">
                <p style="color: #666; font-size: 0.85rem; margin: 0 0 0.5rem 0;">Best Margin</p>
        """, unsafe_allow_html=True)
        st.metric(
            "",
            format_number(max(margin_a, margin_b), is_percentage=True),
            delta=f"{'Scenario A' if margin_a > margin_b else 'Scenario B'}"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with summary_cols[3]:
        total_vc_calls = kpisA['VC Calls'] + kpisB['VC Calls']
        st.markdown("""
            <div style="background: #e8f5e9; padding: 1rem; border-radius: 8px; border-left: 4px solid #4caf50;">
                <p style="color: #666; font-size: 0.85rem; margin: 0 0 0.5rem 0;">Total VC Volume</p>
        """, unsafe_allow_html=True)
        st.metric(
            "",
            format_number(total_vc_calls),
            delta=f"{(total_vc_calls/n*100):.1f}% of tourists"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Key Insights with better visual design
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("## 💡 Key Insights & Recommendations")
    
    insights_col1, insights_col2 = st.columns(2, gap="large")
    
    with insights_col1:
        if profit_diff > 0:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%); 
                            padding: 1.5rem; border-radius: 10px; border: 2px solid #4caf50; margin: 1rem 0;">
                    <h4 style="color: #2e7d32; margin-bottom: 0.5rem;">✅ Scenario A (Paid VC) Recommended</h4>
            """, unsafe_allow_html=True)
            st.success(f"""
            **Financial Advantage:**
            - Higher net profit by {format_number(profit_diff, is_currency=True)} ({profit_diff_pct:+.1f}%)
            - Profit margin: {format_number(margin_a, is_percentage=True)}
            - Revenue per tourist: {format_number(kpisA['Revenue per tourist (SAR)'], is_currency=True)}
            """)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background: #E3F2FD; padding: 1.5rem; border-radius: 10px; border: 2px solid #2196F3; margin: 1rem 0;">
                    <h4 style="color: #1976D2; margin-bottom: 0.5rem;">🔵 Scenario A (Paid VC) Performance</h4>
            """, unsafe_allow_html=True)
            st.info(f"""
            **Metrics:**
            - Net profit: {format_number(kpisA['Net Profit (SAR)'], is_currency=True)}
            - Profit margin: {format_number(margin_a, is_percentage=True)}
            - Revenue per tourist: {format_number(kpisA['Revenue per tourist (SAR)'], is_currency=True)}
            """)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with insights_col2:
        if profit_diff < 0:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #ffe0b2 0%, #ffcc80 100%); 
                            padding: 1.5rem; border-radius: 10px; border: 2px solid #ff9800; margin: 1rem 0;">
                    <h4 style="color: #e65100; margin-bottom: 0.5rem;">✅ Scenario B (Free VC) Recommended</h4>
            """, unsafe_allow_html=True)
            st.success(f"""
            **Financial Advantage:**
            - Higher net profit by {format_number(abs(profit_diff), is_currency=True)} ({abs(profit_diff_pct):+.1f}%)
            - Profit margin: {format_number(margin_b, is_percentage=True)}
            - Revenue per tourist: {format_number(kpisB['Revenue per tourist (SAR)'], is_currency=True)}
            """)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background: #FFF3E0; padding: 1.5rem; border-radius: 10px; border: 2px solid #FF9800; margin: 1rem 0;">
                    <h4 style="color: #F57C00; margin-bottom: 0.5rem;">🟠 Scenario B (Free VC) Performance</h4>
            """, unsafe_allow_html=True)
            st.info(f"""
            **Metrics:**
            - Net profit: {format_number(kpisB['Net Profit (SAR)'], is_currency=True)}
            - Profit margin: {format_number(margin_b, is_percentage=True)}
            - Revenue per tourist: {format_number(kpisB['Revenue per tourist (SAR)'], is_currency=True)}
            """)
            st.markdown("</div>", unsafe_allow_html=True)

    # Visual Comparisons
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 📊 Financial Comparison")
    
    chart_col1, chart_spacer, chart_col2 = st.columns([10, 1, 10])
    
    with chart_col1:
        # Revenue comparison
        fig_revenue = create_comparison_chart(kpisA, kpisB, 'Revenue (SAR)', 'Revenue Comparison')
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with chart_col2:
        # Profit comparison
        fig_profit = create_comparison_chart(kpisA, kpisB, 'Net Profit (SAR)', 'Net Profit Comparison')
        st.plotly_chart(fig_profit, use_container_width=True)


    # Waterfall charts
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Revenue to Profit Breakdown")
    waterfall_col1, waterfall_spacer, waterfall_col2 = st.columns([10, 1, 10])
    
    with waterfall_col1:
        costs_a = {'VC Costs': kpisA['VC Cost (SAR)']}
        fig_waterfall_a = create_waterfall_chart('Scenario A', kpisA['Revenue (SAR)'], 
                                                  costs_a, kpisA['Net Profit (SAR)'])
        st.plotly_chart(fig_waterfall_a, use_container_width=True)
    
    with waterfall_col2:
        costs_b = {
            'VC Costs': kpisB['VC Cost (SAR)'],
            'Emergency Costs': kpisB['Emergency Cost (SAR)']
        }
        fig_waterfall_b = create_waterfall_chart('Scenario B', kpisB['Revenue (SAR)'], 
                                                  costs_b, kpisB['Net Profit (SAR)'])
        st.plotly_chart(fig_waterfall_b, use_container_width=True)

    # Detailed KPIs with collapsible sections
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    detail_col1, detail_spacer, detail_col2 = st.columns([10, 1, 10])

    with detail_col1:
        with st.expander("🔵 **Scenario A — Detailed Metrics** (Click to expand)", expanded=False):
            st.markdown("""
                <div style="background: #E3F2FD; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                    <p style="color: #1976D2; margin: 0; font-weight: 600;">Complete financial breakdown for Scenario A</p>
                </div>
            """, unsafe_allow_html=True)
            
            for k, v in kpisA.items():
                if k == 'Profit Margin':
                    st.metric(k, format_number(v, is_percentage=True) if isinstance(v, (int, float)) else v)
                elif 'SAR' in k:
                    st.metric(k, format_number(v, is_currency=True) if isinstance(v, (int, float)) else v)
                else:
                    st.metric(k, format_number(v) if isinstance(v, (int, float)) else v)

    with detail_col2:
        with st.expander("🟠 **Scenario B — Detailed Metrics** (Click to expand)", expanded=False):
            st.markdown("""
                <div style="background: #FFF3E0; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                    <p style="color: #F57C00; margin: 0; font-weight: 600;">Complete financial breakdown for Scenario B</p>
                </div>
            """, unsafe_allow_html=True)
            
            for k, v in kpisB.items():
                if k == 'Profit Margin':
                    st.metric(k, format_number(v, is_percentage=True) if isinstance(v, (int, float)) else v)
                elif 'SAR' in k:
                    st.metric(k, format_number(v, is_currency=True) if isinstance(v, (int, float)) else v)
                else:
                    st.metric(k, format_number(v) if isinstance(v, (int, float)) else v)

    # Operational Insights
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 🎯 Operational Insights")
    
    op_col1, op_col2, op_col3 = st.columns(3)
    
    with op_col1:
        st.markdown("**VC Utilization**")
        vc_a_rate = (kpisA['VC Calls'] / n * 100) if n > 0 else 0
        vc_b_rate = (kpisB['VC Calls'] / n * 100) if n > 0 else 0
        st.metric("Scenario A", f"{vc_a_rate:.2f}%")
        st.metric("Scenario B", f"{vc_b_rate:.2f}%")
    
    with op_col2:
        st.markdown("**Cost Efficiency**")
        cost_per_call_a = kpisA['VC Cost (SAR)'] / kpisA['VC Calls'] if kpisA['VC Calls'] > 0 else 0
        cost_per_call_b = kpisB['VC Cost (SAR)'] / kpisB['VC Calls'] if kpisB['VC Calls'] > 0 else 0
        st.metric("Scenario A", format_number(cost_per_call_a, is_currency=True))
        st.metric("Scenario B", format_number(cost_per_call_b, is_currency=True))
    
    with op_col3:
        st.markdown("**Profit per Tourist**")
        profit_per_tourist_a = kpisA['Net Profit (SAR)'] / n
        profit_per_tourist_b = kpisB['Net Profit (SAR)'] / n
        st.metric("Scenario A", format_number(profit_per_tourist_a, is_currency=True))
        st.metric("Scenario B", format_number(profit_per_tourist_b, is_currency=True))

    # Strategic Recommendations
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 🎯 Strategic Recommendations")
    
    if abs(profit_diff) / max(abs(kpisA['Net Profit (SAR)']), abs(kpisB['Net Profit (SAR)'])) < 0.05:
        st.warning("⚠️ **Close Decision**: Profit difference is less than 5%. Consider non-financial factors such as customer satisfaction, operational complexity, and strategic alignment.")
    
    if kpisA['Net Profit (SAR)'] > kpisB['Net Profit (SAR)']:
        st.success(f"""
        ### ✅ Recommend: Scenario A (Paid VC Model)
        
        **Financial Advantage**: {format_number(profit_diff, is_currency=True)} ({profit_diff_pct:+.1f}%)
        
        **Key Considerations**:
        - Lower operational complexity (pay-per-use model)
        - Revenue scales with VC adoption
        - Break-even VC fee: {format_number(kpisA.get('Break-even VC fee (SAR)', 0), is_currency=True)}
        - Suitable if VC adoption can be maintained at {A_pct_vc*100:.0f}%
        """)
    else:
        st.success(f"""
        ### ✅ Recommend: Scenario B (Free VC Model)
        
        **Financial Advantage**: {format_number(abs(profit_diff), is_currency=True)} ({abs(profit_diff_pct):+.1f}%)
        
        **Key Considerations**:
        - Higher customer value proposition (included service)
        - Predictable revenue model (premium-based)
        - Better for customer satisfaction and loyalty
        - Pool per tourist: {format_number(kpisB.get('Pool per tourist (SAR)', 0), is_currency=True)} available for services
        """)

    # ============= SAVE/LOAD FUNCTIONALITY =============
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## Save & Load Scenarios")
    
    save_col1, save_col2 = st.columns(2)
    
    with save_col1:
        st.markdown("### 💾 Save Current Scenario")
        scenario_name = st.text_input(
            "Scenario Name", 
            value=f"whatif_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}",
            key='save_whatif_name'
        )
        
        if st.button("💾 Save Scenario", use_container_width=True, key='save_whatif_btn'):
            config = scenario_manager.create_scenario_config(
                global_params={'n': n, 'premium': premium, 'vc_cost': vc_cost},
                scenario_a_params={'sick': A_sick, 'vc_uptake': A_pct_vc, 'vc_fee': A_vc_fee},
                scenario_b_params={'sick': B_sick, 'vc_uptake': B_pct_vc, 'emergency': B_emerg}
            )
            saved_name = scenario_manager.save_scenario_config(config, scenario_name)
            st.success(f"✅ Scenario '{saved_name}' saved successfully!")
        
        # Export to JSON
        if st.button("📤 Export to JSON", use_container_width=True, key='export_whatif_json'):
            config = scenario_manager.create_scenario_config(
                global_params={'n': n, 'premium': premium, 'vc_cost': vc_cost},
                scenario_a_params={'sick': A_sick, 'vc_uptake': A_pct_vc, 'vc_fee': A_vc_fee},
                scenario_b_params={'sick': B_sick, 'vc_uptake': B_pct_vc, 'emergency': B_emerg}
            )
            json_str = scenario_manager.export_scenario_to_json(config, scenario_name)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"{scenario_name}.json",
                mime="application/json",
                key='download_whatif_json'
            )
    
    with save_col2:
        st.markdown("### 📂 Load Saved Scenario")
        saved_scenarios = scenario_manager.get_saved_scenarios()
        
        if saved_scenarios:
            scenario_list = list(saved_scenarios.keys())
            selected_scenario = st.selectbox(
                "Select a saved scenario:",
                scenario_list,
                key='load_whatif_select'
            )
            
            if st.button("📂 Load Scenario", use_container_width=True, key='load_whatif_btn'):
                config = scenario_manager.load_scenario_config(selected_scenario)
                if config:
                    st.success(f"✅ Scenario '{selected_scenario}' loaded! Parameters shown below.")
                    st.json(config)
                    st.info("💡 Note: Adjust the inputs above to apply the loaded scenario values.")
            
            if st.button("🗑️ Delete Scenario", use_container_width=True, key='delete_whatif_btn'):
                if scenario_manager.delete_scenario(selected_scenario):
                    st.success(f"✅ Scenario '{selected_scenario}' deleted!")
                    st.rerun()
        else:
            st.info("No saved scenarios yet. Save a scenario to load it later.")
        
        # Import from JSON
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📥 Import from JSON")
        uploaded_file = st.file_uploader("Upload JSON file", type=['json'], key='import_whatif_json')
        if uploaded_file is not None:
            json_str = uploaded_file.read().decode('utf-8')
            config, imported_name = scenario_manager.import_scenario_from_json(json_str)
            if config:
                st.success(f"✅ Scenario '{imported_name}' imported successfully!")
                st.json(config)
            else:
                st.error("❌ Invalid JSON file. Please check the format.")

    # Download data
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## 📥 Export Analysis Data")
    if st.button("📥 Export Analysis to CSV", use_container_width=True):
        comparison_df = pd.DataFrame({
            'Metric': list(kpisA.keys()),
            'Scenario A': [str(v) for v in kpisA.values()],
            'Scenario B': [str(v) for v in kpisB.values()]
        })
        csv = comparison_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="scenario_comparison.csv",
            mime="text/csv"
        )