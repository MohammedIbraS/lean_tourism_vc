# # pages/1_comparison.py
# import streamlit as st
# import numpy as np
# import pandas as pd 
# from utils.calculations import calc_scenario_A, calc_scenario_B
# from utils import plots

# def app():
#     st.header("Comparison — Scenario A (Paid) vs Scenario B (Free)")
#     st.markdown(
#         "Use control global ranges and defaults. "
#         "This page displays multiple 3D surfaces for both scenarios. Colors: red=loss, green=profit."
#     )

# # population 
#     n = st.number_input("Total tourists (N)", min_value=1, value=28130000, step=1000, key='n_global')
# # Premium
#     premium = st.number_input("Initial premium (SAR)", min_value=1, value=95, key='premium')
#     max_emerg = premium - 5
# # Cost of VC   
#     # vc_cost_min, vc_cost_max = st.slider("VC Cost range (SAR)", 10, 200, (20, 120), key='vc_cost_range')
#     default_vc_cost = st.number_input("Cost of Virtual Clinic (SAR)", min_value=1, value=50, key='vc_cost')


#     colA, colB = st.columns(2)

#     with colA:
#         st.subheader("Scenario A — Paid VC")

#     #% of Sick
#         pct_sick_min_pct_a, pct_sick_max_pct_a = st.slider("A: % Sick pop range (%)", 1, 30, (3, 9), key='pct_sick_range')
#         pct_sick_min_a = pct_sick_min_pct_a / 100.0; pct_sick_max_a = pct_sick_max_pct_a / 100.0

#     #% of VC 

#         pct_vc_min_pct_a, pct_vc_max_pct_a = st.slider(" A: % VC uptake range (%)", 0, 100, (10, 40), key='pct_vc_range')
#         pct_vc_min_a = pct_vc_min_pct_a / 100.0; pct_vc_max_a = pct_vc_max_pct_a / 100.0

#     #% Fee of VC  
#         vc_fee_min, vc_fee_max = st.slider("VC Fee range (SAR)", 0, 300, (40, 140), key='vc_fee_range')

#     # prepare grids
#         pct_sicks = np.linspace(pct_sick_min_a, pct_sick_max_a, 30)
#         pct_vcs = np.linspace(pct_vc_min_a, pct_vc_max_a, 30)
#         vc_fees = np.linspace(vc_fee_min, vc_fee_max, 30)
#         # Z1 = np.zeros((len(pct_vcs), len(vc_costs)))
#         result = []
#         for i, pct_si in enumerate(pct_sicks):
#             for j, pct_vc in enumerate(pct_vcs):
#                 for k, vc_fee in enumerate(vc_fees):
#                     result.append(calc_scenario_A(n, pct_si, pct_vc, vc_fee, default_vc_cost))

#         df_ = pd.DataFrame(result)
#         fig_1 = plots.make_4d_scatter_plotly(
#                     df=df_,
#                     x_col="Sick %",
#                     y_col="% VC Uptake",
#                     z_col="VC Fee",
#                     color_col='net_profit',
#                     title='Net Profit Across Scenarios'
#                                                     )
#         fig_1.update_layout(template="plotly_white") 
#         st.plotly_chart(fig_1, use_container_width=True)


#     with colB:

#         st.subheader("Scenario B — Free VC")

#     #% of Sick
#         pct_sick_min_pct_b, pct_sick_max_pct_b = st.slider("B: % Sick pop range (%)", 1, 30, (6, 16), key='pct_sick_range_b')
#         pct_sick_min_b = pct_sick_min_pct_b / 100.0; pct_sick_max_b = pct_sick_max_pct_b / 100.0

#     #% of VC 

#         pct_vc_min_pct_b, pct_vc_max_pct_b = st.slider(" B: % VC uptake range (%)", 0, 100, (30, 80), key='pct_vc_range_b')
#         pct_vc_min_b = pct_vc_min_pct_b / 100.0; pct_vc_max_b = pct_vc_max_pct_b / 100.0

#     # Emergency Premium 
#         ei_fee_min, ei_fee_max = st.slider("Emergency premium range (SAR)", 30, max_emerg, (30, 70), key='ei_fee_range')

#     # prepare grids
#         pct_sicks = np.linspace(pct_sick_min_b, pct_sick_max_b, 30)
#         pct_vcs = np.linspace(pct_vc_min_b, pct_vc_max_b, 30)
#         ei_fees = np.linspace(ei_fee_min, ei_fee_max, 30)
#         # Z1 = np.zeros((len(pct_vcs), len(vc_costs)))
#         result = []
#         for i, pct_si in enumerate(pct_sicks):
#             for j, pct_vc in enumerate(pct_vcs):
#                 for k, ei_fee in enumerate(ei_fees):
#                     result.append(calc_scenario_B(n, premium, ei_fee,  pct_si, pct_vc,  default_vc_cost))

#         df_ = pd.DataFrame(result)
#         fig_2 = plots.make_4d_scatter_plotly(
#                     df=df_,
#                     x_col="Sick %",
#                     y_col="% VC Uptake",
#                     z_col="EI Fee",
#                     color_col='net_profit',
#                     title='Net Profit Across Scenarios'
#                                                     )
#         fig_2.update_layout(template="plotly_white") 
#         st.plotly_chart(fig_2, use_container_width=True)



#     # x_key, x_vals = axis_options[x_choice]
#     # y_key, y_vals = axis_options[y_choice]
#     # Zadhoc = np.zeros((len(y_vals), len(x_vals)))
#     # for i, yv in enumerate(y_vals):
#     #     for j, xv in enumerate(x_vals):
#     #         if scenario_choice.startswith("A"):
#     #             s = default_pct_sick_a; u = default_pct_vc_a; f = default_vc_fee; c = default_vc_cost
#     #             if x_key == "vc_cost": c = xv
#     #             if x_key == "vc_fee": f = xv
#     #             if x_key == "pct_vc": u = xv
#     #             if x_key == "pct_sick": s = xv
#     #             if y_key == "vc_cost": c = yv
#     #             if y_key == "vc_fee": f = yv
#     #             if y_key == "pct_vc": u = yv
#     #             if y_key == "pct_sick": s = yv
#     #             res = calc_scenario_A(n, s, u, f, c)
#     #             Zadhoc[i, j] = res['net_profit']
#     #         else:
#     #             s = default_pct_sick_b; u = default_pct_vc_b; c = default_vc_cost; emerg = default_emergency_premium
#     #             if x_key == "vc_cost": c = xv
#     #             if x_key == "pct_vc": u = xv
#     #             if x_key == "pct_sick": s = xv
#     #             if x_key == "emerg": emerg = xv
#     #             if y_key == "vc_cost": c = yv
#     #             if y_key == "pct_vc": u = yv
#     #             if y_key == "pct_sick": s = yv
#     #             if y_key == "emerg": emerg = yv
#     #             res = calc_scenario_B(n, premium, emerg, s, u, c)
#     #             Zadhoc[i, j] = res['net_profit']

#     # figAdhoc = make_surface_plotly(x_vals, y_vals, Zadhoc, x_choice, y_choice, "Net Profit (SAR)", title=f"Ad-hoc: {scenario_choice}")
#     # st.plotly_chart(figAdhoc, use_container_width=True)


# pages/1_comparison.py
import streamlit as st
import numpy as np
import pandas as pd 
from utils.calculations import calc_scenario_A, calc_scenario_B, compute_kpis_A, compute_kpis_B
from utils import plots
from utils import comparison
from utils import scenario_manager

def app():
    # Enhanced styling
    st.markdown("""
        <style>
        .insight-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .metric-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin: 10px 0;
        }
        .scenario-section-a {
            background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #2196F3;
            margin: 15px 0;
        }
        .scenario-section-b {
            background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #FF9800;
            margin: 15px 0;
        }
        .help-text {
            font-size: 0.85rem;
            color: #666;
            font-style: italic;
            margin-top: 0.25rem;
        }
        .parameter-group {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 1px solid #e0e0e0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Page header with better description
    st.markdown("""
        <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
            <h2 style="color: #1f77b4; margin-bottom: 0.5rem;">📊 Sensitivity & Break-Even Analysis</h2>
            <p style="color: #555; font-size: 1rem; margin: 0;">
                Explore how key parameters impact profitability and identify break-even thresholds for optimal decision-making.
                Adjust parameters below to see real-time analysis across multiple scenarios.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Global Parameters with collapsible section
    with st.expander("⚙️ **Global Parameters** (Click to expand)", expanded=True):
        st.markdown("""
            <div class="help-text" style="margin-bottom: 1rem;">
                💡 These parameters apply to both scenarios. Adjust them first before exploring scenario-specific parameters.
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            n = st.number_input(
                "Total Tourists (N)", 
                min_value=1, 
                value=28130000, 
                step=1000000, 
                key='n_global',
                help="Total number of tourists expected in the analysis period"
            )
            st.caption(f"📊 {n/1_000_000:.1f}M tourists")
        with col2:
            premium = st.number_input(
                "Insurance Premium (SAR)", 
                min_value=1, 
                value=95, 
                key='premium',
                help="Base insurance premium charged per tourist"
            )
            st.caption(f"💰 SAR {premium} per tourist")
        with col3:
            default_vc_cost = st.number_input(
                "VC Delivery Cost (SAR)", 
                min_value=1, 
                value=50, 
                key='vc_cost',
                help="Cost to deliver one virtual consultation"
            )
            st.caption(f"💊 SAR {default_vc_cost} per VC call")
        
        # Grid size option for performance
        grid_size = st.slider(
            "Analysis Grid Size (affects computation time)",
            min_value=10,
            max_value=30,
            value=20,
            step=5,
            key='grid_size',
            help="Smaller values = faster computation, larger values = more detailed analysis"
        )
        st.caption(f"⚡ Using {grid_size}x{grid_size}x{grid_size} grid ({grid_size**3:,} combinations per scenario)")

    max_emerg = premium - 5

    # Analysis Mode Selection with better UI
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
            <h3 style="color: #1f77b4; margin-bottom: 0.5rem;">🎯 Analysis Mode Selection</h3>
            <p style="color: #666; margin: 0; font-size: 0.95rem;">
                Choose the type of analysis you want to perform. Each mode provides different insights and visualizations.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    analysis_mode = st.radio(
        "Select Analysis Type:",
        ["📈 Sensitivity Analysis", "⚖️ Break-Even Analysis", "🔍 Parameter Optimization", "📊 Comparative Analysis"],
        horizontal=True,
        help="Sensitivity: See how parameters affect profit | Break-Even: Find profitability thresholds | Optimization: Find best parameter combinations | Comparative: See correlations and relationships"
    )
    
    # Show description for selected mode
    mode_descriptions = {
        "📈 Sensitivity Analysis": "Analyze how changes in individual parameters impact overall profitability",
        "⚖️ Break-Even Analysis": "Identify the minimum/maximum parameter values needed to break even",
        "🔍 Parameter Optimization": "Discover the most profitable parameter combinations",
        "📊 Comparative Analysis": "Explore correlations and relationships between parameters and outcomes"
    }
    
    st.info(f"**{analysis_mode}**: {mode_descriptions[analysis_mode]}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # Tabs for scenarios with better labels
    tab_a, tab_b = st.tabs([
        "🔵 Scenario A — Paid VC (Tourists pay per consultation)", 
        "🟠 Scenario B — Free VC (Included in premium)"
    ])

    # ============= SCENARIO A =============
    with tab_a:
        st.markdown("""
            <div class="scenario-section-a">
                <h3 style="color: #1976D2; margin-bottom: 0.5rem;">🔵 Scenario A: Paid Virtual Consultation Model</h3>
                <p style="color: #666; font-style: italic; margin-top: -5px;">
                    <strong>Business Model:</strong> Tourists pay separately for VC services. Revenue scales with VC adoption and fee.
                </p>
                <p style="color: #666; margin-top: 0.5rem; font-size: 0.9rem;">
                    💡 <strong>Key Parameters:</strong> Sick population %, VC uptake %, and VC fee determine profitability.
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Parameter inputs with better organization
        with st.expander("📝 **Scenario A Parameters** (Click to adjust)", expanded=True):
            col_a1, col_a2, col_a3 = st.columns(3)
            with col_a1:
                pct_sick_min_pct_a, pct_sick_max_pct_a = st.slider(
                    "% Population Seeking Care Range", 
                    1, 30, (3, 9), 
                    key='pct_sick_range_a',
                    help="Percentage of tourists who need medical care"
                )
                pct_sick_min_a = pct_sick_min_pct_a / 100.0
                pct_sick_max_a = pct_sick_max_pct_a / 100.0
                st.caption(f"Range: {pct_sick_min_pct_a}% - {pct_sick_max_pct_a}%")

            with col_a2:
                pct_vc_min_pct_a, pct_vc_max_pct_a = st.slider(
                    "% VC Uptake Range", 
                    0, 100, (10, 40), 
                    key='pct_vc_range_a',
                    help="Percentage of sick tourists who choose VC over in-person visits"
                )
                pct_vc_min_a = pct_vc_min_pct_a / 100.0
                pct_vc_max_a = pct_vc_max_pct_a / 100.0
                st.caption(f"Range: {pct_vc_min_pct_a}% - {pct_vc_max_pct_a}%")

            with col_a3:
                vc_fee_min, vc_fee_max = st.slider(
                    "VC Fee Range (SAR)", 
                    0, 300, (40, 140), 
                    key='vc_fee_range_a',
                    help="Price charged per virtual consultation"
                )
                st.caption(f"Range: SAR {vc_fee_min} - SAR {vc_fee_max}")
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Generate data for Scenario A with progress
        st.markdown("### 📊 Analysis Results")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("🔄 Computing Scenario A analysis... This may take a few seconds."):
            pct_sicks_a = np.linspace(pct_sick_min_a, pct_sick_max_a, grid_size)
            pct_vcs_a = np.linspace(pct_vc_min_a, pct_vc_max_a, grid_size)
            vc_fees_a = np.linspace(vc_fee_min, vc_fee_max, grid_size)
            
            total_combinations = len(pct_sicks_a) * len(pct_vcs_a) * len(vc_fees_a)
            results_a = []
            
            count = 0
            for pct_si in pct_sicks_a:
                for pct_vc in pct_vcs_a:
                    for vc_fee in vc_fees_a:
                        results_a.append(calc_scenario_A(n, pct_si, pct_vc, vc_fee, default_vc_cost))
                        count += 1
                        if count % 100 == 0:
                            progress_bar.progress(count / total_combinations)
                            status_text.text(f"Processing: {count}/{total_combinations} combinations...")
            
            df_a = pd.DataFrame(results_a)
            # Store in session state for comparison dashboard
            st.session_state.df_a = df_a
            progress_bar.progress(1.0)
            status_text.text("✅ Analysis complete!")
            st.success(f"✅ Analyzed {len(df_a):,} parameter combinations")

        # Key Insights for Scenario A
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💡 Key Insights — Scenario A")
        
        optimal_a = df_a.loc[df_a['net_profit'].idxmax()]
        worst_a = df_a.loc[df_a['net_profit'].idxmin()]
        
        insight_col1, insight_col2, insight_col3, insight_col4 = st.columns(4)
        
        with insight_col1:
            st.metric("Optimal Profit", f"SAR {optimal_a['net_profit']/1e6:.2f}M")
            st.caption(f"At: {optimal_a['Sick %']:.1f}% sick, {optimal_a['% VC Uptake']:.1f}% uptake, SAR {optimal_a['VC Fee']:.0f} fee")
        
        with insight_col2:
            break_even_a = df_a[df_a['net_profit'] >= 0]
            st.metric("Break-Even Scenarios", f"{len(break_even_a)}/{len(df_a)}")
            st.caption(f"{len(break_even_a)/len(df_a)*100:.1f}% of scenarios profitable")
        
        with insight_col3:
            avg_profit_a = df_a['net_profit'].mean()
            st.metric("Average Profit", f"SAR {avg_profit_a/1e6:.2f}M")
            st.caption("Across all parameter combinations")
        
        with insight_col4:
            profit_range_a = optimal_a['net_profit'] - worst_a['net_profit']
            st.metric("Profit Range", f"SAR {profit_range_a/1e6:.2f}M")
            st.caption("Difference between best and worst")

        # Analysis visualizations based on mode
        st.markdown("<br>", unsafe_allow_html=True)
        
        if analysis_mode == "📈 Sensitivity Analysis":
            st.markdown("### 📈 Sensitivity Analysis — Scenario A")
            
            # # Tornado Chart
            # fig_tornado_a = plots.create_tornado_chart(df_a, 'Scenario A (Paid VC)')
            # st.plotly_chart(fig_tornado_a, use_container_width=True)
            
            # 2D Heatmaps
            col_heat1, col_heat2 = st.columns(2)
            
            with col_heat1:
                st.markdown("#### Net Profit by Sick % vs VC Uptake %")
                fig_heat1_a = plots.create_2d_heatmap(
                    df_a, 'Sick %', '% VC Uptake', 'net_profit',
                    'Net Profit: Sick % vs VC Uptake %'
                )
                st.plotly_chart(fig_heat1_a, use_container_width=True)
            
            with col_heat2:
                st.markdown("#### Net Profit by VC Uptake % vs Fee")
                fig_heat2_a = plots.create_2d_heatmap(
                    df_a, '% VC Uptake', 'VC Fee', 'net_profit',
                    'Net Profit: VC Uptake % vs Fee'
                )
                st.plotly_chart(fig_heat2_a, use_container_width=True)
            
            # Parameter Impact Lines
            st.markdown("#### Individual Parameter Impact on Profit")
            fig_params_a = plots.create_parameter_impact_lines(df_a, 'Scenario A')
            st.plotly_chart(fig_params_a, use_container_width=True)
        
        elif analysis_mode == "⚖️ Break-Even Analysis":
            st.markdown("### ⚖️ Break-Even Analysis — Scenario A")
            
            # Interactive break-even finder
            st.markdown("#### Break-Even VC Fee Calculator")
            st.markdown("*Fix two parameters to find the break-even VC Fee*")
            
            col_be1, col_be2 = st.columns(2)
            with col_be1:
                fixed_sick_a = st.slider("Fixed % Sick Population", 
                                         float(pct_sick_min_a*100), 
                                         float(pct_sick_max_a*100), 
                                         float(np.mean([pct_sick_min_a, pct_sick_max_a])*100),
                                         key='fixed_sick_a') / 100.0
            with col_be2:
                fixed_vc_a = st.slider("Fixed % VC Uptake", 
                                       float(pct_vc_min_a*100), 
                                       float(pct_vc_max_a*100), 
                                       float(np.mean([pct_vc_min_a, pct_vc_max_a])*100),
                                       key='fixed_vc_a') / 100.0
            
            # Calculate break-even
            break_even_fee_a = default_vc_cost  # Simplified: break-even when fee = cost
            
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown(f"""
            **Break-Even VC Fee: SAR {break_even_fee_a:.2f}**
            
            At {fixed_sick_a*100:.1f}% sick population and {fixed_vc_a*100:.1f}% VC uptake, 
            the VC fee must be at least **SAR {break_even_fee_a:.2f}** to break even.
            
            - Current VC cost: SAR {default_vc_cost}
            - Minimum profitable fee: SAR {break_even_fee_a:.2f}
            - Recommended fee (with 20% margin): SAR {break_even_fee_a * 1.2:.2f}
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Break-even visualization
            fig_breakeven_a = plots.create_breakeven_chart(df_a, fixed_sick_a, fixed_vc_a, break_even_fee_a)
            st.plotly_chart(fig_breakeven_a, use_container_width=True)
            
        elif analysis_mode == "🔍 Parameter Optimization":
            st.markdown("### 🔍 Parameter Optimization — Scenario A")
            
            # Show optimal combinations
            top_scenarios_a = df_a.nlargest(10, 'net_profit')[['Sick %', '% VC Uptake', 'VC Fee', 'net_profit', 'revenue', 'cost_vc']]
            top_scenarios_a['Profit (M)'] = top_scenarios_a['net_profit'] / 1e6
            top_scenarios_a['Revenue (M)'] = top_scenarios_a['revenue'] / 1e6
            top_scenarios_a['Cost (M)'] = top_scenarios_a['cost_vc'] / 1e6
            
            st.markdown("#### Top 10 Most Profitable Parameter Combinations")
            st.dataframe(
                top_scenarios_a[['Sick %', '% VC Uptake', 'VC Fee', 'Profit (M)', 'Revenue (M)', 'Cost (M)']].style.format({
                    'Sick %': '{:.1f}%',
                    '% VC Uptake': '{:.1f}%',
                    'VC Fee': 'SAR {:.0f}',
                    'Profit (M)': '{:.2f}M',
                    'Revenue (M)': '{:.2f}M',
                    'Cost (M)': '{:.2f}M'
                }).background_gradient(subset=['Profit (M)'], cmap='RdYlGn'),
                use_container_width=True
            )
            
            # Optimal ranges visualization
            fig_optimal_a = plots.create_optimal_ranges_chart(df_a)
            st.plotly_chart(fig_optimal_a, use_container_width=True)
        
        elif analysis_mode == "📊 Comparative Analysis":
            st.markdown("### 📊 Comparative Analysis — Scenario A")
            
            # Correlation matrix
            fig_corr_a = plots.create_correlation_heatmap(df_a, 'Scenario A')
            st.plotly_chart(fig_corr_a, use_container_width=True)
            
            # 3D scatter with profit zones
            fig_3d_a = plots.create_3d_profit_zones(df_a, 'Sick %', '% VC Uptake', 'VC Fee', 'net_profit', 'Scenario A')
            st.plotly_chart(fig_3d_a, use_container_width=True)

    # ============= SCENARIO B =============
    with tab_b:
        st.markdown("""
            <div class="scenario-section-b">
                <h3 style="color: #F57C00; margin-bottom: 0.5rem;">🟠 Scenario B: Free Virtual Consultation Model</h3>
                <p style="color: #666; font-style: italic; margin-top: -5px;">
                    <strong>Business Model:</strong> VC included in insurance premium. Fixed revenue, variable costs.
                </p>
                <p style="color: #666; margin-top: 0.5rem; font-size: 0.9rem;">
                    💡 <strong>Key Parameters:</strong> Sick population %, VC uptake %, and Emergency Insurance fee determine profitability.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
        st.markdown("<br>", unsafe_allow_html=True)

        # Parameter inputs with better organization
        with st.expander("📝 **Scenario B Parameters** (Click to adjust)", expanded=True):
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                pct_sick_min_pct_b, pct_sick_max_pct_b = st.slider(
                    "% Population Seeking Care Range", 
                    1, 30, (6, 16), 
                    key='pct_sick_range_b',
                    help="Percentage of tourists who need medical care"
                )
                pct_sick_min_b = pct_sick_min_pct_b / 100.0
                pct_sick_max_b = pct_sick_max_pct_b / 100.0
                st.caption(f"Range: {pct_sick_min_pct_b}% - {pct_sick_max_pct_b}%")

            with col_b2:
                pct_vc_min_pct_b, pct_vc_max_pct_b = st.slider(
                    "% VC Uptake Range", 
                    0, 100, (30, 80), 
                    key='pct_vc_range_b',
                    help="Percentage of sick tourists who choose VC over in-person visits"
                )
                pct_vc_min_b = pct_vc_min_pct_b / 100.0
                pct_vc_max_b = pct_vc_max_pct_b / 100.0
                st.caption(f"Range: {pct_vc_min_pct_b}% - {pct_vc_max_pct_b}%")

            with col_b3:
                ei_fee_min, ei_fee_max = st.slider(
                    "Emergency Insurance Range (SAR)", 
                    30, max_emerg, (30, 70), 
                    key='ei_fee_range_b',
                    help="Cost per tourist for emergency insurance coverage"
                )
                st.caption(f"Range: SAR {ei_fee_min} - SAR {ei_fee_max}")
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Generate data for Scenario B with progress
        st.markdown("### 📊 Analysis Results")
        
        progress_bar_b = st.progress(0)
        status_text_b = st.empty()
        
        with st.spinner("🔄 Computing Scenario B analysis... This may take a few seconds."):
            pct_sicks_b = np.linspace(pct_sick_min_b, pct_sick_max_b, grid_size)
            pct_vcs_b = np.linspace(pct_vc_min_b, pct_vc_max_b, grid_size)
            ei_fees_b = np.linspace(ei_fee_min, ei_fee_max, grid_size)
            
            total_combinations_b = len(pct_sicks_b) * len(pct_vcs_b) * len(ei_fees_b)
            results_b = []
            
            count_b = 0
            for pct_si in pct_sicks_b:
                for pct_vc in pct_vcs_b:
                    for ei_fee in ei_fees_b:
                        results_b.append(calc_scenario_B(n, premium, ei_fee, pct_si, pct_vc, default_vc_cost))
                        count_b += 1
                        if count_b % 100 == 0:
                            progress_bar_b.progress(count_b / total_combinations_b)
                            status_text_b.text(f"Processing: {count_b}/{total_combinations_b} combinations...")
            
            df_b = pd.DataFrame(results_b)
            # Store in session state for comparison dashboard
            st.session_state.df_b = df_b
            progress_bar_b.progress(1.0)
            status_text_b.text("✅ Analysis complete!")
            st.success(f"✅ Analyzed {len(df_b):,} parameter combinations")

        # Key Insights for Scenario B
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💡 Key Insights — Scenario B")
        
        optimal_b = df_b.loc[df_b['net_profit'].idxmax()]
        worst_b = df_b.loc[df_b['net_profit'].idxmin()]
        
        insight_col1, insight_col2, insight_col3, insight_col4 = st.columns(4)
        
        with insight_col1:
            st.metric("Optimal Profit", f"SAR {optimal_b['net_profit']/1e6:.2f}M")
            st.caption(f"At: {optimal_b['Sick %']:.1f}% sick, {optimal_b['% VC Uptake']:.1f}% uptake, SAR {optimal_b['EI Fee']:.0f} EI fee")
        
        with insight_col2:
            break_even_b = df_b[df_b['net_profit'] >= 0]
            st.metric("Break-Even Scenarios", f"{len(break_even_b)}/{len(df_b)}")
            st.caption(f"{len(break_even_b)/len(df_b)*100:.1f}% of scenarios profitable")
        
        with insight_col3:
            avg_profit_b = df_b['net_profit'].mean()
            st.metric("Average Profit", f"SAR {avg_profit_b/1e6:.2f}M")
            st.caption("Across all parameter combinations")
        
        with insight_col4:
            profit_range_b = optimal_b['net_profit'] - worst_b['net_profit']
            st.metric("Profit Range", f"SAR {profit_range_b/1e6:.2f}M")
            st.caption("Difference between best and worst")

        # Analysis visualizations based on mode
        st.markdown("<br>", unsafe_allow_html=True)
        
        if analysis_mode == "📈 Sensitivity Analysis":
            st.markdown("### 📈 Sensitivity Analysis — Scenario B")
            
            # # Tornado Chart
            # fig_tornado_b = plots.create_tornado_chart(df_b, 'Scenario B (Free VC)')
            # st.plotly_chart(fig_tornado_b, use_container_width=True)
            
            # 2D Heatmaps
            col_heat1, col_heat2 = st.columns(2)
            
            with col_heat1:
                st.markdown("#### Net Profit by Sick % vs VC Uptake %")
                fig_heat1_b = plots.create_2d_heatmap(
                    df_b, 'Sick %', '% VC Uptake', 'net_profit',
                    'Net Profit: Sick % vs VC Uptake %'
                )
                st.plotly_chart(fig_heat1_b, use_container_width=True)
            
            with col_heat2:
                st.markdown("#### Net Profit by VC Uptake % vs EI Fee")
                fig_heat2_b = plots.create_2d_heatmap(
                    df_b, '% VC Uptake', 'EI Fee', 'net_profit',
                    'Net Profit: VC Uptake % vs EI Fee'
                )
                st.plotly_chart(fig_heat2_b, use_container_width=True)
            
            # Parameter Impact Lines
            st.markdown("#### Individual Parameter Impact on Profit")
            fig_params_b = plots.create_parameter_impact_lines(df_b, 'Scenario B')
            st.plotly_chart(fig_params_b, use_container_width=True)
        
        elif analysis_mode == "⚖️ Break-Even Analysis":
            st.markdown("### ⚖️ Break-Even Analysis — Scenario B")
            
            # Interactive break-even finder
            st.markdown("#### Break-Even Emergency Insurance Fee Calculator")
            st.markdown("*Fix two parameters to find the maximum Emergency Insurance fee for profitability*")
            
            col_be1, col_be2 = st.columns(2)
            with col_be1:
                fixed_sick_b = st.slider("Fixed % Sick Population", 
                                         float(pct_sick_min_b*100), 
                                         float(pct_sick_max_b*100), 
                                         float(np.mean([pct_sick_min_b, pct_sick_max_b])*100),
                                         key='fixed_sick_b') / 100.0
            with col_be2:
                fixed_vc_b = st.slider("Fixed % VC Uptake", 
                                       float(pct_vc_min_b*100), 
                                       float(pct_vc_max_b*100), 
                                       float(np.mean([pct_vc_min_b, pct_vc_max_b])*100),
                                       key='fixed_vc_b') / 100.0
            
            # Calculate break-even EI fee
            # Revenue = premium * n
            # Cost = (n * sick% * vc% * vc_cost) + (n * EI_fee)
            # Break-even: Revenue = Cost
            # premium * n = (n * sick% * vc% * vc_cost) + (n * EI_fee)
            # EI_fee = premium - (sick% * vc% * vc_cost)
            break_even_ei_b = premium - (fixed_sick_b * fixed_vc_b * default_vc_cost)
            
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown(f"""
            **Maximum Emergency Insurance Fee: SAR {break_even_ei_b:.2f}**
            
            At {fixed_sick_b*100:.1f}% sick population and {fixed_vc_b*100:.1f}% VC uptake, 
            the Emergency Insurance fee must be **at most SAR {break_even_ei_b:.2f}** to break even.
            
            - Insurance Premium: SAR {premium}
            - VC Cost per call: SAR {default_vc_cost}
            - VC utilization cost: SAR {fixed_sick_b * fixed_vc_b * default_vc_cost:.2f} per tourist
            - Maximum EI fee for break-even: SAR {break_even_ei_b:.2f}
            - Recommended EI fee (with 20% buffer): SAR {break_even_ei_b * 0.8:.2f}
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Break-even visualization
            fig_breakeven_b = plots.create_breakeven_chart_b(df_b, fixed_sick_b, fixed_vc_b, break_even_ei_b)
            st.plotly_chart(fig_breakeven_b, use_container_width=True)
            
        elif analysis_mode == "🔍 Parameter Optimization":
            st.markdown("### 🔍 Parameter Optimization — Scenario B")
            
            # Show optimal combinations
            top_scenarios_b = df_b.nlargest(10, 'net_profit')[['Sick %', '% VC Uptake', 'EI Fee', 'net_profit', 'revenue', 'cost_vc', 'cost_emergency']]
            top_scenarios_b['Profit (M)'] = top_scenarios_b['net_profit'] / 1e6
            top_scenarios_b['Revenue (M)'] = top_scenarios_b['revenue'] / 1e6
            top_scenarios_b['VC Cost (M)'] = top_scenarios_b['cost_vc'] / 1e6
            top_scenarios_b['EI Cost (M)'] = top_scenarios_b['cost_emergency'] / 1e6
            
            st.markdown("#### Top 10 Most Profitable Parameter Combinations")
            st.dataframe(
                top_scenarios_b[['Sick %', '% VC Uptake', 'EI Fee', 'Profit (M)', 'Revenue (M)', 'VC Cost (M)', 'EI Cost (M)']].style.format({
                    'Sick %': '{:.1f}%',
                    '% VC Uptake': '{:.1f}%',
                    'EI Fee': 'SAR {:.0f}',
                    'Profit (M)': '{:.2f}M',
                    'Revenue (M)': '{:.2f}M',
                    'VC Cost (M)': '{:.2f}M',
                    'EI Cost (M)': '{:.2f}M'
                }).background_gradient(subset=['Profit (M)'], cmap='RdYlGn'),
                use_container_width=True
            )
            
            # Optimal ranges visualization
            fig_optimal_b = plots.create_optimal_ranges_chart(df_b)
            st.plotly_chart(fig_optimal_b, use_container_width=True)
        
        elif analysis_mode == "📊 Comparative Analysis":
            st.markdown("### 📊 Comparative Analysis — Scenario B")
            
            # Correlation matrix
            fig_corr_b = plots.create_correlation_heatmap(df_b, 'Scenario B')
            st.plotly_chart(fig_corr_b, use_container_width=True)
            
            # 3D scatter with profit zones
            fig_3d_b = plots.create_3d_profit_zones(df_b, 'Sick %', '% VC Uptake', 'EI Fee', 'net_profit', 'Scenario B')
            st.plotly_chart(fig_3d_b, use_container_width=True)


# ============= REALISTIC CASE ANALYSIS =============
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## 💼 Realistic Case Analysis")
    st.markdown("### Base Case Scenario Comparison with Fixed Parameters")
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; color: white; margin: 20px 0;">
            <h4 style="color: white; margin-top: 0;">📋 Fixed Parameters for Realistic Comparison</h4>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px;">
                <div>
                    <strong>VC Delivery Cost:</strong> SAR 50<br>
                    <strong>Premium:</strong> SAR 95
                </div>
                <div>
                    <strong>Scenario A (Paid):</strong><br>
                    • Sick: 9%<br>
                    • VC Uptake: 30%<br>
                    • VC Fee: SAR 70
                </div>
                <div>
                    <strong>Scenario B (Free):</strong><br>
                    • Sick: 16%<br>
                    • VC Uptake: 80%<br>
                    • EI Fee: SAR 70
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Calculate realistic scenarios
    realistic_vc_cost = 50
    realistic_vc_fee = 70
    realistic_ei_fee = 70
    realistic_sick_a = 0.09
    realistic_sick_b = 0.16
    realistic_vc_uptake_a = 0.30
    realistic_vc_uptake_b = 0.80
    
    # Calculate Scenario A
    result_a_realistic = calc_scenario_A(n, realistic_sick_a, realistic_vc_uptake_a, 
                                         realistic_vc_fee, realistic_vc_cost)
    
    # Calculate Scenario B
    result_b_realistic = calc_scenario_B(n, premium, realistic_ei_fee, realistic_sick_b, 
                                         realistic_vc_uptake_b, realistic_vc_cost)
    
    # Display key metrics
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Realistic Case Results")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        profit_diff_realistic = result_a_realistic['net_profit'] - result_b_realistic['net_profit']
        st.metric(
            "Profit Difference",
            f"SAR {abs(profit_diff_realistic)/1e6:.2f}M",
            delta=f"{'A wins' if profit_diff_realistic > 0 else 'B wins'}"
        )
    
    with metric_col2:
        st.metric(
            "Scenario A Profit",
            f"SAR {result_a_realistic['net_profit']/1e6:.2f}M"
        )
    
    with metric_col3:
        st.metric(
            "Scenario B Profit",
            f"SAR {result_b_realistic['net_profit']/1e6:.2f}M"
        )
    
    with metric_col4:
        total_vc_realistic = result_a_realistic['vc_calls'] + result_b_realistic['vc_calls']
        st.metric(
            "Total VC Calls",
            f"{total_vc_realistic/1e6:.2f}M",
            delta=f"{total_vc_realistic/n*100:.1f}% of tourists"
        )
    
    # Waterfall charts
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💰 Revenue to Profit Breakdown")
    
    waterfall_col1, waterfall_spacer, waterfall_col2 = st.columns([10, 1, 10])
    
    with waterfall_col1:
        st.markdown("#### 🔵 Scenario A (Paid VC)")
        costs_a_realistic = {'VC Costs': result_a_realistic['cost_vc']}
        fig_waterfall_a_realistic = plots.create_waterfall_chart(
            'Scenario A', 
            result_a_realistic['revenue'], 
            costs_a_realistic, 
            result_a_realistic['net_profit']
        )
        st.plotly_chart(fig_waterfall_a_realistic, use_container_width=True)
        
        # Additional details
        with st.expander("📋 View Detailed Breakdown"):
            st.write(f"**Revenue:** SAR {result_a_realistic['revenue']:,.0f}")
            st.write(f"**VC Calls:** {result_a_realistic['vc_calls']:,.0f}")
            st.write(f"**VC Cost:** SAR {result_a_realistic['cost_vc']:,.0f}")
            st.write(f"**Net Profit:** SAR {result_a_realistic['net_profit']:,.0f}")
            st.write(f"**Profit Margin:** {(result_a_realistic['net_profit']/result_a_realistic['revenue']*100):.2f}%")
    
    with waterfall_col2:
        st.markdown("#### 🟠 Scenario B (Free VC)")
        costs_b_realistic = {
            'VC Costs': result_b_realistic['cost_vc'],
            'Emergency Costs': result_b_realistic['cost_emergency']
        }
        fig_waterfall_b_realistic = plots.create_waterfall_chart(
            'Scenario B', 
            result_b_realistic['revenue'], 
            costs_b_realistic, 
            result_b_realistic['net_profit']
        )
        st.plotly_chart(fig_waterfall_b_realistic, use_container_width=True)
        
        # Additional details
        with st.expander("📋 View Detailed Breakdown"):
            st.write(f"**Revenue:** SAR {result_b_realistic['revenue']:,.0f}")
            st.write(f"**VC Calls:** {result_b_realistic['vc_calls']:,.0f}")
            st.write(f"**VC Cost:** SAR {result_b_realistic['cost_vc']:,.0f}")
            st.write(f"**Emergency Cost:** SAR {result_b_realistic['cost_emergency']:,.0f}")
            st.write(f"**Net Profit:** SAR {result_b_realistic['net_profit']:,.0f}")
            st.write(f"**Profit Margin:** {(result_b_realistic['net_profit']/result_b_realistic['revenue']*100):.2f}%")
    
    # Strategic recommendation
    st.markdown("<br>", unsafe_allow_html=True)
    
    if profit_diff_realistic > 0:
        st.success(f"""
        ### ✅ Realistic Case Recommendation: Scenario A (Paid VC)
        
        Under realistic operating conditions, **Scenario A outperforms Scenario B** by **SAR {abs(profit_diff_realistic)/1e6:.2f}M**.
        
        **Key Factors:**
        - Lower sick population in Scenario A (9% vs 16%) reduces overall demand
        - Despite lower VC uptake (30% vs 80%), the fee-based model generates sufficient revenue
        - VC fee of SAR 70 provides a SAR 20 margin over delivery cost
        - No emergency insurance cost burden
        
        **Risk Consideration:** Scenario A's profitability depends on maintaining the 30% VC uptake rate among the sick population.
        """)
    else:
        st.success(f"""
        ### ✅ Realistic Case Recommendation: Scenario B (Free VC)
        
        Under realistic operating conditions, **Scenario B outperforms Scenario A** by **SAR {abs(profit_diff_realistic)/1e6:.2f}M**.
        
        **Key Factors:**
        - Higher sick population (16%) increases service demand
        - High VC uptake (80%) effectively diverts patients from expensive emergency care
        - Fixed revenue model (premium-based) provides stability
        - Emergency insurance cost is offset by premium collection
        
        **Value Proposition:** Scenario B offers better customer satisfaction with included services and more predictable revenue streams.
        """)
    
    # Sensitivity note
    st.info("""
    💡 **Note:** This analysis uses fixed realistic parameters. Use the sensitivity analysis tabs above to explore 
    how variations in these parameters affect profitability and to identify optimal operating ranges.
    """)

    # ============= SCENARIO COMPARISON DASHBOARD =============
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## 🔄 Direct Scenario Comparison Dashboard")
    st.markdown("Compare Scenario A and Scenario B side-by-side with comprehensive visualizations.")
    
    # Calculate KPIs for comparison
    kpis_a = compute_kpis_A(result_a_realistic, n)
    kpis_b = compute_kpis_B(result_b_realistic, n, premium)
    
    # Comparison charts
    comp_col1, comp_col2 = st.columns(2)
    
    with comp_col1:
        st.markdown("### 📊 Key Metrics Comparison")
        fig_comp = comparison.create_scenario_comparison_chart(kpis_a, kpis_b, "Scenario A vs Scenario B")
        st.plotly_chart(fig_comp, use_container_width=True)
    
    with comp_col2:
        st.markdown("### 📈 Profit Distribution Comparison")
        # Check if dataframes are available in session state
        if 'df_a' in st.session_state and 'df_b' in st.session_state:
            df_a_comp = st.session_state.df_a
            df_b_comp = st.session_state.df_b
            if len(df_a_comp) > 0 and len(df_b_comp) > 0:
                try:
                    fig_dist = comparison.create_profit_comparison_heatmap(df_a_comp, df_b_comp)
                    st.plotly_chart(fig_dist, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating profit distribution: {str(e)}")
                    st.info("Make sure you've run the sensitivity analysis for both scenarios above.")
            else:
                st.info("💡 Run the sensitivity analysis in the tabs above to see profit distribution comparison.")
        else:
            st.info("💡 Run the sensitivity analysis in the tabs above to see profit distribution comparison.")
    
    # Win/Loss Analysis
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎯 Win/Loss Analysis")
    st.markdown("Analyze which scenario performs better under different conditions.")
    
    if 'df_a' in st.session_state and 'df_b' in st.session_state:
        df_a_comp = st.session_state.df_a
        df_b_comp = st.session_state.df_b
        try:
            fig_winloss, comp_df = comparison.create_win_loss_analysis(df_a_comp, df_b_comp, n, premium, default_vc_cost)
            if fig_winloss:
                st.plotly_chart(fig_winloss, use_container_width=True)
                
                # Summary statistics
                win_a = len(comp_df[comp_df['Winner'] == 'A'])
                win_b = len(comp_df[comp_df['Winner'] == 'B'])
                total = len(comp_df)
                
                win_col1, win_col2, win_col3 = st.columns(3)
                with win_col1:
                    st.metric("Scenario A Wins", f"{win_a}/{total}", f"{win_a/total*100:.1f}%")
                with win_col2:
                    st.metric("Scenario B Wins", f"{win_b}/{total}", f"{win_b/total*100:.1f}%")
                with win_col3:
                    avg_diff = comp_df['Difference'].mean()
                    st.metric("Average Difference", f"SAR {avg_diff/1e6:.2f}M", 
                             delta="A advantage" if avg_diff > 0 else "B advantage")
        except Exception as e:
            st.info(f"Win/loss analysis available after running sensitivity analysis. Error: {str(e)}")
    else:
        st.info("💡 Run the sensitivity analysis in the tabs above to see win/loss analysis.")
    
    # Parameter Sensitivity Comparison
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📉 Parameter Sensitivity Comparison")
    if 'df_a' in st.session_state and 'df_b' in st.session_state:
        df_a_comp = st.session_state.df_a
        df_b_comp = st.session_state.df_b
        try:
            fig_sens = comparison.create_parameter_sensitivity_comparison(df_a_comp, df_b_comp)
            st.plotly_chart(fig_sens, use_container_width=True)
        except Exception as e:
            st.info(f"Parameter sensitivity comparison available after running sensitivity analysis. Error: {str(e)}")
    else:
        st.info("💡 Run the sensitivity analysis in the tabs above to see parameter sensitivity comparison.")

    # ============= SAVE/LOAD FUNCTIONALITY =============
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## Save & Load Scenarios")
    
    save_col1, save_col2 = st.columns(2)
    
    with save_col1:
        st.markdown("### 💾 Save Current Scenario")
        scenario_name = st.text_input(
            "Scenario Name", 
            value=f"scenario_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}",
            key='save_scenario_name'
        )
        
        if st.button("💾 Save Scenario", use_container_width=True):
            # Create configuration
            config = scenario_manager.create_scenario_config(
                global_params={
                    'n': n,
                    'premium': premium,
                    'vc_cost': default_vc_cost
                },
                scenario_a_params={
                    'pct_sick_min': pct_sick_min_a,
                    'pct_sick_max': pct_sick_max_a,
                    'pct_vc_min': pct_vc_min_a,
                    'pct_vc_max': pct_vc_max_a,
                    'vc_fee_min': vc_fee_min,
                    'vc_fee_max': vc_fee_max
                },
                scenario_b_params={
                    'pct_sick_min': pct_sick_min_b,
                    'pct_sick_max': pct_sick_max_b,
                    'pct_vc_min': pct_vc_min_b,
                    'pct_vc_max': pct_vc_max_b,
                    'ei_fee_min': ei_fee_min,
                    'ei_fee_max': ei_fee_max
                }
            )
            
            saved_name = scenario_manager.save_scenario_config(config, scenario_name)
            st.success(f"✅ Scenario '{saved_name}' saved successfully!")
        
        # Export to JSON
        if st.button("📤 Export to JSON", use_container_width=True):
            config = scenario_manager.create_scenario_config(
                global_params={'n': n, 'premium': premium, 'vc_cost': default_vc_cost},
                scenario_a_params={
                    'pct_sick_min': pct_sick_min_a, 'pct_sick_max': pct_sick_max_a,
                    'pct_vc_min': pct_vc_min_a, 'pct_vc_max': pct_vc_max_a,
                    'vc_fee_min': vc_fee_min, 'vc_fee_max': vc_fee_max
                },
                scenario_b_params={
                    'pct_sick_min': pct_sick_min_b, 'pct_sick_max': pct_sick_max_b,
                    'pct_vc_min': pct_vc_min_b, 'pct_vc_max': pct_vc_max_b,
                    'ei_fee_min': ei_fee_min, 'ei_fee_max': ei_fee_max
                }
            )
            json_str = scenario_manager.export_scenario_to_json(config, scenario_name)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"{scenario_name}.json",
                mime="application/json"
            )
    
    with save_col2:
        st.markdown("### 📂 Load Saved Scenario")
        saved_scenarios = scenario_manager.get_saved_scenarios()
        
        if saved_scenarios:
            scenario_list = list(saved_scenarios.keys())
            selected_scenario = st.selectbox(
                "Select a saved scenario:",
                scenario_list,
                key='load_scenario_select'
            )
            
            if st.button("📂 Load Scenario", use_container_width=True):
                config = scenario_manager.load_scenario_config(selected_scenario)
                if config:
                    global_params, scenario_a, scenario_b = scenario_manager.apply_scenario_config(config)
                    st.success(f"✅ Scenario '{selected_scenario}' loaded! Adjust parameters above to apply.")
                    st.json(config)
            
            if st.button("🗑️ Delete Scenario", use_container_width=True):
                if scenario_manager.delete_scenario(selected_scenario):
                    st.success(f"✅ Scenario '{selected_scenario}' deleted!")
                    st.rerun()
        else:
            st.info("No saved scenarios yet. Save a scenario to load it later.")
        
        # Import from JSON
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📥 Import from JSON")
        uploaded_file = st.file_uploader("Upload JSON file", type=['json'], key='import_json')
        if uploaded_file is not None:
            json_str = uploaded_file.read().decode('utf-8')
            config, imported_name = scenario_manager.import_scenario_from_json(json_str)
            if config:
                st.success(f"✅ Scenario '{imported_name}' imported successfully!")
                st.json(config)
            else:
                st.error("❌ Invalid JSON file. Please check the format.")


    # Export functionality
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## 📥 Export Analysis")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        if st.button("📊 Export Scenario A Data"):
            csv_a = df_a.to_csv(index=False)
            st.download_button(
                label="Download Scenario A CSV",
                data=csv_a,
                file_name="scenario_a_sensitivity_analysis.csv",
                mime="text/csv"
            )
    
    with export_col2:
        if st.button("📊 Export Scenario B Data"):
            csv_b = df_b.to_csv(index=False)
            st.download_button(
                label="Download Scenario B CSV",
                data=csv_b,
                file_name="scenario_b_sensitivity_analysis.csv",
                mime="text/csv"
            )