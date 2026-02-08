# utils/calculations.py
import math
import streamlit as st

# Simplified healthcare service parameters
DEFAULT_HEALTHCARE_PARAMS = {
    'vc_to_hospital_pct': 0.25,  # 25% of VC users proceed to hospital
    'avg_hospital_visit_cost': 350,  # SAR - Average cost per hospital visit (consultation + tests)
    'avg_medicine_cost': 80,  # SAR - Average medicine cost per prescription
    
    # VC medicine prescription (for those who DON'T go to hospital)
    'vc_medicine_prescription_pct': 0.50,  # 60% of VC-only patients get medicine prescription
    
    # Hospital visitor utilization
    'hospital_medicine_utilization': 0.85,  # 85% of hospital visitors get medicines
    
    # Non-VC users hospital-seeking behavior
    'non_vc_hospital_seeking_pct': 0.05,  # 70% of sick tourists who skip VC will go to hospital
}

def calc_downstream_revenue(vc_calls, params=None):
    """
    Calculate downstream healthcare revenue from VC users.
    
    Two pathways:
    1. VC → Hospital: vc_to_hospital_pct go to hospital, incur hospital visit + medicine costs
    2. VC Only: Remaining get medicine prescription only
    """
    if params is None:
        params = DEFAULT_HEALTHCARE_PARAMS.copy()
    
    # Pathway 1: VC users who go to hospital
    hospital_visitors = vc_calls * params['vc_to_hospital_pct']
    hospital_visit_revenue = hospital_visitors * params['avg_hospital_visit_cost']
    hospital_medicine_revenue = hospital_visitors * params['hospital_medicine_utilization'] * params['avg_medicine_cost']
    
    # Pathway 2: VC-only patients who get medicine prescription
    vc_only_patients = vc_calls * (1 - params['vc_to_hospital_pct'])
    vc_medicine_patients = vc_only_patients * params['vc_medicine_prescription_pct']
    vc_medicine_revenue = vc_medicine_patients * params['avg_medicine_cost']
    
    total_downstream_revenue = hospital_visit_revenue + hospital_medicine_revenue + vc_medicine_revenue
    
    return {
        'hospital_visitors': hospital_visitors,
        'hospital_visit_revenue': hospital_visit_revenue,
        'hospital_medicine_revenue': hospital_medicine_revenue,
        'vc_only_patients': vc_only_patients,
        'vc_medicine_patients': vc_medicine_patients,
        'vc_medicine_revenue': vc_medicine_revenue,
        'total_downstream_revenue': total_downstream_revenue,
        'avg_revenue_per_hospital_visit': (hospital_visit_revenue + hospital_medicine_revenue) / hospital_visitors if hospital_visitors > 0 else 0
    }

@st.cache_data(show_spinner=False)
def calc_scenario_A(n, sick_pct, pct_vc, vc_fee, vc_cost, referral_rate=0.25):
    """
    Scenario A (Paid VC)
    revenue = vc_fee * #vc_calls
    cost_vc = vc_cost * #vc_calls
    net_profit = revenue - cost_vc
    """
    sick_total = n * sick_pct
    vc_calls = sick_total * pct_vc
    revenue = vc_calls * vc_fee
    cost_vc = vc_calls * vc_cost
    net_profit = revenue - cost_vc
    total_op_visits = sick_total - vc_calls 
    
    return {
        "sick_total": sick_total,
        "vc_calls": vc_calls,
        "revenue": revenue,
        "vc_cost": cost_vc,
        "net_profit": net_profit,
        "Sick %": sick_pct * 100, 
        "% VC Uptake": pct_vc * 100, 
        "VC Fee": vc_fee,
        "total_op_visits": total_op_visits
    }

@st.cache_data(show_spinner=False)
def calc_scenario_B(n, premium, emergency_premium, sick_pct, pct_vc, vc_cost, referral_rate=0.25):
    """
    Scenario B (Free VC)
    revenue = premium * n
    cost_vc = vc_cost * #vc_calls
    cost_emergency = emergency_premium * n
    net_profit = revenue - cost_emergency - cost_vc
    """
    revenue = n * premium
    vc_calls = n * sick_pct * pct_vc
    cost_vc = vc_calls * vc_cost
    cost_emergency = n * emergency_premium
    net_profit = revenue - cost_emergency - cost_vc
    total_op_visits = n * sick_pct - vc_calls 
    
    return {
        "sick_total": n * sick_pct,
        "vc_calls": vc_calls,
        "revenue": revenue,
        "vc_cost": cost_vc,
        "cost_emergency": cost_emergency,
        "net_profit": net_profit,
        "total_op_visits": total_op_visits, 
        "Sick %": sick_pct * 100, 
        "% VC Uptake": pct_vc * 100, 
        "EI Fee": emergency_premium,
        "total_op_visits": total_op_visits
    }




@st.cache_data(show_spinner=False)
def compute_kpis_A(resA, n):
    revenue = resA['revenue']
    cost_vc = resA['vc_cost']
    profit = resA['net_profit']
    profit_margin = (profit / revenue * 100.0) if revenue != 0 else 0
    per_tourist_rev = revenue / n
    per_tourist_cost = cost_vc / n
    
    breakeven_vc_fee = None
    if resA['vc_calls'] > 0:
        breakeven_vc_fee = cost_vc / resA['vc_calls']
    
    return {
        "VC Calls": int(round(resA['vc_calls'])),
        "Revenue (SAR)": revenue,
        "VC Cost (SAR)": cost_vc,
        "Net Profit (SAR)": profit,
        "Profit Margin": profit_margin,
        "Revenue per tourist (SAR)": per_tourist_rev,
        "Cost per tourist (SAR)": per_tourist_cost,
        "Break-even VC fee (SAR)": breakeven_vc_fee if breakeven_vc_fee else 'n/a'
    }

@st.cache_data(show_spinner=False)
def compute_kpis_B(resB, n, premium):
    revenue = resB['revenue']
    cost_vc = resB['vc_cost']
    cost_emerg = resB['cost_emergency']
    profit = resB['net_profit']
    profit_margin = (profit / revenue * 100.0) if revenue != 0 else 0
    per_tourist_rev = revenue / n
    per_tourist_cost = (cost_vc + cost_emerg) / n
    pool_per_tourist = premium - (cost_emerg / n)
    
    return {
        "VC Calls": int(round(resB['vc_calls'])),
        "Revenue (SAR)": revenue,
        "VC Cost (SAR)": cost_vc,
        "Emergency Cost (SAR)": cost_emerg,
        "Net Profit (SAR)": profit,
        "Profit Margin": profit_margin,
        "Revenue per tourist (SAR)": per_tourist_rev,
        "Cost per tourist (SAR)": per_tourist_cost,
        "Pool per tourist (SAR)": pool_per_tourist
    }

@st.cache_data(show_spinner=False)
def calc_scenario_A_page_3(n, sick_pct, pct_vc, vc_fee, vc_cost, referral_rate=0.25, healthcare_params=None):
    """
    Scenario A (Paid VC) - Tourist pays for VC + downstream services
    
    Tourist spending:
    1. VC fee (if they use VC)
    2. Hospital visit cost (if they go to hospital after VC)
    3. Medicine cost (if prescribed - from VC or hospital)
    
    Non-VC users: Only a portion will actually go to hospital (hospital-seeking behavior)
    """
    if healthcare_params is None:
        healthcare_params = DEFAULT_HEALTHCARE_PARAMS.copy()
    
    sick_total = n * sick_pct
    vc_calls = sick_total * pct_vc
    
    # VC revenue and cost
    vc_revenue = vc_calls * vc_fee
    vc_cost_total = vc_calls * vc_cost
    
    # Downstream healthcare revenue (tourist spending)
    downstream = calc_downstream_revenue(vc_calls, healthcare_params)
    
    # Total tourist spending on healthcare through VC pathway
    total_tourist_spending = vc_revenue + downstream['total_downstream_revenue']
    
    # Net profit for VC operator
    net_profit = vc_revenue - vc_cost_total
    
    # Direct hospital visits (bypass VC) - only a portion will actually go to hospital
    sick_no_vc = sick_total - vc_calls
    direct_hospital_visits = sick_no_vc * healthcare_params['non_vc_hospital_seeking_pct']
    direct_hospital_spending = direct_hospital_visits * healthcare_params['avg_hospital_visit_cost']
    
    # Sick tourists who don't use VC and don't go to hospital (self-care)
    self_care_tourists = sick_no_vc * (1 - healthcare_params['non_vc_hospital_seeking_pct'])
    
    # Total healthcare system revenue
    total_healthcare_revenue = total_tourist_spending + direct_hospital_spending
    
    return {
        "sick_total": sick_total,
        "vc_calls": vc_calls,
        "direct_hospital_visits": direct_hospital_visits,
        "self_care_tourists": self_care_tourists,
        "vc_to_hospital_patients": downstream['hospital_visitors'],

        # VC operator financials
        "vc_revenue": vc_revenue,
        "vc_cost": vc_cost_total,
        "net_profit": net_profit,
        
        # Tourist spending breakdown
        "vc_spending": vc_revenue,
        "hospital_visit_spending": downstream['hospital_visit_revenue'],
        "hospital_medicine_spending": downstream['hospital_medicine_revenue'],
        "vc_medicine_spending": downstream['vc_medicine_revenue'],
        "direct_hospital_spending": direct_hospital_spending,
        
        # Healthcare revenue components
        "hospital_visitors_from_vc": downstream['hospital_visitors'],
        "vc_only_patients": downstream['vc_only_patients'],
        "vc_medicine_patients": downstream['vc_medicine_patients'],
        "downstream_revenue": downstream['total_downstream_revenue'],
        "avg_revenue_per_hospital_visit": downstream['avg_revenue_per_hospital_visit'],
        
        # Total metrics
        "total_tourist_spending": total_tourist_spending,  # VC pathway spending
        "total_healthcare_revenue": total_healthcare_revenue,  # All healthcare spending
        "spending_per_tourist": total_healthcare_revenue / n,
        "spending_per_sick_tourist": total_healthcare_revenue / sick_total if sick_total > 0 else 0,
        "spending_per_vc_user": total_tourist_spending / vc_calls if vc_calls > 0 else 0,
        
        # Care pathway metrics
        "vc_penetration_rate": (vc_calls / sick_total * 100) if sick_total > 0 else 0,
        "hospital_conversion_rate": (downstream['hospital_visitors'] / vc_calls * 100) if vc_calls > 0 else 0,
        "hospital_seeking_rate": (direct_hospital_visits / sick_no_vc * 100) if sick_no_vc > 0 else 0,
        
        # For plotting
        "Sick %": sick_pct * 100, 
        "% VC Uptake": pct_vc * 100, 
        "VC Fee": vc_fee,
        "revenue": vc_revenue  # backward compatibility
    }

@st.cache_data(show_spinner=False)
def calc_scenario_B_page_3(n, sick_pct, pct_vc, premium, vc_cost, page, ei_fee, referral_rate=0.25, healthcare_params=None):
    """
    Scenario B (Free VC) - Tourist pays insurance premium, VC included
    
    Tourist spending: 
    1. Insurance premium (fixed, includes VC)
    2. Hospital visit cost (if they go to hospital after VC)
    3. Medicine cost (if prescribed - from VC or hospital)
    
    Non-VC users: Only a portion will actually go to hospital (hospital-seeking behavior)
    """

    
    if healthcare_params is None:
        healthcare_params = DEFAULT_HEALTHCARE_PARAMS.copy()
    
    sick_total = n * sick_pct
    vc_calls = sick_total * pct_vc
    if page==3:  premium=0
    # Insurance revenue (fixed)
    insurance_revenue = n * premium
    
    # VC costs (absorbed by insurance company)
    vc_cost_total = vc_calls * vc_cost
    
    # Downstream healthcare revenue (tourist still pays for hospital & medicine)
    downstream = calc_downstream_revenue(vc_calls, healthcare_params)
    
    # Total tourist spending on healthcare through VC pathway
    total_tourist_spending = insurance_revenue + downstream['total_downstream_revenue']
    
    # Net profit for insurance company
    net_profit = insurance_revenue - vc_cost_total
    
    # Direct hospital visits (bypass VC) - only a portion will actually go to hospital
    sick_no_vc = sick_total - vc_calls
    direct_hospital_visits = sick_no_vc * healthcare_params['non_vc_hospital_seeking_pct']
    direct_hospital_spending = direct_hospital_visits * healthcare_params['avg_hospital_visit_cost']
    
    # Sick tourists who don't use VC and don't go to hospital (self-care)
    self_care_tourists = sick_no_vc * (1 - healthcare_params['non_vc_hospital_seeking_pct'])
    
    # Total healthcare system revenue
    total_healthcare_revenue = total_tourist_spending + direct_hospital_spending
    
    return {
        "sick_total": sick_total,
        "vc_calls": vc_calls,
        "direct_hospital_visits": direct_hospital_visits,
        "self_care_tourists": self_care_tourists,
        "vc_to_hospital_patients": downstream['hospital_visitors'],
        
        # Insurance company financials
        "revenue": insurance_revenue,
        "vc_cost": vc_cost_total,
        "net_profit": net_profit,
        
        # Tourist spending breakdown
        "insurance_spending": insurance_revenue,
        "hospital_visit_spending": downstream['hospital_visit_revenue'],
        "hospital_medicine_spending": downstream['hospital_medicine_revenue'],
        "vc_medicine_spending": downstream['vc_medicine_revenue'],
        "direct_hospital_spending": direct_hospital_spending,
        
        # Healthcare revenue components
        "hospital_visitors_from_vc": downstream['hospital_visitors'],
        "vc_only_patients": downstream['vc_only_patients'],
        "vc_medicine_patients": downstream['vc_medicine_patients'],
        "downstream_revenue": downstream['total_downstream_revenue'],
        "avg_revenue_per_hospital_visit": downstream['avg_revenue_per_hospital_visit'],
        
        # Total metrics
        "total_tourist_spending": total_tourist_spending,  # VC pathway spending
        "total_healthcare_revenue": total_healthcare_revenue,  # All healthcare spending
        "spending_per_tourist": total_healthcare_revenue / n,
        "spending_per_sick_tourist": total_healthcare_revenue / sick_total if sick_total > 0 else 0,
        "spending_per_vc_user": total_tourist_spending / vc_calls if vc_calls > 0 else 0,
        
        # Care pathway metrics
        "vc_penetration_rate": (vc_calls / sick_total * 100) if sick_total > 0 else 0,
        "hospital_conversion_rate": (downstream['hospital_visitors'] / vc_calls * 100) if vc_calls > 0 else 0,
        "hospital_seeking_rate": (direct_hospital_visits / sick_no_vc * 100) if sick_no_vc > 0 else 0,
        
        # For plotting
        "Sick %": sick_pct * 100, 
        "% VC Uptake": pct_vc * 100, 
        "EI Fee": 0,  # no emergency insurance
        "cost_emergency": 0  # backward compatibility
    }

@st.cache_data(show_spinner=False)
def compute_kpis_A_page_3(resA, n):
    vc_revenue = resA.get('vc_revenue', resA.get('revenue', 0))
    cost_vc = resA.get('vc_cost', 0)
    profit = resA['net_profit']
    
    profit_margin = (profit / vc_revenue * 100.0) if vc_revenue != 0 else 0
    
    return {
        # Volume metrics
        "VC Calls": int(round(resA['vc_calls'])),
        "Hospital Visitors (from VC)": int(round(resA.get('hospital_visitors_from_vc', 0))),
        "VC-Only Patients": int(round(resA.get('vc_only_patients', 0))),
        "VC Medicine Patients": int(round(resA.get('vc_medicine_patients', 0))),
        
        # VC Operator Financials
        "VC Revenue (SAR)": vc_revenue,
        "VC Cost (SAR)": cost_vc,
        "Net Profit (SAR)": profit,
        "Profit Margin (%)": profit_margin,
        
        # Tourist Spending Breakdown
        "VC Fee Spending (SAR)": resA.get('vc_spending', 0),
        "Hospital Visit Spending (SAR)": resA.get('hospital_visit_spending', 0),
        "Hospital Medicine Spending (SAR)": resA.get('hospital_medicine_spending', 0),
        "VC Medicine Spending (SAR)": resA.get('vc_medicine_spending', 0),
        "Direct Hospital Spending (SAR)": resA.get('direct_hospital_spending', 0),
        
        # Total Tourist Spending
        "Total Tourist Spending (SAR)": resA.get('total_healthcare_revenue', 0),
        "Spending per Tourist (SAR)": resA.get('spending_per_tourist', 0),
        "Spending per Sick Tourist (SAR)": resA.get('spending_per_sick_tourist', 0),
        "Spending per VC User (SAR)": resA.get('spending_per_vc_user', 0),
        
        # Efficiency metrics
        "VC Penetration Rate (%)": resA.get('vc_penetration_rate', 0),
        "Hospital Conversion Rate (%)": resA.get('hospital_conversion_rate', 0),
        
        # Backward compatibility
        "Revenue (SAR)": vc_revenue,
        "Revenue per tourist (SAR)": vc_revenue / n,
        "Cost per tourist (SAR)": cost_vc / n,
        "Break-even VC fee (SAR)": cost_vc / resA['vc_calls'] if resA['vc_calls'] > 0 else 'n/a'
    }

@st.cache_data(show_spinner=False)
def compute_kpis_B_page_3(resB, n, premium):
    insurance_revenue = resB['revenue']
    cost_vc = resB['cost_vc']
    profit = resB['net_profit']
    
    profit_margin = (profit / insurance_revenue * 100.0) if insurance_revenue != 0 else 0
    
    return {
        # Volume metrics
        "VC Calls": int(round(resB['vc_calls'])),
        "Hospital Visitors (from VC)": int(round(resB.get('hospital_visitors_from_vc', 0))),
        "VC-Only Patients": int(round(resB.get('vc_only_patients', 0))),
        "VC Medicine Patients": int(round(resB.get('vc_medicine_patients', 0))),
        
        # Insurance Company Financials
        "Insurance Revenue (SAR)": insurance_revenue,
        "VC Cost (SAR)": cost_vc,
        "Net Profit (SAR)": profit,
        "Profit Margin (%)": profit_margin,
        
        # Tourist Spending Breakdown
        "Insurance Premium Spending (SAR)": resB.get('insurance_spending', 0),
        "Hospital Visit Spending (SAR)": resB.get('hospital_visit_spending', 0),
        "Hospital Medicine Spending (SAR)": resB.get('hospital_medicine_spending', 0),
        "VC Medicine Spending (SAR)": resB.get('vc_medicine_spending', 0),
        "Direct Hospital Spending (SAR)": resB.get('direct_hospital_spending', 0),
        
        # Total Tourist Spending
        "Total Tourist Spending (SAR)": resB.get('total_healthcare_revenue', 0),
        "Spending per Tourist (SAR)": resB.get('spending_per_tourist', 0),
        "Spending per Sick Tourist (SAR)": resB.get('spending_per_sick_tourist', 0),
        "Spending per VC User (SAR)": resB.get('spending_per_vc_user', 0),
        
        # Efficiency metrics
        "VC Penetration Rate (%)": resB.get('vc_penetration_rate', 0),
        "Hospital Conversion Rate (%)": resB.get('hospital_conversion_rate', 0),
        
        # Backward compatibility
        "Revenue (SAR)": insurance_revenue,
        "Revenue per tourist (SAR)": insurance_revenue / n,
        "Cost per tourist (SAR)": cost_vc / n,
        "Pool per tourist (SAR)": premium,
        "Emergency Cost (SAR)": 0  # removed
    }