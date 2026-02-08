# pages/3_healthcare_revenue.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.calculations import (
    calc_scenario_A_page_3, calc_scenario_B_page_3, 
    compute_kpis_A_page_3, compute_kpis_B_page_3,
    DEFAULT_HEALTHCARE_PARAMS
)

def format_number(value, is_currency=False, is_percentage=False):
    """Format numbers for readability"""
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

def create_tourist_spending_comparison(result_a, result_b, n):
    """Create comparison chart of tourist spending per tourist"""
    
    categories = ['Scenario A\n(Paid VC)', 'Scenario B\n(Free VC)']
    
    # Scenario A spending per tourist
    spending_a = result_a['spending_per_tourist']
    
    # Scenario B spending per tourist
    spending_b = result_b['spending_per_tourist']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=[spending_a, spending_b],
            marker_color=['#1f77b4', '#ff7f0e'],
            text=[format_number(spending_a, is_currency=True), 
                  format_number(spending_b, is_currency=True)],
            textposition='outside',
            width=0.5
        )
    ])
    
    fig.update_layout(
        title="Tourist Spending Comparison (Per Tourist)",
        yaxis_title="Spending (SAR)",
        height=400,
        showlegend=False
    )
    
    return fig

def create_spending_breakdown_chart(result, scenario_name):
    """Create stacked bar chart showing spending breakdown"""
    
    if scenario_name == 'Scenario A':
        categories = ['VC Fees', 'Hospital Visits', 'Hospital Medicine', 'VC Medicine', 'Direct Hospital']
        values = [
            result['vc_spending'],
            result['hospital_visit_spending'],
            result['hospital_medicine_spending'],
            result['vc_medicine_spending'],
            result['direct_hospital_spending']
        ]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    else:  # Scenario B
        # categories = ['Insurance Premium', 'Hospital Visits', 'Hospital Medicine', 'VC Medicine', 'Direct Hospital']
        # categories = [ 'Hospital Visits', 'Hospital Medicine', 'VC Medicine', 'Direct Hospital']
        categories = ['VC Fees', 'Hospital Visits', 
                      'Hospital Medicine', 'VC Medicine', 'Direct Hospital']

        values = [
            # result['insurance_spending'],
            0, 
            result['hospital_visit_spending'],
            result['hospital_medicine_spending'],
            result['vc_medicine_spending'],
            result['direct_hospital_spending']
        ]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[format_number(v, is_currency=True) for v in values],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=f"{scenario_name} - Tourist Spending Breakdown",
        xaxis_title="Spending Category",
        yaxis_title="Total Spending (SAR)",
        height=450,
        xaxis={'tickangle': -45},
        margin=dict(b=120)
    )
    
    return fig

def create_patient_flow_sankey(result, scenario_name):
    """Create Sankey diagram showing patient flow"""
    
    sick_total = result['sick_total']
    vc_calls = result['vc_calls']
    vc_to_hospital = result['vc_to_hospital_patients']
    vc_only = result['vc_only_patients']
    vc_medicine = result['vc_medicine_patients']
    direct_hospital = result['direct_hospital_visits']
    self_care = result.get('self_care_tourists', 0)
    
    labels = [
        'Sick Tourists',
        'Choose VC',
        'Skip VC',
        'VC Only',
        'Get Medicine',
        'VC → Hospital',
        'Direct Hospital',
        'Self-Care'
    ]
    
    source = [0, 0, 1, 1, 2, 2, 3]
    target = [1, 2, 3, 5, 6, 7, 4]
    value = [vc_calls, sick_total - vc_calls, vc_only, vc_to_hospital, direct_hospital, self_care, vc_medicine]
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=['#667eea', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#e377c2', '#bcbd22']
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=['rgba(31, 119, 180, 0.4)', 'rgba(255, 127, 14, 0.4)', 
                   'rgba(44, 160, 68, 0.4)', 'rgba(214, 39, 40, 0.4)', 
                   'rgba(148, 103, 189, 0.4)', 'rgba(227, 119, 194, 0.4)', 'rgba(214, 39, 40, 0.4)']
        )
    )])
    
    fig.update_layout(
        title=f"{scenario_name} - Patient Care Pathway",
        height=450,
        font=dict(size=11)
    )
    
    return fig

def create_spending_per_user_comparison(result_a, result_b):
    """Compare spending per VC user between scenarios"""
    
    fig = go.Figure(data=[
        go.Bar(
            name='Scenario A',
            x=['VC Fee', 'Downstream'],
            y=[result_a['vc_spending'] / result_a['vc_calls'], 
               result_a['downstream_revenue'] / result_a['vc_calls']],
            marker_color='#1f77b4'
        ),
        go.Bar(
            name='Scenario B',
            x=['Insurance', 'Downstream'],
            y=[result_b['insurance_spending'] / result_b['vc_calls'], 
               result_b['downstream_revenue'] / result_b['vc_calls']],
            marker_color='#ff7f0e'
        )
    ])
    
    fig.update_layout(
        title="Average Spending per VC User",
        yaxis_title="Spending (SAR)",
        barmode='group',
        height=400
    )
    
    return fig

def app():
    st.markdown("""
        <style>
        .metric-card {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin: 0.5rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
            <h1 style="color: white; margin: 0;">🏥 Total Tourist Spending Analysis</h1>
            <p style="color: white; opacity: 0.95; margin: 0.5rem 0 0 0;">
                Compare total healthcare spending per tourist across both scenarios
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Global Parameters
    with st.expander("⚙️ **Global Parameters**", expanded=True):
        col1,  col3 = st.columns(2)
        
        with col1:
            n = st.number_input("Total Tourists (N)", min_value=1, value=28130000, 
                              step=1000000, key='n_hc')
            st.caption(f"📊 {n/1_000_000:.1f}M tourists (*based on 2024 tourism data*)")

        with col3:
            vc_cost = st.number_input("VC Delivery Cost (SAR)", min_value=1, value=50, key='vc_cost_hc')
            st.caption(f"💊 SAR {vc_cost} per VC call (*assumed*)")
    
    # Healthcare Parameters - Simplified
    st.markdown("---")
    st.markdown("## 🏥 Healthcare Cost Parameters")
    
    with st.expander("📋 **Configure Healthcare Costs**", expanded=True):
        healthcare_params = DEFAULT_HEALTHCARE_PARAMS.copy()
        
        
        col_hc1, col_hc2 = st.columns(2)
        
        with col_hc1:
            healthcare_params['avg_hospital_visit_cost'] = st.number_input(
                "Average Hospital Visit Cost (SAR)",
                min_value=0,
                value=DEFAULT_HEALTHCARE_PARAMS['avg_hospital_visit_cost'],
                step=10,
                help="Avg cost of Out Patient Visit"
            )
            st.caption("💉 Based on NHA 2023 average outpatient cost, including consultation and routine tests")
            
            healthcare_params['vc_to_hospital_pct'] = st.slider(
                "VC → Hospital Conversion Rate (%)",
                min_value=0,
                max_value=100,
                value=int(DEFAULT_HEALTHCARE_PARAMS['vc_to_hospital_pct'] * 100),
                help="% of VC users who proceed to hospital"
            ) / 100.0
            st.caption(f"🔄 Hospital escalation rate (18%) aligned with global telemedicine post-consultation patterns")

            healthcare_params['vc_medicine_prescription_pct'] = st.slider(
                "VC Medicine Prescription Rate (%)",
                min_value=0,
                max_value=100,
                value=int(DEFAULT_HEALTHCARE_PARAMS['vc_medicine_prescription_pct'] * 100),
                help="% of VC-only patients who get medicine prescription"
            ) / 100.0
            st.caption(f"""💊 {healthcare_params['vc_medicine_prescription_pct']*100:.0f}% of VC patients get medicine
                        \n *(Medication issuance rate follows primary-care prescription probabilities)*""")
            
        
        with col_hc2:
            healthcare_params['avg_medicine_cost'] = st.number_input(
                "Average Medicine Cost (SAR)",
                min_value=0,
                value=DEFAULT_HEALTHCARE_PARAMS['avg_medicine_cost'],
                step=10,
                help="Average prescription cost"
            )
            st.caption("💊 Per prescription Reflects midpoint of evidence-based range (SAR 50–200) from recent cost-of-care studies.")

                    
            healthcare_params['hospital_medicine_utilization'] = st.slider(
                "Hospital Medicine Utilization (%)",
                min_value=0,
                max_value=100,
                value=int(DEFAULT_HEALTHCARE_PARAMS['hospital_medicine_utilization'] * 100),
                help="% of hospital visitors who get medicine"
            ) / 100.0
            st.caption(f"""💊 {healthcare_params['hospital_medicine_utilization']*100:.0f}% of hospital visitors get medicine (*High prescribing likelihood where most OP include medication.*)""")
    
    # Scenario Parameters
    st.markdown("---")
    st.markdown("## 📋 Scenario Parameters")
    
    scenario_col1, scenario_spacer, scenario_col2 = st.columns([10, 1, 10])
    
    with scenario_col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                        padding: 1.5rem; border-radius: 12px; border: 2px solid #2196F3;">
                <h3 style="color: #1976D2; margin: 0;">🔵 Scenario A — Paid VC</h3>
                <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Tourist pays per VC use</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        A_sick = st.slider("Population Seeking Care (%)", 1, 30, 6, key='A_sick_hc') / 100.0
        
        st.caption("Research shows <1% of tourists fall ill (*though our 3-year Lean data indicates ~6%*)")


        A_pct_vc = st.slider("VC Adoption Rate (%)", 0, 100, 13, key='A_vc_hc') / 100.0

        st.caption("Based on research, ~13% of tourists are expected to opt for paid VC")

        A_vc_fee = st.number_input("VC Service Fee (SAR)", min_value=0, value=70, step=5, key='A_fee_hc')

        A_healthcare_params = healthcare_params.copy()  
        A_healthcare_params['non_vc_hospital_seeking_pct']=0.05
        A_healthcare_params['non_vc_hospital_seeking_pct'] = st.slider(
                "Non-VC Hospital-Seeking Rate (%)",
                min_value=0,
                max_value=100,
                value=int(A_healthcare_params['non_vc_hospital_seeking_pct'] * 100),
                help="% of sick tourists who skip VC and go directly to hospital (rest do self-care)"
                ,key='a_helath_'
            ) / 100.0
        st.caption("If VC is paid: ~5% of sick tourists skip VC and go directly to the hospital.")


        
        st.caption(f"📊 {int(n*A_sick):,} sick tourists, {int(n*A_sick*A_pct_vc):,} use VC")
    
    with scenario_col2:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); 
                        padding: 1.5rem; border-radius: 12px; border: 2px solid #FF9800;">
                <h3 style="color: #F57C00; margin: 0;">🟠 Scenario B — Free VC</h3>
                <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0 0 0;">VC included in insurance</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        B_sick = st.slider("Population Seeking Care (%)", 1, 30, 16, key='B_sick_hc') / 100.0

        st.caption("Reported sick: 6% | Free VC may drive higher call volume, including minor issues" )


        B_pct_vc = st.slider("VC Adoption Rate (%)", 0, 100, 75, key='B_vc_hc') / 100.0

        st.caption("Based on research, ~75% of tourists are expected to opt for Free VC")

        st.metric("VC Service Fee (SAR)", format_number(0, is_currency=True))

        b_healthcare_params = healthcare_params.copy()  
        b_healthcare_params['non_vc_hospital_seeking_pct']=0.03
    

        b_healthcare_params['non_vc_hospital_seeking_pct'] = st.slider(
                "Non-VC Hospital-Seeking Rate (%)",
                min_value=0,
                max_value=100,
                value=int(b_healthcare_params['non_vc_hospital_seeking_pct'] * 100),
                help="% of sick tourists who skip VC and go directly to hospital (rest do self-care)"
                ,  key='B_helath_'
            ) / 100.0
        st.caption("If VC is free: ~3% of sick tourists skip VC and go directly to the hospital.")



        st.caption(f"📊 {int(n*B_sick):,} sick tourists, {int(n*B_sick*B_pct_vc):,} use VC")
    
    # Calculate scenarios
    result_a = calc_scenario_A_page_3(n, A_sick, A_pct_vc, A_vc_fee, vc_cost, 
                                healthcare_params=A_healthcare_params)
    premium = 95
    result_b = calc_scenario_B_page_3(n, B_sick, B_pct_vc, premium, vc_cost,
                                healthcare_params=b_healthcare_params, page=3)
    
    kpis_a = compute_kpis_A_page_3(result_a, n)
    kpis_b = compute_kpis_B_page_3(result_b, n, premium)
    
    # Executive Summary
    st.markdown("---")
    st.markdown("## 📈 Tourist Spending Comparison")
    
    summary_cols = st.columns(4)
    
    with summary_cols[0]:
        st.metric(
            "Scenario A: Per Tourist",
            format_number(result_a['spending_per_tourist'], is_currency=True)
        )
    
    with summary_cols[1]:
        st.metric(
            "Scenario B: Per Tourist",
            format_number(result_b['spending_per_tourist'], is_currency=True)
        )
    
    with summary_cols[2]:
        diff = result_a['spending_per_tourist'] - result_b['spending_per_tourist']
        st.metric(
            "Difference",
            format_number(abs(diff), is_currency=True),
            delta="A Higher" if diff > 0 else "B Higher"
        )
    
    with summary_cols[3]:
        st.metric(
            "Total VC Users",
            format_number(result_a['vc_calls'] + result_b['vc_calls']),
            delta=f"{(result_a['vc_calls'] + result_b['vc_calls'])/n*100:.1f}% of tourists"
        )
    
    # Main comparison chart
    st.markdown("<br>", unsafe_allow_html=True)
    fig_comparison = create_tourist_spending_comparison(result_a, result_b, n)
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Spending breakdown
    st.markdown("---")
    st.markdown("## 💰 Spending Breakdown by Category")
    
    breakdown_col1, breakdown_spacer, breakdown_col2 = st.columns([10, 1, 10])
    
    with breakdown_col1:
        st.plotly_chart(create_spending_breakdown_chart(result_a, 'Scenario A'), 
                       use_container_width=True)
    
    with breakdown_col2:
        st.plotly_chart(create_spending_breakdown_chart(result_b, 'Scenario B'), 
                       use_container_width=True)
    
    # Patient flow
    st.markdown("---")
    st.markdown("## 🔄 Patient Care Pathways")
    
    flow_col1, flow_spacer, flow_col2 = st.columns([10, 1, 10])
    
    with flow_col1:
        st.plotly_chart(create_patient_flow_sankey(result_a, 'Scenario A'), 
                       use_container_width=True)
        st.metric("Total Tourist Spending (SAR)", format_number(kpis_a['Total Tourist Spending (SAR)'], is_currency=True))
        st.caption("")
        
        path_col1, path_col2, path_col3 = st.columns(3)
        with path_col1:
            st.metric("VC-Only Patients", format_number(result_a['vc_only_patients']))
            st.metric("Get Medicine", format_number(result_a['vc_medicine_patients']))
        with path_col2:
            st.metric("VC→Hospital", format_number(result_a['vc_to_hospital_patients']))
            st.metric("Direct Hospital", format_number(result_a['direct_hospital_visits']))
        with path_col3:
            st.metric("Self-Care", format_number(result_a.get('self_care_tourists', 0)))
            st.metric("Hospital Rate", format_number(result_a['hospital_conversion_rate'], is_percentage=True))
    
    with flow_col2:
        st.plotly_chart(create_patient_flow_sankey(result_b, 'Scenario B'), 
                       use_container_width=True)
        st.metric("Total Tourist Spending (SAR)", format_number(kpis_b['Total Tourist Spending (SAR)'], is_currency=True))
        st.caption("")
        path_col1, path_col2, path_col3 = st.columns(3)
        with path_col1:
            st.metric("VC-Only Patients", format_number(result_b['vc_only_patients']))
            st.metric("Get Medicine", format_number(result_b['vc_medicine_patients']))
        with path_col2:
            st.metric("VC→Hospital", format_number(result_b['vc_to_hospital_patients']))
            st.metric("Direct Hospital", format_number(result_b['direct_hospital_visits']))
        with path_col3:
            st.metric("Self-Care", format_number(result_b.get('self_care_tourists', 0)))
            st.metric("Hospital Rate", format_number(result_b['hospital_conversion_rate'], is_percentage=True))
    
    # Detailed KPIs
    st.markdown("---")
    st.markdown("## 📊 Detailed Metrics")
    
    tab_comp, tab_a, tab_b  = st.tabs([
        "⚖️ Side-by-Side",
        "🔵 Scenario A Details",
        "🟠 Scenario B Details",
    ])
    
    with tab_a:
        st.markdown("### Tourist Spending Breakdown")

        # st.metric("Sick Population", kpis_a['sick_total'])        
        # st.metric("Direct Hospitals OP", kpis_a['direct_hospital_visits'])
        # st.metric("Virual Calls", kpis_a['vc_calls'])
        # st.metric("Virtual Calls to Hospital", kpis_a['vc_to_hospital_patients'])




        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:
            st.metric("VC Fee Spending", 
                     format_number(kpis_a['VC Fee Spending (SAR)'], is_currency=True))
            st.metric("Hospital Visit Spending", 
                     format_number(kpis_a['Hospital Visit Spending (SAR)'], is_currency=True))
        
        with kpi_col2:
            st.metric("Hospital Medicine", 
                     format_number(kpis_a['Hospital Medicine Spending (SAR)'], is_currency=True))
            st.metric("VC Medicine", 
                     format_number(kpis_a['VC Medicine Spending (SAR)'], is_currency=True))
        
        with kpi_col3:
            st.metric("Direct Hospital", 
                     format_number(kpis_a['Direct Hospital Spending (SAR)'], is_currency=True))
            st.metric("Total Spending", 
                     format_number(kpis_a['Total Tourist Spending (SAR)'], is_currency=True))
        
        st.markdown("### Per-Tourist Metrics")
        
        per_col1, per_col2, per_col3 = st.columns(3)
        
        with per_col1:
            st.metric("Spending per Tourist", 
                     format_number(kpis_a['Spending per Tourist (SAR)'], is_currency=True))
        
        with per_col2:
            st.metric("Spending per Sick Tourist", 
                     format_number(kpis_a['Spending per Sick Tourist (SAR)'], is_currency=True))
        
        with per_col3:
            st.metric("Spending per VC User", 
                     format_number(kpis_a['Spending per VC User (SAR)'], is_currency=True))
    
    with tab_b:
        st.markdown("### Tourist Spending Breakdown")

        st.metric("Sick Population", kpis_b['sick_total'])        
        st.metric("Direct Hospitals OP", kpis_b['direct_hospital_visits'])
        st.metric("Virual Calls", kpis_b['vc_calls'])
        st.metric("Virtual Calls to Hospital", kpis_b['vc_to_hospital_patients'])


        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:

            st.metric("VC Fee Spending", 
                     format_number(0, is_currency=True))
            st.metric("Hospital Visit Spending", 
                     format_number(kpis_b['Hospital Visit Spending (SAR)'], is_currency=True))

            
            # st.metric("Insurance Premium", 
            #          format_number(kpis_b['Insurance Premium Spending (SAR)'], is_currency=True))
            # st.metric("Hospital Visit Spending", 
                    #  format_number(kpis_b['Hospital Visit Spending (SAR)'], is_currency=True))
        
        with kpi_col2:
            st.metric("Hospital Medicine", 
                     format_number(kpis_b['Hospital Medicine Spending (SAR)'], is_currency=True))
            st.metric("VC Medicine", 
                     format_number(kpis_b['VC Medicine Spending (SAR)'], is_currency=True))
        
        with kpi_col3:
            st.metric("Direct Hospital", 
                     format_number(kpis_b['Direct Hospital Spending (SAR)'], is_currency=True))
            st.metric("Total Spending", 
                     format_number(kpis_b['Total Tourist Spending (SAR)'], is_currency=True))
        
        st.markdown("### Per-Tourist Metrics")
        
        per_col1, per_col2, per_col3 = st.columns(3)
        
        with per_col1:
            st.metric("Spending per Tourist", 
                     format_number(kpis_b['Spending per Tourist (SAR)'], is_currency=True))
        
        with per_col2:
            st.metric("Spending per Sick Tourist", 
                     format_number(kpis_b['Spending per Sick Tourist (SAR)'], is_currency=True))
        
        with per_col3:
            st.metric("Spending per VC User", 
                     format_number(kpis_b['Spending per VC User (SAR)'], is_currency=True))
    
    with tab_comp:
        st.markdown("### Side-by-Side Comparison")
        
        comparison_data = {
            'Metric': [
                'Spending per Tourist',
                'Spending per Sick Tourist',
                'Spending per VC User',
                'Total VC Cost',
                'Total VC Fee',
                'Total VC Medicine Revnue',
                'Total VC Hospital Revenue',
                'Total VC Hospital Medicine Revenue',
                'Total Direct Hospital Revenue',
                'Total Tourist Spending',
                'Sick Population', 
                'Direct Hospitals OP', 
                'Virual Calls',
                'Virtual Calls to Hospital', 

            ],
            'Scenario A': [
                format_number(kpis_a['Spending per Tourist (SAR)'], is_currency=True),
                format_number(kpis_a['Spending per Sick Tourist (SAR)'], is_currency=True),
                format_number(kpis_a['Spending per VC User (SAR)'], is_currency=True),
                format_number(kpis_a['VC Cost (SAR)'], is_currency=True),   
                format_number(kpis_a['VC Revenue (SAR)'], is_currency=True),
                format_number(kpis_a['VC Medicine Spending (SAR)'], is_currency=True),
                format_number(kpis_a['Hospital Visit Spending (SAR)'], is_currency=True),
                format_number(kpis_a['Hospital Medicine Spending (SAR)'], is_currency=True),
                format_number(kpis_a['Direct Hospital Spending (SAR)'], is_currency=True),               
                format_number(kpis_a['Total Tourist Spending (SAR)'], is_currency=True),

                kpis_a['sick_total'], 
                kpis_a['direct_hospital_visits'],
                kpis_a['vc_calls'],
                kpis_a['vc_to_hospital_patients'],


                # format_number(kpis_a['VC Penetration Rate (%)'], is_percentage=True),
                # format_number(kpis_a['Hospital Conversion Rate (%)'], is_percentage=True)
            ],
            'Scenario B': [

                format_number(kpis_b['Spending per Tourist (SAR)'], is_currency=True),
                format_number(kpis_b['Spending per Sick Tourist (SAR)'], is_currency=True),
                format_number(kpis_b['Spending per VC User (SAR)'], is_currency=True),
                format_number(kpis_b['VC Cost (SAR)'], is_currency=True),               
                format_number(kpis_b['VC Revenue (SAR)'], is_currency=True),
                format_number(kpis_b['VC Medicine Spending (SAR)'], is_currency=True),
                format_number(kpis_b['Hospital Visit Spending (SAR)'], is_currency=True),
                format_number(kpis_b['Hospital Medicine Spending (SAR)'], is_currency=True),
                format_number(kpis_b['Direct Hospital Spending (SAR)'], is_currency=True),               
                format_number(kpis_b['Total Tourist Spending (SAR)'], is_currency=True),

                kpis_b['sick_total'], 
                kpis_b['direct_hospital_visits'],
                kpis_b['vc_calls'],
                kpis_b['vc_to_hospital_patients'],

                # format_number(kpis_b['VC Penetration Rate (%)'], is_percentage=True),
                # format_number(kpis_b['Hospital Conversion Rate (%)'], is_percentage=True)
            ]
        }
        
        import pandas as pd
        df_comp = pd.DataFrame(comparison_data)
        st.dataframe(df_comp, use_container_width=True, hide_index=True)
        
        # Winner analysis
        st.markdown("### 🏆 Summary")
        
        if result_a['spending_per_tourist'] > result_b['spending_per_tourist']:
            winner = "Scenario A (Paid VC)"
            diff = result_a['spending_per_tourist'] - result_b['spending_per_tourist']
            st.success(f"✅ **{winner}** results in Increases tourist spending by {format_number(diff, is_currency=True)} per tourist")
        else:
            winner = "Scenario B (Free VC)"
            diff = result_b['spending_per_tourist'] - result_a['spending_per_tourist']
            st.success(
                f"""
                ✅ **{winner}** leads to an increase in tourist spending of **{format_number(diff, is_currency=True)} per visitor**.
                
                While offering the VC at no cost drives higher visitor expenditure, it also introduces a **Revenue Loss**.  

                To explore strategies for offsetting the VC cost and understanding the broader financial implications,  
                please proceed to the **VC Cost – What-If Simulator** section.
                """
            )

    
    # Export
    st.markdown("---")
    if st.button("📥 Export Analysis", use_container_width=True):
        export_data = {
            'Metric': list(kpis_a.keys()),
            'Scenario A': [str(v) for v in kpis_a.values()],
            'Scenario B': [str(v) for v in kpis_b.values()]
        }
        
        import pandas as pd
        df_export = pd.DataFrame(export_data)
        csv = df_export.to_csv(index=False)
        
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="tourist_spending_analysis.csv",
            mime="text/csv"
        )